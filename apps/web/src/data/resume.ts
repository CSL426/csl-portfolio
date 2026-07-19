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
  tools: ['Python、PyTorch', 'FastAPI、RESTful API', 'React、Vue', 'RAG、MongoDB', 'Linux、Git、Docker', 'GCP、AWS', 'ETL Pipeline'],
  experiences: [
    {
      title: 'AI 工程師｜創造智能（2025/4 - 至今）',
      bullets: [
        '多項 AI 開源專案二次開發與客製化,快速交付 POC/MVP;開發 AI 虛擬人應用,串接對嘴(lip-sync)、TTS 與知識庫大腦。',
        '建置 RAG 知識庫系統與管理後台，優化高併發與檢索準確度；該產品已成功導入 4 家企業客戶。',
        'FastAPI 開發 RESTful API、MongoDB 資源管理；React/Vue 管理後台獲採用為公司開發範本。',
        '台語 TTS 模型 finetune 與資料前處理；ETL 數據 pipeline 與資料清洗。',
      ],
    },
    {
      title: '個人專案與接案 - AI 客服 / 知識庫系統',
      bullets: [
        '自主架設家業 LINE Bot AI 客服系統，以 Google ADK 開發 AI Agent 並整合知識庫；獨立完成架構設計、GCP Cloud Run 部署與維運。',
        '接案協助地方單位開發 LINE OA 知識庫 AI Agent 系統。',
      ],
    },
    {
      title: 'TibaMe - AI 應用開發培訓(專案 - 路遊憩)',
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
    '具備 AI 應用端到端交付能力：從模型微調、量化與 vLLM 推論優化，到 RAG 系統、FastAPI 後端、React/Vue 前端與 GCP 雲端部署，能獨立完成完整的開發與交付流程。',
    '太空科學碩士出身，擅長演算法設計與大規模數據處理，研究成果於三場國際研討會發表；習慣以數據驗證與快速迭代交付 MVP。',
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
        '在前一份工作期間，我主導了多個 AI/LLM 與多媒體專案的開發與部署。其中最具代表性的成果是從零建置 RAG 知識庫系統，優化高併發處理與檢索準確度，並串接對嘴（Lip-sync）模型實現 AI 虛擬人即時互動（該產品已成功導入 4 家企業客戶）；此外，我亦導入 vLLM 加速語音合成（TTS）與其他開源模型的推理速度，並以 React/Vue 開發後台管理介面（交付客戶並建立為公司內部專案的開發標準範本）。在工作之外，我基於 Google ADK 與 GCP Cloud Run，為家族事業獨立研發並維運 LINE Bot 智慧客服系統。這些實戰經驗培養了我端到端（End-to-End）交付 AI 應用與解決複雜問題的能力，期盼能為貴團隊帶來實質貢獻。',
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
        'In my previous role, I built a RAG knowledge-base system from scratch: optimizing high-concurrency handling and retrieval accuracy, accelerating inference with vLLM, and integrating a Lip-sync model for real-time AI avatar interactions. I also developed the administrative console in React/Vue, which was delivered to clients and adopted as the company boilerplate.',
        'Outside of work, I independently built and maintain a smart LINE Bot customer-service system for my family business using Google ADK and GCP Cloud Run. Earlier, as a key member of the Route Leisure project at TibaMe, I designed core routing algorithms, created a Line Bot interface integrated with LLM-based conversational flows, and led Docker containerization.',
      ],
    },
    {
      heading: 'Closing',
      paragraphs: [
        'My academic training in algorithm development, combined with end-to-end full-stack AI experience, prepares me to contribute to teams that value analytical problem-solving and innovation. I look forward to bringing my technical expertise and collaborative mindset to your organization.',
      ],
    },
  ],
}
