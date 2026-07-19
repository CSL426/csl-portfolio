# 架構文件

## 一句話

Monorepo:Vue 3 SPA(`apps/web`) + FastAPI 後端(`apps/api`),後端同時服務「LINE webhook」與「網頁 `/api/chat`」,共用同一套 Agent 抽象。

```
┌──────────────┐         ┌──────────────────────────────┐
│  LINE 使用者  │ ──webhook→ │                              │
└──────────────┘         │   FastAPI  (apps/api)        │
                         │   ├── /api/webhook/line      │
┌──────────────┐         │   ├── /api/chat              │
│  網頁使用者   │ ──/api/→  │   └── /api/health            │
│ (apps/web)   │         │                              │
└──────────────┘         │   AgentRegistry              │
                         │   ├── EchoAgent              │
                         │   ├── GoogleADKAgent ────────┼──→ Gemini (AI Studio / Vertex)
                         │   └── (你的 Agent)            │
                         └──────────────────────────────┘
```

## 目錄

```
resume/
├── apps/
│   ├── web/                  Vue 3 + TS + Vite + Tailwind
│   │   ├── src/
│   │   │   ├── pages/        Home / Resume / Agents / NotFound
│   │   │   ├── components/   resume/* + ui/*
│   │   │   ├── composables/  useDownload, useChat
│   │   │   ├── data/         resume.ts (履歷內容)
│   │   │   ├── router/
│   │   │   └── styles/
│   │   ├── public/           favicon, 履歷 PDF
│   │   ├── Dockerfile        nginx + proxy /api → api:8000
│   │   └── vite.config.ts    dev 時 proxy /api 到 localhost:8000
│   │
└── api/                  FastAPI + line-bot-sdk v3 (Python simplified layout)
    ├── server/           importable package — `from server.X import ...`
    │   ├── main.py       create_app(), CORS, lifespan
    │   ├── core/         config (pydantic-settings), logging (structlog)
    │   ├── agents/       BaseAgent, EchoAgent, GoogleADKAgent, registry
    │   ├── routes/       health, chat, webhook 路由
    │   ├── integrations/ line_client (parser + reply)
    │   ├── schemas/      pydantic models
    │   └── py.typed      PEP 561 typed package marker
    ├── tests/            pytest (pythonpath=["."])
    ├── pyproject.toml    uv-managed, hatchling build
    └── Dockerfile        uv sync → uvicorn server.main:app

│
├── docs/                     架構與內容素材
├── archive/legacy-html/      舊 resume.html + Python 工具
├── docker-compose.yml        web (8080) + api (8000)
├── pnpm-workspace.yaml
└── package.json              workspace 根
```

## Agent 抽象

```python
class BaseAgent(ABC):
    name: str
    @abstractmethod
    async def handle(self, ctx: AgentContext) -> AgentReply: ...
```

`AgentContext` 帶 `user_id` / `source` ('line' | 'web' | 'test') / `message` / `metadata`。
`AgentReply` 帶 `text` + `extra`(quick reply、image url 等)。

**路由規則**:訊息以 `/<agent_name>` 開頭 → 切到那個 agent;否則用 `DEFAULT_AGENT`。

新增一個 Agent:

```python
# apps/api/server/agents/my_agent.py
from server.agents.base import AgentContext, AgentReply, BaseAgent

class MyAgent(BaseAgent):
    name = "my"
    async def handle(self, ctx: AgentContext) -> AgentReply:
        return AgentReply(text=f"hello {ctx.user_id}")
```

註冊:在 `server/agents/registry.py` 加 `registry.register(MyAgent())`。

## LINE Webhook 流程

1. LINE → `POST /api/webhook/line`(含 `x-line-signature` header)
2. `WebhookParser` 驗章,失敗 → 400
3. 解析出來的 events 丟到 `BackgroundTasks`,**立刻回 200**(LINE 對非 2xx 會重試)
4. 背景任務 `_dispatch_event`:抽 text → 用 `registry.route` 選 agent → `agent.handle()` → `reply_text(reply_token, ...)`

