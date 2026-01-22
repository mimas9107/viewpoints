# Changelog

所有重要的變更都會記錄在此檔案中。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，
版本號遵循 [Semantic Versioning](https://semver.org/zh-TW/)。

---

## [Unreleased] - 技術重點整理與修復

### Added

- **分類藍圖發現工具 (`scraper_blueprint.py`)**
  - 建立網站結構分析工具，自動發現所有監控點分類頁面
  - 支援三種頁面類型偵測：直接列表、按鈕型分頁、分區型分頁
  - 生成完整終點頁面列表，確保不遺漏任何監控點
  - 產生 `scraper_blueprint.json` 包含 80 個終點頁面

- **基於藍圖的爬蟲 (`scraper2.py`)**
  - 使用分類藍圖進行結構化抓取
  - 改進去重機制，防止重複監控點
  - 測試輸出到 `testoutput.json`

### Changed

- **爬蟲架構重構與修復 (`scraper.py`)**
  - 新增版本號管理，與主程式版本同步
  - 改進 HLS 串流提取邏輯，支援多種來源格式
  - 修復動態圖片 URL 處理，移除 `/snapshot` 參數以實現自動更新
  - 改進對於外部播放器監控點的處理策略

### Fixed

- **HLS 串流提取**
  - 支援三種 HLS 來源格式：
    - `<source type="application/x-mpegURL">` 標籤
    - `<iframe src="...live.m3u8">` 元素
    - 外部播放器頁面連結（自動跳過不支援類型）
  - 修復台北市區監控點 HLS URL 提取問題
  - 修復新北市監控點（如 NWT0217）HLS 提取問題

- **動態圖片 URL 處理**
  - 修復台中市監控點不會自動更新的問題
  - 自動移除靜態快照 URL 中的 `/snapshot?t=...` 參數
  - 使用動態圖片端點（如 `https://tcnvr8.taichung.gov.tw/c0415ae1`）

- **分類結構支援**
  - 修復國道總覽頁面無法正確提取子分類的問題
  - 支援台北市、高雄市、台南市等市區的分區結構
  - 支援國道、快速道路的按鈕型分類

- **瀏覽器相容性**
  - Firefox HLS 串流相容性問題（需安裝擴充功能）
  - Chrome 正常顯示 HLS 串流

- **去重機制**
  - 新增 `seen_ids` 集合防止重複監控點
  - 改進爬取效率，減少不必要的重複請求

### Technical Highlights

**問題分析與解決方案**

1. **爬取不完整問題**
   - **原因**：原始 `scraper.py` 無法處理網站的三種頁面結構
   - **解決**：建立 `scraper_blueprint.py` 自動發現所有分類和終點頁面

2. **數據格式落後問題**
   - **原因**：抓取的數據格式不符合新監控牆功能需求
   - **解決**：支援 HLS、YouTube、Image 三種監控點類型

3. **監控點無法自動更新問題**
   - **原因**：靜態快照 URL 不會定期更新
   - **解決**：使用動態圖片端點，移除 `/snapshot` 參數

4. **外部播放器相容性問題**
   - **原因**：部分監控點需要複雜的外部播放器處理
   - **解決**：自動跳過不支援類型，確保監控牆穩定性

### Removed

- 移除對需要外部播放器的監控點的支援（如宜蘭縣部分監控點）
- 這些監控點需要複雜的 AJAX 請求和令牌處理，不適合在監控牆中直接播放

### Documentation

- 更新技術重點整理文檔
- 新增 scraper.py 版本號管理

---

## [2.0.0] - 2026-01-20

### Changed

- **統一伺服器架構 (`start-server-fastapi.py`)**
  - 整合 `start-server.py` 與 `config-server.py` 為單一 FastAPI 伺服器
  - 單一端口 (8844) 提供靜態服務與 Config API
  - 簡化部署與維護流程
  - 移除 `VIEWPOINTS_CONFIG_PORT` 環境變數

- **前端 API URL 整合**
  - `upload.html` 與 `picker.html` 改用相對路徑 `/api/config`
  - 無需區分端口，全部統一透過 FastAPI 伺服器

### Added

- **FastAPI 統一伺服器功能**
  - `GET /api/config` - 讀取配置
  - `POST /api/config` - 儲存配置
  - `GET /api/config/download` - 下載配置
  - `GET /api/config/backups` - 列出備份
  - `POST /api/config/backups/{name}/restore` - 復原備份
  - 自動備份機制（最多保留 10 份）

- **新增依賴套件**
  - `fastapi>=0.109.0`
  - `uvicorn[standard]>=0.27.0`
  - `python-multipart>=0.0.6`

### Removed

- 廢棄 `config-server.py`（功能已整合至 FastAPI 版本）
- 廢棄 `VIEWPOINTS_CONFIG_PORT` 環境變數

### Documentation

- 更新 `README.md` - 新增 FastAPI 統一伺服器說明
- 更新 `QUICKSTART.md` - 簡化啟動指令
- 更新 `PICKER_USAGE.md` - 單一伺服器說明
- 更新 `UPLOAD_USAGE.md` - 單一伺服器說明

---

## [1.3.0] - 2026-01-20

### Added

- **配置 API 管理伺服器 (`config-server.py`)**
  - 新增 REST API 端點支援
  - `GET /api/config` - 讀取配置
  - `POST /api/config` - 儲存配置
  - `GET /api/config/download` - 下載配置
  - `GET /api/config/backup` - 列出備份
  - `GET /api/config/restore/{filename}` - 復原備份
  - 自動備份機制（最多保留 10 份）

- **上傳介面 (`upload.html`)**
  - 圖形化介面上傳自訂 JSON 檔案
  - 支援拖曳上傳
  - 即時顯示目前配置狀態
  - 驗證 JSON 格式

- **環境變數支援**
  - 新增 `.env` 設定檔
  - `VIEWPOINTS_PORT` - 主伺服器連接埠（預設：8844）
  - `VIEWPOINTS_CONFIG_PORT` - 配置伺服器連接埠（預設：8845）

### Changed

- **配置載入優先順序 (`js/config.js`)**
  1. URL 參數 `?configUrl=...`（外部 URL）
  2. API 端點 `/api/config`（config-server.py）
  3. 本地檔案 `./viewpoints.json`（fallback）

- **選擇器新增功能 (`picker.html`)**
  - 新增「儲存到伺服器」按鈕
  - 可直接將配置寫入 viewpoints.json

### Documentation

- 新增 `UPLOAD_USAGE.md` 上傳介面使用說明
- 更新 `README.md` 繁體中文內容
- 更新 `QUICKSTART.md` 繁體中文內容
- 更新 `PICKER_USAGE.md` 說明

### Changed
- **前端樣式分離**：將 `index.html` 中的 CSS 樣式提取至 `css/style.css`。
- 完善專案結構，將樣式與結構分離。

## [1.2.2] - 2026-01-19

### Changed
- **前端邏輯模組化**：將 `index.html` 內部長達 300 行的 JavaScript 拆分至 `js/` 目錄下。
  - `js/config.js`: 配置載入。
  - `js/ui.js`: 介面操作與全螢幕。
  - `js/image-loader.js`: 圖片重試與校驗。
  - `js/player.js`: HLS 播放器。
  - `js/app.js`: 主程式進入點。
- 使用原生 ES Modules (`import/export`)，維持零編譯環境。

## [1.2.1] - 2026-01-19

### Fixed
- **徹底繁體化**：修正了 `index.html`、`start-server.py` 與所有 Markdown 文件中殘留的簡體字（如：墙、自动、开启等）。
- **穩定性提升**：修復了更新時間戳記時可能產生的 `null` 元素參考錯誤。

## [1.2.0] - 2026-01-19

### Added
- **全面擴充爬蟲分類範圍** (`scraper.py`)
  - 新增所有國道 (1-10號)
  - 新增所有快速道路 (台61-88線)
  - 新增各縣市省道與市區路況
  - 新增更多國家公園與風景區
  - 新增氣象署、水利署等其他來源
- **選擇器支援動態分類** (`picker.html`)
  - 自動根據資料庫內容生成篩選標籤
  - 自動統計並顯示每個分類的監控點數量
  - 自動按數量排序分類標籤

### Changed
- 選擇器不再使用硬編碼的分類標籤，改為動態生成，提高了對新資料庫的適應性

## [1.1.1] - 2026-01-19

### Added
- 新增雙向導航功能
  - 主頁面新增「⚙️ 選擇器」按鈕 - 快速訪問監控點選擇器
  - 選擇器頁面新增「🏠 回傳監控牆」按鈕 - 方便回傳主頁面
  - 改善使用者體驗，無需手動輸入 URL

### Fixed
- **修復選擇器篩選功能無法運作的問題**
  - **問題描述：** 篩選標籤（國道、景點、市區等）與資料庫實際分類不比對，導致篩選無效
  - **根本原因：** 資料庫使用具體地點名稱（陽明山、合歡山等），而非大分類
  - **解決方案：** 更新篩選標籤符合資料庫實際分類
  - **新的篩選標籤：** 陽明山、合歡山、阿里山、日月潭、雪霸、北宜、蘇花改、台64線、台61線、新北省道
  - **資料庫統計：** 611 個監控點，涵蓋 10 個主要分類

### Changed
- 優化界面導航流程
- 更新篩選標籤，符合資料庫實際內容

---

## [1.1.0] - 2026-01-19

### Added
- 新增監視器選擇器 (`picker.html`) - 提供圖形化界面選擇監控點
- 新增監控點資料庫 (`cameras_database.json`) - 套件含 10 個精選監控點
- 新增爬蟲程式 (`scraper.py`) - 用於未來擴充資料庫
- 新增選擇器使用說明 (`PICKER_USAGE.md`)
- 新增 CSS 類別 `.grid-2x3` - 支援 2 欄 × 3 列版面設定

### Fixed
- **[重要] 修復靜態圖片監控點無法載入的問題**
  - **問題描述：** 設定檔中的靜態圖片監控點缺少必要欄位（`type` 和 `imageUrl`），導致 JavaScript 嘗試載入 `undefined` URL，產生 HTTP 404 錯誤
  - **影響範圍：** 合歡山武嶺亭、北宜公路石碇、台64線 等靜態圖片監控點
  - **錯誤日誌：**
    ```
    GET /undefined?t=1768804679493 HTTP/1.1" 404 -
    ```
  - **根本原因：** 從 tw.live 複製的設定缺少監控類型判斷和對應的 URL 欄位
  - **解決方案：** 
    1. 為所有靜態圖片監控點新增 `type: "image"` 欄位
    2. 新增 `imageUrl` 欄位，值從 `thumbnail` URL 中提取
    3. 統一補齊 `location`、`category`、`description` 等欄位
  - **修正的監控點：**
    - 合歡山武嶺亭 (`T14A-d61a0c91`)
    - 北宜公路石碇 (`CCTV-11-0090-023-001`)
    - 台64線 (`CCTV-12-0640-023-002`)

### Changed
- 更新 `index.html` - 支援 2x3 網格版面設定
- 更新響應式版面設定 CSS - 套件含 `.grid-2x3` 在手機版適配中

---

## [1.0.0] - 2026-01-19

### Added
- 初始版本發布
- 支援三種監控類型：
  - 靜態圖片 (image)
  - YouTube 直播 (youtube)
  - HLS 串流 (hls)
- 支援網格版面設定：2x2, 3x2, 3x3, 4x3
- 自動/手動重新整理功能
- 全屏查看功能
- JSON 設定檔支援
- Python 和 Node.js 服務器啟動腳本
- 響應式設計（支援手機和電腦）

### Documentation
- 新增 README.md - 完整使用說明
- 新增 QUICKSTART.md - 快速開始指南
- 新增 AGENTS.md - AI Proxy開發指南

---

## 已知問題

### [待修復]
- HLS URL 可能套件含時效性 token，需定期更新
- 部分監控點可能因為來源暫時離線而無法顯示

### [計畫功能]
- [ ] 選擇器新增拖拉排序功能
- [ ] 支援自訂網格版面設定（手動設定欄列數）
- [ ] 預覽縮圖顯示
- [ ] 儲存/載入多組設定
- [ ] 自動爬蟲更新資料庫
- [ ] 資料庫擴充至 1000+ 監控點

---

## 設定檔案格式規範

### 必要欄位說明

為避免 `undefined` 錯誤，請確保所有監控點套件含以下欄位：

#### 靜態圖片 (type: "image")
```json
{
  "id": "唯一ID",
  "name": "監控點名稱",
  "description": "詳細描述",
  "type": "image",           // ← 必須
  "imageUrl": "圖片URL",      // ← 必須
  "location": "地點",
  "category": "分類"
}
```

#### YouTube 直播 (type: "youtube")
```json
{
  "id": "唯一ID",
  "name": "監控點名稱",
  "description": "詳細描述",
  "type": "youtube",         // ← 必須
  "youtubeId": "影片ID",      // ← 必須
  "location": "地點",
  "category": "分類"
}
```

#### HLS 串流 (type: "hls")
```json
{
  "id": "唯一ID",
  "name": "監控點名稱",
  "description": "詳細描述",
  "type": "hls",             // ← 必須
  "hlsUrl": "串流URL",        // ← 必須
  "location": "地點",
  "category": "分類"
}
```

---

## 故障排除

### 監控點無法載入（顯示 404 錯誤）

**症狀：**
- 瀏覽器控制台顯示 `GET /undefined` 錯誤
- 監控畫面顯示「加載失敗」

**診斷：**
```bash
# 檢查設定檔格式
python3 -m json.tool viewpoints.json

# 查看服務器日誌
# 尋找 "404" 和 "undefined" 關鍵字
```

**解決方案：**
1. 檢查所有監控點是否套件含對應類型的 URL 欄位
2. 靜態圖片必須有 `imageUrl`
3. YouTube 必須有 `youtubeId`
4. HLS 必須有 `hlsUrl`
5. 所有監控點必須有 `type` 欄位

**建議：**
- 使用選擇器 (`picker.html`) 自動產生設定，避免手動編輯錯誤
- 手動編輯後務必驗證 JSON 格式

---

## 版本說明

### 版本號格式：主版本.次版本.修訂號

- **主版本：** 不相容的 API 變更
- **次版本：** 向下相容的功能新增
- **修訂號：** 向下相容的問題修正

---

## 貢獻指南

如果你發現新的問題或有改進建議：

1. 記錄問題的完整描述
2. 提供重現步驟
3. 附上錯誤日誌（如果有）
4. 說明預期行為和實際行為
5. 更新此 CHANGELOG.md

---

## 聯絡資訊

- 專案靈感來源：[tw.live](https://tw.live)
- 授權：MIT License
- 版本：2.0.0
- 最後更新：2026-01-20
