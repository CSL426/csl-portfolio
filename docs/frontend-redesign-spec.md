# Frontend Redesign Spec — csl-portfolio

本規格書定義 `apps/web` 前端整體改版（Hallmark Multi-page Redesign）的設計系統、逐頁結構調整、相容邊界與驗證標準，用以系統性解決既有前端的模板感、對比度不足、多層嵌套與互動細節缺口。

---

## 1. 目標與範圍（Scope & Non-Goals）

### 目標
1. **建立單一設計系統**：於專案根目錄產出 `design.md`，並於 `apps/web/src/styles/tokens.css` 以 OKLCH 集中管理色彩、字體、間距與動態 token，消除散落元件的硬編碼色碼。
2. **重做作品集外殼結構**：重新設計 `AppNav`、`App.vue` 頁尾、`HomePage`、`ProjectsPage`、`AgentsPage`、`NotFoundPage`，移除漸層大標、重複 eyebrow、置中模板與跨頁重複的三欄等寬白卡。
3. **補齊無障礙與響應式底線**：修正連結對比度（WCAG AA ≥ 4.5:1）、補齊高對比零延遲 `:focus-visible` 外框、`prefers-reduced-motion: reduce`、`overflow-x: clip`、按鈕防折行（`whitespace-nowrap`）與 `:active` 回饋。

### Non-Goals（明確不動的項目）
- **不動 `/resume` 三頁 A4 履歷內頁版型與高度**：`ProfileCard`、`SidebarPanel`、`ExperienceCard`、`AutobioCard`、`EnglishSection`、`ResumeSheet` 維持既有 PDF 對照設計與 297 mm（≈ 1122.5 px）頁高。
- **不動資料內容與後端**：不修改 `src/data/resume.ts`、`src/data/projects.ts` 文案與 `apps/api`。
- **不刪除既有檔案或路由**：所有改動採 in-place 更新或新增 token／設計文件，零刪除。
- **不破壞既有 Playwright E2E 測試**（詳見第 5 節）。

---

## 2. 設計系統規格（`design.md` & `tokens.css`）

### 2.1 Genre 與整體調性
- **Genre**：`modern-minimal`
- **調性**：克制、精準、偏工程師與研究者的工具美學（無裝飾性漸層、無重複毛玻璃、以細線與排版層次取代厚重陰影）。

### 2.2 色彩系統（OKLCH，錨定既有冷藍 `H ≈ 242°`）

| Token | Value | 用途與對比說明 |
| --- | --- | --- |
| `--color-paper` | `oklch(97.2% 0.006 242)` | 頁面基底（微冷紙白，取代 `#edf1f5`） |
| `--color-paper-2` | `oklch(99.2% 0.003 242)` | 卡片／工作區表面（極淡冷白，取代純白 `#fff`） |
| `--color-surface-subtle` | `oklch(94.2% 0.011 242)` | 次要區塊、標籤底色（取代 `#e8edf3`） |
| `--color-ink` | `oklch(22% 0.02 250)` | 主文字、深色按鈕底色（對比 > 14:1） |
| `--color-ink-2` | `oklch(46% 0.02 248)` | 次要說明文字（對比 > 6.5:1） |
| `--color-rule` | `oklch(87% 0.014 242)` | 1px 結構細線（取代大面積陰影） |
| `--color-accent` | `oklch(48% 0.12 245)` | 主強調色／文字連結（白底對比 ≥ 6.2:1，取代僅 2.56:1 的 `#76abd6`） |
| `--color-accent-soft` | `oklch(71% 0.08 242)` | 保留既有 `#76abd6` 語感，僅供大面積裝飾或履歷頭像卡使用，不用於小字 |
| `--color-focus` | `oklch(48% 0.12 245)` | 鍵盤 `:focus-visible` 2px 外框 |
| `--color-status-live-bg` / `-fg` | `oklch(94% 0.04 155)` / `oklch(38% 0.10 155)` | `LIVE` / `ACTIVE` 狀態標籤 |
| `--color-status-soon-bg` / `-fg` | `oklch(95% 0.05 85)` / `oklch(44% 0.10 75)` | `SOON` 狀態標籤 |
| `--color-status-muted-bg` / `-fg` | `oklch(93% 0.008 242)` / `oklch(46% 0.02 248)` | `ARCHIVED` 狀態標籤 |
| `--color-danger` | `oklch(50% 0.18 25)` | 錯誤提示文字 |

