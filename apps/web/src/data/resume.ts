import type { ResumeData } from '@/types/resume'

export const resumeData: ResumeData = {
  profile: {
    nameZh: '廖啓舜',
    nameEn: 'Liao Chi-Shun',
    contacts: [
      { label: 'Email', value: 'spark.cs.liao@gmail.com', href: 'mailto:spark.cs.liao@gmail.com' },
      { label: 'Phone', value: '0983-967-396', href: 'tel:+886983967396' },
    ],
  },
  education: [
    {
      school: '國立中央大學',
      degree: '太空科學與工程學系碩士',
      period: '2021/9 - 2023/7',
      note: '日冕洞演化與高速太陽風之關係',
    },
    {
      school: '國立中央大學',
      degree: '大氣科學學系太空組',
      period: '2017/9 - 2021/6',
    },
  ],
  tools: ['Python、PyTorch', 'FastAPI', 'Vue', 'RAG、MongoDB', 'PySpark、Databricks', 'Linux、Git、Docker', 'GCP、AWS', 'ETL Pipeline', 'CLI、GitHub Actions'],
  experiences: [
    {
      title: 'AI 工程師｜創造智能（2025/4 - 至今）',
      bullets: [
        'AI 虛擬人平台：訊息層、RAG 檢索，串接 lip-sync 與 TTS。',
        'LLM 供應商與模型備援路由、TTS 備援。',
        'ASR／TTS 評測（CER／WER、延遲、併發）與推論調校。',
        '台語 TTS finetune 與語料處理。',
        '向 NVIDIA NeMo 提交修正 PR，解決載入權重時 CPU 記憶體重複佔用的問題。',
      ],
    },
    {
      title: '個人專案與接案',
      bullets: [
        '開源 CLI「ai-config (acg)」：跨 Claude Code、Codex、Antigravity 的設定同步與交接工具，單檔發行、三平台 CI。',
        'LLM 批次管線（PySpark、Databricks）：模組化重構與測試、併發與重試調校，標註空值率由 44% 降至 4.7%；管線斷線根因追查與補跑。',
        'LINE Bot AI 客服：Google ADK、以公司資料回答客戶問題，獨立部署與維運於 GCP Cloud Run。',
      ],
    },
    {
      title: 'TibaMe - AI 應用開發培訓（專案 - 路遊憩）',
      bullets: [
        '主導旅遊規劃系統：整合 Line Bot、LLM 與資料庫實現個人化行程規劃，設計路線規劃演算法，以 Docker 容器化部署。',
      ],
    },
    {
      title: '學術研究 - 太陽物理研究',
      bullets: [
        '太陽物理研究累積影像分析與演算法設計經驗，熟悉大規模數據處理；於 TGA、AOGS、JpGU 國際研討會發表成果。',
      ],
    },
  ],
  strengths: [
    '語音 AI：ASR／TTS 評測、finetune 與推論調校。',
    'LLM 應用：RAG 檢索、Agent、模型備援路由。',
    '資料工程：PySpark 批次管線、併發與重試調校、斷線追查與補跑。',
    '後端與部署：Python 後端、Docker、AWS 與 GCP 部署。',
    '研究背景：太空科學碩士，擅長演算法設計與大規模數據處理，研究成果於三場國際研討會發表。',
  ],
  reference: {
    name: '楊宏文',
    role: '顧問｜勞動部勞發署講師',
    email: 'gohubert@gmail.com',
    phone: '0955-520-080',
  },
  autobiography: [
    {
      heading: '關於我與特質',
      paragraphs: [
        '各位主管、HR您好，我是廖啓舜，畢業於國立中央大學太空科學與工程學系碩士班。從高中開始參與籃球校隊，曾隨隊打進 HBL 乙組北區複賽，到大學時期更帶領系隊拿下大地盃亞軍，這些經歷讓我深知團隊合作的重要性。在團隊中我善於促進溝通交流，能在團隊中扮演潤滑劑的角色。在追求目標時，具有堅持和全力以赴的特質，這種態度不只展現在球場上，也幫助我在學術研究和專案開發上都能達到理想成果。',
      ],
    },
    {
      heading: '學習歷程與專業發展',
      paragraphs: [
        '大學期間，我精進了 MATLAB 與 Python 程式設計，並透過雷達專題與衛星姿態控制課程奠定跨領域整合能力。此外，擔任系籃副隊長與女籃教練的經歷，亦培養了我的團隊管理與溝通協調能力。',
        '碩士期間專注於太陽物理研究，負責開發影像分析演算法，處理並分析大規模觀測數據，研究成果已發表於三場國際研討會（TGA、AOGS、JpGU）。在此期間，我透過自學演算法培養了量化分析與獨立解決問題的能力，並確立投身機器學習領域的志向。畢業後，我參與 TibaMe AI 工程師培訓，系統化掌握 Python 生態系、PyTorch 深度學習框架與軟體開發規範。',
        '在「路遊憩」專題中，我擔任核心開發角色，負責路線規劃演算法設計、LLM 對話流程與 Prompt 工程，並完成資料庫整合、API 串接及 LINE Bot 介面開發，從中磨練了敏捷協作與跨模組整合技能。',
        '在目前的工作中，我參與多個 AI/LLM 與語音專案的開發與部署。其中規模最大的是 AI 虛擬人平台，我負責後端訊息層與 RAG 檢索，並串接對嘴（Lip-sync）與語音合成（TTS）；此外也進行 ASR／TTS 模型評測、推論調校與台語 TTS finetune，並向 NVIDIA NeMo 提交修正 PR。在工作之外，我以接案方式進行 LLM 批次資料管線的模組化與調校，基於 Google ADK 與 GCP Cloud Run 為家族事業獨立研發並維運 LINE Bot 智慧客服系統，並開源了跨 AI CLI 的設定同步工具 ai-config（acg），以單一執行檔發行並在三個作業系統上持續整合測試。這些實戰經驗培養了我端到端（End-to-End）交付 AI 應用與解決複雜問題的能力，期盼能為貴團隊帶來實質貢獻。',
      ],
    },
  ],
  english: [
    {
      heading: 'About Me',
      paragraphs: [
        "I am Chi-Shun Liao, holding a Master's degree from the Department of Space Science and Engineering at National Central University. My journey began in academic research—developing image-processing algorithms for solar physics and presenting findings at international conferences including AOGS and JpGU—and has since evolved into hands-on AI engineering. Leadership experience as a basketball team vice-captain also shaped my team-management and communication skills.",
      ],
    },
    {
      heading: 'Professional Experience',
      paragraphs: [
        'In my current role, I work on an AI avatar platform, covering the backend messaging layer and RAG retrieval and integrating lip-sync and TTS. I also evaluate ASR and TTS models, tune inference, fine-tune Taiwanese TTS models, and have submitted a fix to NVIDIA NeMo.',
        'Outside of work, I modularized and tuned an LLM batch data pipeline as freelance work, independently built and maintain a LINE Bot customer-service system for my family business using Google ADK and GCP Cloud Run, and open-sourced ai-config (acg), a cross-tool configuration sync and session-handoff CLI for Claude Code, Codex, and Antigravity, shipped as a single executable with CI on Linux, macOS, and Windows. Earlier, as a key member of the Route Leisure project at TibaMe, I designed core routing algorithms, created a Line Bot interface integrated with LLM-based conversational flows, and led Docker containerization.',
      ],
    },
    {
      heading: 'Closing',
      paragraphs: [
        'My academic training in algorithm development, combined with end-to-end AI delivery experience, prepares me to contribute to teams that value analytical problem-solving and innovation. I look forward to bringing my technical expertise and collaborative mindset to your organization.',
      ],
    },
  ],
}
