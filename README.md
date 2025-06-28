# Semantic Blog Importer 🚀

將 WordPress / Notion 匯出的內容轉換為語意化的 Markdown 結構，適合發佈至 GitHub Pages 或靜態網站平台（如 Super / Potion / Vercel）。

---

## 📦 專案結構

- `setup_repo.sh`：一鍵推送到 GitHub 的初始化腳本
- `blog_loader/`：載入器，支援 Notion 匯出轉換
- `run_all.py`：主流程，一鍵處理匯入與匯出
- `assets/`：封面與素材圖像
- `docs/`：靜態網站展示（支援 GitHub Pages）

---

## 🚀 使用方法

1. 將 Notion 或 WordPress 匯出檔放入 `input/` 資料夾
2. 執行 `run_all.py`
3. 調整 `docs/index.md` 與封面，即可發佈展示站

---

## 📘 授權與版本

MIT License | 建立者：Eric  
Powered by Copilot Semantic Stack 🧠
