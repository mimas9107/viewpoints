# 🤖 Viewpoints AI 代理開發聖經 (Agent Instructions)

這份文件專為 AI 代理（Coding Agents）設計，旨在提供關於 **Viewpoints** 專案的深度架構資訊、開發規範、工具呼叫準則及故障排除指南。

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
- `config-server.py`: 配置管理伺服器 (Port 8845)。[ v1.x.y版本 ]
- `start-server.py`: Python HTTP 伺服器 (Port 8844)。[ v1.x.y版本 ]
- `start-server-fastapi.py`: Python HTTP 伺服器（Port 8844）[ >=v2.0.0版本 ]
- `start-server.js`: 雙模伺服器 (HTTP + MCP)。[ v1.x.y版本 ]
- `.env`: 環境變數設定檔。
- `.backups/`: 自動備份目錄。
- `scraper.py`: 主要爬蟲程式，使用預定義的分類列表進行抓取成"全域資料庫"用途。`v2.0.1`
- `scraper2.py`: 使用分類藍圖進行測試抓取成測試資料庫比對用途，須與scraper_blueprint.py搭配使用。`v2.0.1`
- `scraper_blueprint.py`: 分類發現工具，遍歷全站並收集所有監控點分類頁面。`v2.0.1`
- `SCRAPER.md`: 爬蟲使用指南，包含技術重點整理、方法文件、故障排除指南。

