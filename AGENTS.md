# 🤖 Viewpoints AI 代理開發聖經 (Agent Instructions)

這份文件專為 AI 代理（Coding Agents）設計，旨在提供關於 **Viewpoints** 專案的深度架構資訊、開發規範、工具呼叫準則及故障排除指南。

---

## 🏗️ 專案核心架構

Viewpoints 是一個基於資料驅動的「即時影像聚合網頁應用」。

### 1. 數據流向 (Data Flow)
`cameras_database.json` (全域資料庫) ➔ `picker.html` (選取器) ➔ `viewpoints.json` (使用者配置) ➔ `index.html` (渲染引擎)

### 2. 核心元件
- **渲染引擎 (index.html)**: 僅包含 HTML/CSS 結構。
- **邏輯模組 (js/*.js)**: 
  - `app.js`: 主進入點。
  - `config.js`: 配置管理。
  - `ui.js`: 介面操作。
  - `image-loader.js`: 圖片重試載入邏輯。
  - `player.js`: HLS 播放器初始化。
- **選取器 (picker.html)**: 負責過濾資料並產生標準格式的 JSON。支援搜尋、動態分類標籤與自動版面計算。
- **雙模伺服器 (start-server.js)**:
  - **HTTP 模式**: 提供靜態檔案存取 (Port 8848)。
  - **MCP 模式**: 透過標準輸入輸出 (stdio) 為 AI 提供 API 工具。

---

## 📡 MCP 工具與 AI 協作準則

當你作為 AI Agent 運作時，請優先使用以下流程：

### 1. 獲取資訊 (Discovery)
- 使用 `list_cameras` 搜尋特定地點。
- **關鍵準則**: 優先回傳 `id` 供後續操作。

### 2. 視覺分析 (Vision Analysis)
- 使用 `get_camera_image` 獲取 URL。
- **思考邏輯**: "我需要先獲取截圖，再利用我的視覺能力分析畫面中的車流、天氣或人潮。"

### 3. 配置管理 (Configuration)
- 使用 `get_current_config` 了解目前監控牆狀態。
- **重要**: 修改配置後，務必驗證 JSON 格式。

---

## 📜 資料格式規範 (Strict Schema)

為避免出現 `undefined` 或 404 錯誤，所有監控點必須符合以下格式：

### 📷 靜態圖片 (Image Type)
```json
{
  "id": "必填: 唯一識別碼",
  "name": "必填: 顯示名稱",
  "type": "image",
  "imageUrl": "必填: 靜態圖片連結",
  "location": "建議: 地點名稱",
  "category": "必填: 分類標籤"
}
```

### 🎥 YouTube 直播 (YouTube Type)
```json
{
  "id": "唯一碼",
  "name": "名稱",
  "type": "youtube",
  "youtubeId": "必填: 11位元影片ID",
  "category": "分類"
}
```

### 📡 HLS 串流 (HLS Type)
```json
{
  "id": "唯一碼",
  "name": "名稱",
  "type": "hls",
  "hlsUrl": "必填: .m3u8 連結",
  "category": "分類"
}
```

---

## 🎨 界面開發規範 (Frontend Guidelines)

### 1. CSS Grid 佈局
- **規則**: 必須在 `index.html` 的 `<style>` 中定義對應的 `.grid-NxM` 類別。
- **斷點**: 768px 以下自動切換為垂直單欄。
- **效能**: 避免使用 JS 計算高度，優先使用 CSS `vh` 或 `calc()`。

### 2. 圖片快取機制
- **Cache Busting**: 載入圖片時必須附加 `?t=${Date.now()}` 確保抓取最新畫面。
- **錯誤處理**: `tempImg.onerror` 必須提供重試按鈕的 HTML 結構。

---

## 🛠️ 開發常用命令

### 啟動服務 (雙模 - 推薦)
```bash
node start-server.js
```

### 啟動服務 (輕量)
```bash
python3 start-server.py
```

### 資料庫轉換 (簡轉繁)
```bash
python3 convert_to_traditional.py
```

### JSON 驗證
```bash
python3 -m json.tool viewpoints.json
```

---

## 🚨 AI 代理禁忌與原則 (The Golden Rules)

1.  **禁止硬編碼 (No Hardcoding)**: 不要手動將分類標籤寫死在 `picker.html`，請使用 `generateFilterTabs()` 動態生成。
2.  **繁體中文優先 (Traditional Chinese Only)**: 所有 UI 文字、註解與文檔必須使用繁體中文。
3.  **安全性檢查**:
    - HTTP 伺服器嚴禁存取 `..` 上層目錄。
    - 確保 `Access-Control-Allow-Origin: *` 僅用於本地開發環境。
4.  **Git 規範**:
    - 提交前必須更新 `CHANGELOG.md`。
    - 使用 `feat:`, `fix:`, `chore:`, `docs:` 作為提交前綴。
    - 保持提交記錄原子化 (Atomic Commits)。

---

## 🔍 深度調試技巧

1. **影像無法顯示**:
   - 檢查 `viewpoints.json` 類型 (type) 是否與欄位 (imageUrl/youtubeId) 匹配。
   - 檢查瀏覽器控制台 (F12) 是否有 `CORS` 或 `404` 錯誤。
2. **佈局混亂**:
   - 驗證 `document.getElementById('cameraGrid').className` 是否正確獲取了 CSS 類別名。
3. **MCP 故障**:
   - 檢查 `start-server.js` 的 `stderr` 輸出，這是 MCP 的主要日誌通道。

---

## 📈 未來擴充路線圖 (Agent Roadmap)
如果你目前沒有任務，可以考慮提議實作以下功能：
- [ ] **拖曳排序**: 讓 `picker.html` 支援拖曳更換監控點順序。
- [ ] **多重配置**: 支援儲存 `viewpoints_work.json` 或 `viewpoints_travel.json`。
- [ ] **視覺警報**: 透過 MCP 定時截圖並在車流量過大時發出通知。

---
**版本**: 1.2.2
**最後更新**: 2026-01-19
**維護者**: AI Agent Framework
