# Poppler 手動安裝指南 (Windows)

如果 `choco install poppler` 遇到權限問題,可以手動安裝:

## 📥 下載

1. 前往: https://github.com/oschwartz10612/poppler-windows/releases/
2. 下載最新版本的 **Release-XX.XX.X.zip** (例如 Release-24.08.0.zip)
3. 解壓縮到 `C:\poppler` (或你想要的位置)

## ⚙️ 設定環境變數

### 方法 1: 圖形介面

1. 按 `Win + S` 搜尋「環境變數」
2. 點擊「編輯系統環境變數」
3. 點擊「環境變數」按鈕
4. 在「系統變數」區域找到 `Path`,點擊「編輯」
5. 點擊「新增」,輸入: `C:\poppler\Library\bin`
6. 確定關閉所有視窗

### 方法 2: PowerShell (管理員)

```powershell
# 以系統管理員身分執行 PowerShell
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\poppler\Library\bin",
    "Machine"
)
```

## ✅ 驗證安裝

開啟**新的**終端機視窗,執行:

```bash
pdfinfo -v
```

如果顯示版本號,表示安裝成功!

## 🔧 測試 PDF 轉 PNG

```bash
cd /f/resume
python scripts/pdf_to_png.py --help
```

## ⚠️ 常見問題

### Q: 執行後顯示「找不到 poppler」?
**A:** 確保:
1. 路徑正確: `C:\poppler\Library\bin\pdfinfo.exe` 存在
2. 已將路徑加入環境變數
3. **重新開啟**終端機(環境變數需要重新載入)

### Q: 還是不行?
**A:** 檢查解壓縮的目錄結構應該是:
```
C:\poppler\
  └── Library\
      └── bin\
          ├── pdfinfo.exe
          ├── pdftoppm.exe
          └── ... (其他工具)
```

如果不是這樣,調整解壓縮位置或環境變數路徑。