> `tailwind.config.ts` 的 `brand.*` 保留既有 key（`brand-ink`、`brand-muted`、`brand-start` 等）以確保 `.bg-brand-ink` 等既有選擇器與履歷元件 100% 相容。

### 2.3 字體系統（2+1 配對，標題一律正體）
- **Display（`--font-display`）**：`'Space Grotesk', 'Noto Sans TC', sans-serif`（字重 500 / 700，正體 `font-style: normal`）
- **Body（`--font-body`）**：`'Noto Sans TC', 'Microsoft JhengHei', 'PingFang TC', system-ui, sans-serif`（字重 400 / 500）
- **Mono（`--font-mono`）**：`'JetBrains Mono', ui-monospace, SFMono-Regular, monospace`（字重 400 / 500，搭配 `tabular-nums` 用於年份、`<code>`、指令與技術標籤）
- 於 `apps/web/index.html` 載入 Google Fonts：`Space Grotesk (500;700)`、`JetBrains Mono (400;500)` 與既有 `Noto Sans TC (400;500;700)`。

### 2.4 動態與互動準則
- **Motion stance**：`motion-cut`（不引入動畫庫、不做捲動淡入）。
- **Transition**：僅針對明確屬性（`transition-colors` 或 `transition-transform`），時長 `180ms`、曲線 `cubic-bezier(0.16, 1, 0.3, 1)`。
- **焦點環**：所有互動元素具備即時（無過渡動畫）`focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus)]`。
- **按壓回饋**：按鈕具備 `active:translate-y-px`。
- **Reduced motion**：`@media (prefers-reduced-motion: reduce)` 關閉位移與過渡效果。

---

## 3. 逐頁改版規格（Page-by-Page Spec）

### 3.1 全站外殼：`AppNav.vue`、`App.vue`、`IconButton.vue`、`main.css`
- **導覽列（`AppNav.vue` — N5 Floating pill）**：
  - 移除全寬黏性毛玻璃條（`sticky top-0 w-full border-b bg-white/70 backdrop-blur`）。
  - 改為距頂部微留白（`pt-[0.875rem]`）的居中浮動膠囊（`max-w-[44rem]`、`rounded-full`、`border border-[var(--color-rule)]`、`bg-[var(--color-paper-2)]/95`、輕微陰影），左側 `Spark.dev`（`font-display`）、右側 4 個連結（`Home / Resume / Projects / Agents`）。
  - 手機版（320px–390px）：收緊內距與字級，維持單行不換行、不產生橫向捲動。
- **頁尾（`App.vue` — Ft2 Inline single line）**：
  - 移除置中孤立版權字樣。
  - 改為對齊內容寬度的單行細線上緣 colophon：左側 `© 2026 廖啓舜 · Spark`，右側簡潔內部快速連結（`Resume`、`Projects`、`Agents`）。
- **按鈕元件（`IconButton.vue`）**：
  - 補上 `whitespace-nowrap`、`active:translate-y-px`、高對比 `focus-visible` 外框，將 `transition` 改為 `transition-colors`。
- **全域樣式（`main.css`）**：
  - 匯入 `./tokens.css`，在 `html, body` 加入 `overflow-x: clip`。
  - 保留 `.resume-page`、`.resume-frame` 與完整 `@media print` 規則不動。

### 3.2 首頁：`HomePage.vue`（Split Studio / H2 Split Diptych）
- **移除**：`PORTFOLIO` eyebrow、置中大標、`bg-clip-text` 漸層文字、3 欄等寬白卡。
- **上半部（不對稱雙欄 `lg:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)]`）**：
  - **左欄**：大字實心正體主標（`廖啓舜` + `Spark`）、簡潔定位敘述（AI 工程師 · 太空科學碩士）、兩組明確行動按鈕（主按鈕「查看履歷」→ `/resume`、次按鈕「瀏覽專案」→ `/projects`）。
  - **右欄（F3 細線規格卡）**：以 1px 細線分隔的精簡資訊列（`身分`、`背景`、`主力專案`、`即時互動`），使用 `font-mono` 標示關鍵詞與狀態，無多餘裝飾。
