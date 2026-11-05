# Cloud Run 部署指南

> 狀態:Draft

單一 container 架構:根目錄 `Dockerfile` 先用 pnpm build 出 Vite 靜態檔,再由 FastAPI(`SpaStaticFiles`)同時服務前端與 `/api/*`。不需要 nginx、沒有 CORS 問題,Cloud Run 只要管一個 service。

GitHub Actions(`.github/workflows/deploy-cloudrun.yml`)在 push 到 `main` 時自動 build image → 推上 Artifact Registry → 部署 Cloud Run。驗證走 Workload Identity Federation(WIF),**不需要在 GitHub 存任何 GCP 金鑰檔**。

## 一次性設定

以下指令在本機 `gcloud` 執行一次即可(先 `gcloud auth login`)。變數自行代入:

```bash
PROJECT_ID="你的-gcp-project-id"
REGION="asia-east1"                      # 台灣機房
GITHUB_REPO="你的帳號/你的repo名"          # 例如 sparkliao/portfolio
SA_NAME="github-deployer"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
```

### 1. 啟用 API 與建立 Artifact Registry

```bash
gcloud config set project "$PROJECT_ID"
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
  iamcredentials.googleapis.com

gcloud artifacts repositories create containers \
  --repository-format=docker --location="$REGION"
```

### 2. 建立部署用 Service Account

```bash
gcloud iam service-accounts create "$SA_NAME"

for ROLE in roles/run.admin roles/artifactregistry.writer roles/iam.serviceAccountUser; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${SA_EMAIL}" --role="$ROLE"
done
```

### 3. Workload Identity Federation(讓 GitHub Actions 免金鑰驗證)

```bash
gcloud iam workload-identity-pools create github \
  --location=global --display-name="GitHub Actions"

gcloud iam workload-identity-pools providers create-oidc github-oidc \
  --location=global --workload-identity-pool=github \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository == '${GITHUB_REPO}'"

PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")

gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github/attribute.repository/${GITHUB_REPO}"
```

### 4. GitHub repo 設定 Secrets

GitHub repo → Settings → Secrets and variables → Actions,新增三個 secret:

| Secret | 值 |
|--------|-----|
| `GCP_PROJECT_ID` | `$PROJECT_ID` |
| `GCP_SA_EMAIL` | `${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com` |
| `GCP_WIF_PROVIDER` | `projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github/providers/github-oidc` |

### 5. 首次部署後的 service 設定(執行一次)

第一次 workflow 跑完 service 建立後,設定公開存取與 Gemini API key:

```bash
# 允許匿名瀏覽(個人網站)
gcloud run services add-iam-policy-binding csl-portfolio \
  --region="$REGION" --member=allUsers --role=roles/run.invoker

# Gemini API key 放 Secret Manager,掛進 service
gcloud services enable secretmanager.googleapis.com
echo -n "你的-gemini-api-key" | gcloud secrets create google-api-key --data-file=-

# 給 Cloud Run 的執行身分讀取權
gcloud secrets add-iam-policy-binding google-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role=roles/secretmanager.secretAccessor

gcloud run services update csl-portfolio --region="$REGION" \
  --set-secrets=GOOGLE_API_KEY=google-api-key:latest \
  --set-env-vars=APP_ENV=prod
```

改用 Claude 當預設 Agent(金鑰同樣放 Secret Manager):

```bash
echo -n "你的-anthropic-api-key" | gcloud secrets create anthropic-api-key --data-file=-
gcloud secrets add-iam-policy-binding anthropic-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role=roles/secretmanager.secretAccessor

gcloud run services update csl-portfolio --region="$REGION" \
  --update-secrets=ANTHROPIC_API_KEY=anthropic-api-key:latest \
  --update-env-vars=DEFAULT_AGENT=claude
# 金鑰若沒有綁定單一 workspace,再加上 ANTHROPIC_WORKSPACE_ID=wrkspc_...
```

之後每次 GitHub Actions 部署只換 image,**env vars 與 secrets 設定會沿用**,不用重設。LINE bot 金鑰(`LINE_CHANNEL_SECRET` / `LINE_CHANNEL_ACCESS_TOKEN`)之後要用同樣方式掛。

## 尚未完成 / 注意事項

- 部署成功且健康檢查通過後,workflow 只留接流量的 revision 與它用的映像,其他都刪掉,所以沒有一鍵回滾;要退版就 revert 後重新部署。刪映像需要部署帳號在 `containers` 映像庫有 `roles/artifactregistry.repoAdmin`:

  ```bash
  gcloud artifacts repositories add-iam-policy-binding containers --project="$PROJECT_ID" --location="$REGION" \n    --member="serviceAccount:github-deployer@${PROJECT_ID}.iam.gserviceaccount.com" \n    --role=roles/artifactregistry.repoAdmin
  ```

- 對話歷史與限流計數都存在程序記憶體,所以 workflow 固定 `--max-instances=1`;重啟或重新部署後會清空。上線前也請到 Anthropic Console 設定月花費上限。
- Cloud Run 檔案系統是暫時性的——知識庫資料不能存本機 SQLite/檔案,簡易版先把知識文件打包進 image,動態編輯需求出現時再上 Firestore。
- 費用:scale to zero + 免費額度,個人站正常流量下應為 $0。
- 本機驗證 image:`docker build -t csl-portfolio . && docker run -p 8080:8080 -e GOOGLE_API_KEY=... csl-portfolio`,瀏覽 `http://localhost:8080`。
