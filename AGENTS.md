---
name:          "AGENTS.md"
description:   "Viewpoints 專案開發聖經 — 即時影像聚合架構與 MCP 工具準則"
created_date:  "2026/05/29 13:25:00"
modified_date: "2026/06/18 10:30:00"
project_version: "2.2.4"
document_version: "1.0.0"
agent_sign: ['human/mimas', 'gemini cli/gemini-cli']
---

# 🤖 Viewpoints AI 代理開發聖經 (AGENTS.md)

本文件定義 Viewpoints 專案的深度架構資訊。Agent 必須同時遵循工作區全域規範 (`../AGENTS.md`)。

---

## 🏗️ 專案核心架構

Viewpoints 是一個基於資料驅動的「即時影像聚合網頁應用」。

### 1. 數據流向 (Data Flow)
`cameras_database.json` (全域資料庫) ➔ `picker.html` (選取器) ➔ `viewpoints.json` (使用者配置) ➔ `index.html` (渲染引擎)
`upload.html` (上傳介面) ➔ `config-server.py` (API) ➔ `viewpoints.json` (使用者配置)

### 2. 目錄結構 (Directory Structure)
- `index.html`: 主監控牆。
- `picker.html`: 監控點選取器。
- `upload.html`: 配置上傳介面。
- `css/`: 樣式表目錄。
- `js/`: 邏輯模組目錄。
- `viewpoints.json`: 當前配置檔。
- `cameras_database.json`: 全域監控點資料庫。
- `config-server.py`: 配置管理伺服器 (Port 8845)。
- `start-server-fastapi.py`: Python HTTP 伺服器 (Port 8844)。
- `.env`: 環境變數設定檔。
- `scraper.py`: 主要爬蟲程式 v2.2.4。

### 3. 核心元件
- **渲染引擎 (index.html)**: 僅包含 HTML 結構。
- **邏輯模組 (js/*.js)**: `app.js`, `config.js`, `ui.js`, `image-loader.js`, `player.js`。
- **雙模伺服器 (start-server.js)**: 提供 HTTP 與 MCP 模式。

---

## 📡 MCP 工具與 AI 協作準則

當你作為 AI Agent 運作時，請優先使用以下流程：

### 1. 獲取資訊 (Discovery)
- 使用 `list_cameras` 搜尋特定地點，優先回傳 `id`。

### 2. 視覺分析 (Vision Analysis)
- 使用 `get_camera_image` 獲取 URL 後進行車流、天氣或人潮分析。

### 3. 配置管理 (Configuration)
- 使用 `get_current_config` 了解狀態，修改後務必驗證 JSON 格式。

---

## 📜 資料格式規範 (Strict Schema v2.2.4)

### 📷 靜態圖片 (Image Type)
- `imageUrl` 移除 `/snapshot` 以實現自動更新。

### 🎥 YouTube 直播 (YouTube Type)
- 必填 11 位元 `youtubeId`。

### 📡 HLS 串流 (HLS Type)
- 支援三種來源格式提取，修復台北/新北 HLS 抓取問題。

---
*註：本文件專注於 Viewpoints 影像處理邏輯，通用環境指令請查閱全域規範。*