- **下半部（不對稱導流區塊）**：
  - 細線分隔後，左側以寬幅區塊呈現精選入口（`ai-config (acg)` 與專案總覽 → `/projects`），右側以垂直雙格細線區塊呈現「履歷（視覺版 / ATS）」→ `/resume` 與「AI Agents 實驗場」→ `/agents`。
  - 所有文字連結改用高對比 `--color-accent`。

### 3.3 專案頁：`ProjectsPage.vue`（Editorial Case + F3 細線索引）
- **移除**：`PROJECTS` eyebrow 與重複的三欄等寬白卡（`md:grid-cols-3`）。
- **頁首**：左對齊大標「專案作品」+ 一行簡述，下方 1px 細線分隔。
- **Featured 區塊（`ai-config (acg)`）**：
  - 改為細線外框的 `--color-paper-2` 主區塊，內部採不對稱雙欄（`lg:grid-cols-[minmax(0,1.6fr)_minmax(0,1fr)]`）：
    - 左欄：專案名稱、狀態標籤、tagline、摘要與 5 點亮點清單。
    - 右欄（側邊規格欄）：`期間`（`font-mono tabular-nums`）、`技術堆疊`（mono 標籤）、`外部連結`按鈕（GitHub / 簡介投影片）。
- **Others 區塊（其餘 3 個專案）**：
  - 改為 **F3 細線結構化索引列**（垂直排列、列間以 1px `--color-rule` 分隔，桌面版為 `grid-cols-[minmax(0,14rem)_minmax(0,1fr)_auto]`）：
    - 左欄：專案名稱 + 狀態標籤 + 年份（`tabular-nums`）。
    - 中欄：tagline、摘要與精簡技術標籤列。
    - 右欄：外部連結（若有），使用 `--color-accent`。

### 3.4 AI Agents 頁：`AgentsPage.vue`（Workbench）
- **移除**：`AI AGENTS` eyebrow、厚重三欄白卡、三層 card-in-card 嵌套（白卡包灰框再包白陰影氣泡）。
- **頂部 Agent 狀態列**：
  - 維持 `<ul class="..."><li><h2>...</h2><span>LIVE / SOON</span>...</li></ul>` 語意結構（確保 E2E 測試 `page.locator('li').filter({ has: page.getByRole('heading', { name: 'Gemini' }) })` 通過）。
  - 視覺改為緊湊的單列細線分隔條（桌面版 3 欄以 1px 細線分割於單一外框內，無獨立卡片陰影），`Echo` 以低調說明標示為 pipeline 測試用。
- **下方對話工作區（單層扁平 Workbench）**：
  - 外層單一 `--color-paper-2` + 1px `--color-rule` 容器，頂部標題列（「試一下」+「清除」按鈕 + 1px 底線）。
  - 訊息清單（保留 `.overflow-y-auto`）：直接置於容器內（不另包一層灰底圓角框），使用者訊息保留 `.bg-brand-ink text-white`，Agent 回覆改以淺色底 `--color-surface-subtle` + 1px 細線呈現（拿掉 `shadow-card`），Agent 名稱以 `font-mono` 標示。
  - 空狀態：左對齊提示文案 + 4 個快捷問題按鈕（維持在 `.overflow-y-auto` 內，確保 E2E `messageList(page).getByRole('button')` 計數為 4）。
  - 輸入列：細線上緣分隔，`<input placeholder="輸入訊息…">` 補上高對比 `:focus-visible` 外框，送出按鈕維持 `shrink-0 whitespace-nowrap` 並加上 `active:translate-y-px`。

### 3.5 履歷頁：`ResumePage.vue` & `AtsResumePage.vue`（僅工具列微調）
- **工具列調整**：
  - 移除 `sticky top-[3.5rem] bg-white/85 backdrop-blur`，改為非黏性實底細線操作條（`border border-[var(--color-rule)] bg-[var(--color-paper-2)]`），消除捲動時與導覽列雙層毛玻璃重疊。
  - 移除 `RESUME` / `ATS RESUME` eyebrow；工具列標題由 `<h2>` 改為 `<p>` 修正標題層級。
  - **保留所有按鈕與連結文字**：`下載 PDF (現場輸出)`、`下載 PNG`、`官方版 PDF`、`ATS 版`、`列印 / 另存 PDF`、`回視覺版`。