未設定 `LINE_CHANNEL_SECRET` 時 webhook 回 503,本機可只用 `/api/chat` 開發。

## 本機開發流程

1. `cp .env.example .env` 在 **repo 根目錄**,填 `GOOGLE_API_KEY` / LINE 等
2. **後端**:`uv sync --project apps/api && uv run --project apps/api uvicorn server.main:app --reload`
3. **前端**:`pnpm install && pnpm dev:web`(Vite 會 proxy `/api` → `localhost:8000`)
4. **LINE webhook 本機測試**:`cloudflared tunnel --url http://localhost:8000` 或 `ngrok http 8000`,把 URL 填到 LINE Developers Console 的 Webhook URL(尾巴加 `/api/webhook/line`)

## 環境變數與 Ports

**單一 `.env` 放在 repo 根目錄**,後端、Vite、docker-compose、nginx envsubst 都讀同一份。
- `apps/api/.env` 若存在會覆蓋根 `.env`(本地實驗用)
- 前端執行期設定由 nginx 在 container 啟動時 envsubst(`API_UPSTREAM` / `SERVER_NAME` / `NGINX_PORT`),build-time 不烘進 bundle

### Ports

**對外只開 `PUBLIC_PORT`(預設 8787)** — 主機只映射這一個 port 到 web 容器,
所有外部流量都走 nginx → `/api/` proxy 到內網的 api 容器。

內部固定 port(寫在 Dockerfile/compose 預設值,通常不用改):
- api 容器內:`8000`(uvicorn 綁到這)
- web 容器內 nginx:`80`
- Vite dev server(本機):`5173`

要改任一個 → compose / vite.config / Dockerfile 都支援同名 env 覆蓋,但日常用不到。

## Frontend nginx 設定(runtime templating)

`apps/web/nginx.conf.template` 用 `${API_UPSTREAM}` / `${SERVER_NAME}` 兩個變數。
`nginx:alpine` 基底映像的 entrypoint 會在啟動時對 `/etc/nginx/templates/*.template`
跑 `envsubst` 後輸出到 `/etc/nginx/conf.d/`。我們用 `NGINX_ENVSUBST_FILTER` 限制
只替換指定變數,避免 nginx 自己的 `$host` / `$uri` 被誤吃掉。

好處:**同一個 image 不重 build 就能換後端 upstream**(local docker / Cloud Run / Render 各自設 env 即可)。

## Google ADK 整合

`GoogleADKAgent` 包了 ADK 的 `LlmAgent` + `InMemoryRunner`,共用一個 runner、依
`(source, user_id)` 切 session,所以 LINE 與網頁的對話記憶各自獨立。

**設定**:取得 [AI Studio API key](https://aistudio.google.com/app/apikey) 填到 `.env` 的 `GOOGLE_API_KEY`。

**加工具(Function calling)**:在 `google_adk.py` 的 `LlmAgent(...)` 加 `tools=[my_func, ...]`,
ADK 會自動把 Python 函式 docstring 轉成 schema 餵給 Gemini。

**換成 multi-agent**:把 `LlmAgent` 換成 `SequentialAgent` / `ParallelAgent` / 用 `sub_agents=[...]`
組合即可,`BaseAgent` 對外介面不變。

**Session 持久化**:目前用 `InMemoryRunner` (重啟即失憶)。要持久化改用 ADK 的
`DatabaseSessionService` 或 `VertexAiSessionService`,在 `_ensure_runner` 注入即可。

## 部署候選

- **api**:Cloud Run / Railway / Render(任一個都接受 Docker)
- **web**:Cloudflare Pages / Vercel(靜態托管),或跟 api 一起塞進 Cloud Run
- 同源:把 web 跟 api 放同一 domain,免處理 CORS;否則調整 `CORS_ORIGINS`
i 放同一 domain,免處理 CORS;否則調整 `CORS_ORIGINS`
