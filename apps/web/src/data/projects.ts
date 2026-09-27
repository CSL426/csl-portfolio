import type { ProjectItem } from '@/types/project'

export const projects: ProjectItem[] = [
  {
    id: 'acg',
    name: 'ai-config (acg)',
    tagline: '跨 AI CLI 設定同步工具：Claude Code · Codex · Antigravity',
    period: '2026/7 - 至今',
    status: 'active',
    featured: true,
    summary:
      '以私有 Git 資料庫為單一事實來源，把 Claude Code、Codex 與 Antigravity 的 rules、skills、agents、settings 在多台機器與多個作業系統之間同步。發行為單一執行檔，目標機器只需要 Git。',
    highlights: [
      'init / apply / status / pull / push 五個核心指令：pull 只做 fast-forward、push 前先 preflight 掃描憑證與越界路徑並顯示完整 diff，commit 訊息由 staged 路徑本地推導，絕不 force-push。',
      '共享記憶與工作線交接：專案日誌跨 Claude Code、Codex、Antigravity 擷取；context 用量到門檻時透過 statusLine hook 提醒交接，讓多個 session 同時處理同一專案。',
      'PyInstaller 單檔發行，GitHub Actions 在 Linux、macOS、Windows 三平台跑測試；版本目錄保留最近五版可一鍵回滾，Bash 與 PowerShell tab completion。',
      '桌面 GUI（pywebview + Vite/TypeScript，Playwright 端對端測試）與 Claude Code plugin marketplace，提供 /acg:status、/acg:handoff 等八個 slash 指令。',
      '約 2 萬行 Python、74 個測試模組、64 版以上的 changelog；symlink、junction、路徑包含等皆視為安全邊界處理。',
    ],
    stack: ['Python 3.11', 'Git', 'PyInstaller', 'GitHub Actions', 'pywebview', 'TypeScript', 'Vite', 'Playwright'],
    links: [
      { label: 'GitHub', href: 'https://github.com/CSL426/ai-config' },
      { label: '簡介投影片', href: 'https://csl426.github.io/ai-config/' },
    ],
  },
  {
    id: 'line-ai-agent',
    name: 'LINE Bot AI 客服',
    tagline: '家業與地方單位的知識庫 AI Agent',
    period: '2025 - 至今',
    status: 'live',
    summary:
      '以 Google ADK 開發 AI Agent 並整合知識庫，透過 LINE Official Account 提供客服。獨立完成架構設計、GCP Cloud Run 部署與維運，另接案協助地方單位建置同類系統。',
    highlights: [
      'Google ADK + Gemini 對話流程，知識庫檢索回答常見問題。',
      'LINE webhook 驗章後立即回 200，事件丟到背景任務處理，避免 LINE 重送。',
      'GCP Cloud Run 無伺服器部署，GitHub Actions 自動發布。',
    ],
    stack: ['Python', 'FastAPI', 'Google ADK', 'Gemini', 'LINE Messaging API', 'GCP Cloud Run'],
  },
  {
    id: 'portfolio',
    name: 'csl-portfolio',
    tagline: '這個網站：履歷、專案與 AI Agent 實驗場',
    period: '2026',
    status: 'live',
    summary:
      'Vue 3 SPA 加 FastAPI 後端的 monorepo。後端同時服務 LINE webhook 與網頁 /api/chat，共用同一套 Agent 抽象；履歷頁可直接輸出 PDF / PNG，另提供 ATS 純文字版。',
    highlights: [
      'Agent registry：訊息以 /<agent> 開頭即切換 Agent，網頁與 LINE 共用路由。',
      'nginx 於容器啟動時 envsubst 注入設定，前端 bundle 不烘進任何環境變數。',
      'Workload Identity Federation 免金鑰部署到 Cloud Run。',
    ],
    stack: ['Vue 3', 'TypeScript', 'Tailwind', 'FastAPI', 'Docker', 'GCP Cloud Run'],
    links: [{ label: 'GitHub', href: 'https://github.com/CSL426/csl-portfolio' }],
  },
  {
    id: 'route-leisure',
    name: '路遊憩',
    tagline: 'LINE Bot 個人化旅遊行程規劃',
    period: '2024',
    status: 'archived',
    summary:
      'TibaMe AI 應用開發培訓專題。整合 LINE Bot、LLM 與資料庫實現個人化行程規劃，負責路線規劃演算法、對話流程與 Prompt 工程，以 Docker 容器化部署。',
    highlights: [
      '路線規劃演算法設計與資料庫整合。',
      'LLM 對話流程與 Prompt 工程，LINE Bot 介面開發。',
    ],
    stack: ['Python', 'LLM', 'LINE Messaging API', 'Docker'],
  },
]