- **履歷本體**：
  - `/resume` 三頁 `<ResumeSheet>` 與所有 `components/resume/*` **不更動**，確保 Page 1 高度維持 297 mm。
  - `/resume/ats` `.ats-page` 與 `@media print` 維持原樣。

### 3.6 404 頁：`NotFoundPage.vue`
- 使用 `font-display` 與 `--color-accent` 呈現 `404`，補齊「回首頁」連結的高對比 `:focus-visible` 與 `active:translate-y-px`。

---

## 4. 檔案異動清單

| 類型 | 檔案路徑 | 說明 |
| --- | --- | --- |
| 新增 | `design.md` | 鎖定全站設計系統（Hallmark Multi-page 單一事實來源） |
| 新增 | `apps/web/src/styles/tokens.css` | OKLCH 色彩、字體、間距、動態 token |
| 新增 | `.hallmark/log.json` | 記錄本次 `scope: "app"` 改版紀錄 |
| 修改 | `apps/web/index.html` | 載入 `Space Grotesk` + `JetBrains Mono` + `Noto Sans TC` |
| 修改 | `apps/web/tailwind.config.ts` | 擴充 `font-display` / `font-mono` 並對接語意 token |
| 修改 | `apps/web/src/styles/main.css` | 匯入 `tokens.css`、加 `overflow-x: clip`、`prefers-reduced-motion`、`:focus-visible` |
| 修改 | `apps/web/src/App.vue` | 改為 Ft2 單行左對齊頁尾 |
| 修改 | `apps/web/src/components/ui/AppNav.vue` | 改為 N5 浮動膠囊導覽列 |
| 修改 | `apps/web/src/components/ui/IconButton.vue` | 補 `whitespace-nowrap`、`:active`、`:focus-visible`、明確 `transition` |
| 修改 | `apps/web/src/pages/HomePage.vue` | Split Diptych + 不對稱導流區塊 |
| 修改 | `apps/web/src/pages/ProjectsPage.vue` | 精選雙欄 + F3 細線索引列 |
| 修改 | `apps/web/src/pages/AgentsPage.vue` | 單層扁平 Workbench + 精簡狀態列 |
| 修改 | `apps/web/src/pages/ResumePage.vue` | 工具列去雙層毛玻璃與標題層級修正（內頁不動） |
| 修改 | `apps/web/src/pages/AtsResumePage.vue` | 工具列去雙層毛玻璃與標題層級修正（內頁不動） |
| 修改 | `apps/web/src/pages/NotFoundPage.vue` | 對齊新設計系統與焦點環 |
| 刪除 | *無* | 不刪除任何檔案 |

---

## 5. E2E 相容契約與驗證計畫

### 5.1 必須維持相容的 `apps/web/e2e/site.spec.ts` 選擇器
- `nav` 內連結精確文字：`Home`、`Resume`、`Projects`、`Agents`
- `/agents`：`li` 包含 `heading` `Gemini` 與文字 `SOON`
- `/agents`：輸入框 placeholder `輸入訊息…`、訊息區 `.overflow-y-auto`、使用者氣泡 `.bg-brand-ink`、清除按鈕 `清除`、空狀態 4 個快捷按鈕位於 `.overflow-y-auto` 內
- `/resume`：按鈕 `官方版 PDF`、`下載 PNG`、`下載 PDF (現場輸出)`、連結 `ATS 版`
- `/no-such-page`：顯示 `404`
- 手機版 `390×844`：5 個路由皆無橫向捲動（`scrollWidth <= clientWidth`），且 `/agents` 輸入列高度 `< 48px`

### 5.2 驗收指令與檢查項目
1. **靜態與單元測試**：執行 `pnpm check`（type-check + ESLint + Vitest + Python lint/mypy/pytest）。
2. **正式建置**：執行 `pnpm build:web` 確認 chunk 大小與建置無誤。
3. **端對端測試**：執行 `pnpm test:e2e` 確認 Playwright 全數綠燈。
4. **視覺與 A4 高度檢查**：以無頭瀏覽器檢查 320px / 375px / 1280px 響應式版面，並確認 `/resume` 在 1200×1697 下三頁 `.resume-page` 高度維持 297 mm（≈ 1122.5 px）未溢頁。