### 3. 核心元件
- **渲染引擎 (index.html)**: 僅包含 HTML 結構。
- **樣式模組 (css/*.css)**: 負責介面視覺外觀。
- **邏輯模組 (js/*.js)**: 
  - `app.js`: 主進入點。
  - `config.js`: 配置管理。
  - `ui.js`: 介面操作。
  - `image-loader.js`: 圖片重試載入邏輯。
  - `player.js`: HLS 播放器初始化。
- **選取器 (picker.html)**: 負責過濾資料並產生標準格式的 JSON。支援搜尋、動態分類標籤與自動版面計算。
- **雙模伺服器 (start-server.js)**:
   - **HTTP 模式**: 提供靜態檔案存取 (Port 由 `.env` 設定，預設 8844)。
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

## 📜 資料格式規範 (Strict Schema v2.0.1)

為避免出現 `undefined` 或 404 錯誤，所有監控點必須符合以下格式：

### 📷 靜態圖片 (Image Type)
```json
{
  "id": "必填: 唯一識別碼",
  "name": "必填: 顯示名稱",
  "type": "image",
  "imageUrl": "必填: 動態圖片連結",
  "location": "建議: 地點名稱",
  "category": "必填: 分類標籤",
  "thumbnail": "縮圖連結 (選填)"
}
```

**v2.0.1 更新**：
- `imageUrl` 現在移除 `/snapshot` 參數以實現自動更新
- 使用動態圖片端點（如 `https://tcnvr8.taichung.gov.tw/c0415ae1`）
- 確保圖片會定期更新而不需要手動刷新

### 🎥 YouTube 直播 (YouTube Type)
```json
{
  "id": "唯一碼",
  "name": "名稱",
  "type": "youtube",
  "youtubeId": "必填: 11位元影片ID",
  "category": "分類",
  "thumbnail": "縮圖連結"
}
```

### 📡 HLS 串流 (HLS Type)
```json
{
  "id": "唯一碼",
  "name": "名稱",
  "type": "hls",
  "hlsUrl": "必填: .m3u8 連結",
  "category": "分類",
  "thumbnail": "縮圖連結"
}
```

**v2.0.1 更新**：
- 支援三種 HLS 來源格式：
  - `<source type="application/x-mpegURL">` 標籤
  - `<iframe src="...live.m3u8">` 元素
  - 外部播放器頁面連結（如需要複雜 token 處理，將自動跳過）
- 修復台北市區監控點（如信義區、松山區等）HLS 提取問題
- 修復新北市監控點（如 NWT0217 樹林區）HLS 提取問題
- 自動跳過需要複雜外部播放器的監控點（如宜蘭縣部分監控點）

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

### 啟動配置管理伺服器 (需要上傳/儲存功能時)
```bash
python3 config-server.py
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

## 📋 文件更新追蹤清單 (Document Update Checklist)

當進行程式碼變更時，必須同步更新以下文件。請依變更類型勾選並更新對應文件：

### 必備文件更新清單

| 變更類型 | 需要更新的文件 | 更新時機 |
|----------|----------------|----------|
| **新功能上線** | `CHANGELOG.md`, `README.md` | 功能完成後 |
| **使用者介面變更** | `README.md`, `QUICKSTART.md` | UI 調整後 |
| **新增/修改 API** | `README.md`, `UPLOAD_USAGE.md` | API 變更後 |
| **選取器功能變更** | `PICKER_USAGE.md`, `README.md` | picker.html 修改後 |
| **上傳功能變更** | `UPLOAD_USAGE.md`, `README.md` | upload.html 修改後 |
| **伺服器變更** | `README.md`, `QUICKSTART.md` | start-server.py 或 config-server.py 修改後 |
| **環境變數變更** | `README.md`, `QUICKSTART.md`, `.env.example` | PORT 或環境變數調整後 |

### 文件更新檢查清單

提交程式碼前，請確認以下文件已同步更新：

- [ ] `CHANGELOG.md` - 新增版本紀錄
- [ ] `README.md` - 更新功能說明與操作流程
- [ ] `QUICKSTART.md` - 更新快速開始指令
- [ ] `PICKER_USAGE.md` - 更新選擇器操作說明（如有變更）
- [ ] `UPLOAD_USAGE.md` - 更新上傳介面說明（如有變更）
- [x] `SCRAPER.md` - 更新爬蟲使用指南（新增 v2.0.1 技術重點整理）

### 文件更新原則

1. **CHANGELOG.md**:
   - 使用 `[Unreleased]` 區塊記錄即將發布的變更
   - 發布版本時移動到正式版本區塊
   - 格式：`## [版本號] - YYYY-MM-DD`

2. **README.md**:
   - 保持「功能特色」與實際功能一致
   - 更新「使用流程」說明
   - 新增或修正「常見問題」

3. **QUICKSTART.md**:
   - 保持指令正確性
   - 反映預設連接埠設定

4. **使用說明文件 (PICKER_USAGE.md, UPLOAD_USAGE.md)**:
   - 介面變更時同步更新截圖或操作說明
   - 新增功能時補充使用範例

### 版本號管理原則

| 變更類型 | 版本號遞增 |
|----------|------------|
| 新增功能 | 次版本 (+0.1.0) |
| 修正問題 | 修訂號 (+0.0.1) |
| 不相容變更 | 主版本 (+1.0.0) |
| 文件更新 | 視情況遞增 |

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

## 📈 爬蟲技術重點 (Scraper Highlights)

### v2.0.1 修復內容

1. **分類藍圖系統 (`scraper_blueprint.py`)**
   - 自動發現所有監控點分類頁面
   - 支援三種頁面類型偵測：直接列表、按鈕型分頁面、分區型分頁面
   - 生成完整終點頁面列表 (80 個終點)
   - 產生 `scraper_blueprint.json` 分類藍圖

2. **爬蟲架構重構與修復 (`scraper.py`)**
   - 新增版本號管理，與主程式版本同步 (v2.0.1)
   - 改進 HLS 串流提取邏輯，支援多種來源格式
   - 修復動態圖片 URL 處理，移除 `/snapshot` 參數實現自動更新
   - 支援三種監控點類型：image（動態）、hls（串流）、youtube（直播）
   - 新增去重機制 (`seen_ids` 集合) 防止重複監控點
   - 支援外部播放器相容性處理，自動跳過不支援的監控點

3. **基於藍圖的測試爬取 (`scraper2.py`)**
   - 使用分類藍圖進行結構化抓取
   - 改進監控點提取邏輯
   - 測試輸出到 `testoutput.json`

4. **技術文件更新 (`SCRAPER.md`)**
   - 新增完整的爬蟲使用指南
   - 包含技術重點整理、方法文件、故障排除指南
   - 詳細記錄版本變更和問題解決方案

### 核心技術問題解決

1. **爬取不完整問題**
   - 原因：原始 `scraper.py` 無法處理網站的三種頁面結構
   - 解決：建立 `scraper_blueprint.py` 自動發現所有分類和終點頁面

2. **資料庫格式落後問題**
   - 原因：抓取的數據格式不符合新版監控牆功能需求
   - 解決：支援 HLS、YouTube、Image 三種監控點類型

3. **監控點無法自動更新問題**
   - 原因：靜態快照 URL 不會定期更新
   - 解決：使用動態圖片端點，移除 `/snapshot` 參數

4. **外部播放器相容性問題**
   - 原因：部分監控點需要複雜的外部播放器處理
   - 解決：自動跳過不支援類型，確保監控牆穩定性

---

## 📈 未來擴充路線圖 (Agent Roadmap)
- [ ] **拖曳排序**: 讓 `picker.html` 支援拖曳更換監控點順序。
- [ ] **多重配置**: 支援儲存 `viewpoints_work.json` 或 `viewpoints_travel.json`。
- [ ] **視覺警報**: 透過 MCP 定時截圖並在車流量過大時發出通知。
---

**版本**: 2.0.1
**最後更新**: 2026-01-23
**維護者**: AI Agent Framework

**v2.0.1 更新內容**：
- 爬蟲系統重構與修復
- 新增分類藍圖發現與測試工具
- 改進 HLS 串流提取邏輯
- 修復動態圖片 URL 處理
- 完善技術文件與使用指南

---