# 履歷轉換工具使用說明

本目錄提供兩個實用工具:
1. **html_to_pdf.py** - HTML 轉 PDF
2. **pdf_to_png.py** - PDF 轉 PNG

---

## 🔧 安裝依賴

### HTML → PDF 工具

```bash
# 安裝 Playwright
pip install playwright

# 安裝瀏覽器 (首次使用)
playwright install chromium
```

### PDF → PNG 工具

```bash
# 安裝 Python 套件
pip install pdf2image pillow

# 安裝 poppler (必要)
# Windows (使用 Chocolatey):
choco install poppler

# 或手動下載:
# https://github.com/oschwartz10612/poppler-windows/releases/
# 下載後解壓到 C:\poppler 並加入 PATH
```

---

## 📖 使用方式

### 1. HTML 轉 PDF

#### 基本用法
```bash
# 轉換 resume.html → resume.pdf
python html_to_pdf.py

# 轉換指定文件
python html_to_pdf.py custom.html

# 指定輸出文件名
python html_to_pdf.py resume.html -o 我的履歷.pdf
```

#### 進階選項
```bash
# 不包含背景色 (純白背景)
python html_to_pdf.py resume.html --no-bg

# 首次使用,安裝瀏覽器
python html_to_pdf.py --install
```

---

### 2. PDF 轉 PNG

#### 基本用法
```bash
# 轉換所有頁面
python pdf_to_png.py resume.pdf

# 只轉換第 1 頁
python pdf_to_png.py resume.pdf -p 1

# 轉換多個頁面
python pdf_to_png.py resume.pdf -p 1 2 3
```

#### 調整解析度
```bash
# 螢幕顯示用 (檔案較小)
python pdf_to_png.py resume.pdf -d 150

# 高品質 (適合打印)
python pdf_to_png.py resume.pdf -d 600

# 預設 300 DPI (平衡品質與檔案大小)
python pdf_to_png.py resume.pdf
```

#### 指定輸出
```bash
# 指定輸出目錄
python pdf_to_png.py resume.pdf -o screenshots/

# 自訂文件名前綴
python pdf_to_png.py resume.pdf --prefix CV
# 輸出: CV_page1.png, CV_page2.png...
```

---

## 🎯 完整工作流程

### 履歷更新 → 生成 PDF → 製作截圖

```bash
# 1. 編輯 resume.html
# 2. 轉成 PDF
python html_to_pdf.py resume.html -o 廖啓舜_履歷.pdf

# 3. 製作第一頁截圖 (用於預覽)
python pdf_to_png.py 廖啓舜_履歷.pdf -p 1 -d 200
```

---

## 🐛 常見問題

### HTML → PDF

**Q: 轉換後樣式跑掉?**
- 確保 CSS 是內嵌在 HTML 中
- 檢查是否使用了相對路徑的外部資源

**Q: 提示 "executable doesn't exist"?**
```bash
playwright install chromium
```

### PDF → PNG

**Q: 提示找不到 poppler?**
- Windows: `choco install poppler`
- 或手動下載並加入 PATH

**Q: 圖片太大/太小?**
- 調整 DPI: `-d 150` (小) 或 `-d 600` (大)
- 預設 300 DPI 適合一般使用

**Q: 轉換很慢?**
- 降低 DPI 可提升速度
- 只轉換需要的頁面: `-p 1 2`

---

## 💡 進階技巧

### 批次處理多個文件

```bash
# 轉換目錄下所有 HTML
for file in *.html; do
    python html_to_pdf.py "$file"
done

# 轉換所有 PDF
for file in *.pdf; do
    python pdf_to_png.py "$file" -p 1
done
```

### 快速預覽

```bash
# 生成低解析度預覽圖 (快速)
python pdf_to_png.py resume.pdf -p 1 -d 100 -o preview/
```
