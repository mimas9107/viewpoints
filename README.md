# 監視器牆 - 個人化 CCTV 監控面板

基於 tw.live 的客製化監視器牆系統，可透過 JSON 組態檔輕鬆管理您關注的監控點。

## 功能特色

- 支援 2x2、3x2、3x3、4x3 等多種版面設定
- 自動重新整理功能（可自訂重新整理間隔）
- 響應式設計，支援手機和電腦
- 點擊圖片可全螢幕查看
- 透過 JSON 檔案輕鬆設定監控點
- 顯示每個監控畫面的最後更新時間
- 圖形化監控點選擇器 (`picker.html`)
- 圖形化上傳介面 (`upload.html`)
- 設定 API 管理伺服器 (`config-server.py`)
- AI 整合 - 支援 MCP Server，讓 AI 助手幫你分析路況

## 快速開始

### 1. 啟動本機伺服器

由於瀏覽器的安全性限制（CORS），需要透過本機伺服器來執行。

**方法 A：使用 Python（推薦）**

```bash
python3 start-server.py
```

**方法 B：使用 Node.js**

```bash
node start-server.js
```

啟動後，瀏覽器會自動開啟 `http://localhost:8844`，或手動存取該位址。

**自訂連接埠：**

編輯 `.env` 檔案：

```bash
VIEWPOINTS_PORT=8080
VIEWPOINTS_CONFIG_PORT=9000
```

### 2. 修改監控點

**方法一：使用選擇器（推薦）**

1. 開啟 `http://localhost:8844/picker.html`
2. 搜尋並選擇監控點
3. 點擊「儲存到伺服器」直接寫入設定

**方法二：使用上傳介面**

1. 開啟 `http://localhost:8844/upload.html`
2. 選擇或拖曳 JSON 檔案
3. 點擊「上傳並套用配置」

**方法三：手動編輯**

編輯 `viewpoints.json` 檔案來更換您想要監控的地點：

```json
{
  "title": "我的監視器牆",
  "autoRefresh": true,
  "refreshInterval": 60,
  "layout": {
    "columns": 2,
    "rows": 2
  },
  "cameras": [
    {
      "id": "1",
      "name": "監控點名稱",
      "description": "監控點描述",
      "type": "image",
      "imageUrl": "監控圖片URL",
      "location": "地理位置",
      "category": "分類標籤"
    }
  ]
}
```

## 配置管理

### 選擇器 (picker.html)

圖形化介面讓您從資料庫中選擇監控點。

**使用方式：**

1. 開啟 `http://localhost:8844/picker.html`
2. 使用搜尋框或分類標籤篩選
3. 點擊監控點進行選擇
4. 選擇完成後：
   - 點擊「儲存到伺服器」直接套用
   - 點擊「匯出設定」下載 JSON 檔案

**詳細說明：** 參考 [PICKER_USAGE.md](./PICKER_USAGE.md)

### 上傳介面 (upload.html)

上傳自訂的 JSON 設定檔案。

**使用方式：**

1. 開啟 `http://localhost:8844/upload.html`
2. 選擇或拖曳 JSON 檔案
3. 點擊「上傳並套用配置」

**功能：**
- 顯示目前配置狀態
- 驗證 JSON 格式
- 拖曳上傳支援
- 備份目前配置

**詳細說明：** 參考 [UPLOAD_USAGE.md](./UPLOAD_USAGE.md)

### API 管理伺服器

啟動配置管理伺服器：

```bash
python3 config-server.py
```

預設連接埠為 8845，可透過 `.env` 調整。

**API 端點：**

| 方法 | 路徑 | 功能 |
|------|------|------|
| GET | `/api/config` | 讀取目前配置 |
| POST | `/api/config` | 儲存新配置 |
| GET | `/api/config/download` | 下載配置檔案 |
| GET | `/api/config/backup` | 列出備份檔案 |
| GET | `/api/config/restore/{檔名}` | 復原備份 |

**備份機制：**
- 每次儲存配置前會自動備份
- 備份檔案存放於 `.backups/` 目錄
- 最多保留 10 份備份

## 如何取得監控器 URL

### 方法 1：靜態圖片監控器

從 tw.live 網站取得靜態監控畫面：

1. 存取 https://tw.live/
2. 找到您想要的監控點（例如：國道一號、陽明山等）
3. 在監控畫面上**右鍵點擊** → 選取「在新標籤頁中開啟圖片」
4. 複製瀏覽器位址欄中的 URL
5. 將這個 URL 填入 `viewpoints.json` 的 `imageUrl` 欄位

**設定範例：**

```json
{
  "id": "1",
  "name": "國道一號三重段",
  "type": "image",
  "imageUrl": "https://cctv1.freeway.gov.tw/abs2jpg.php?sn=1040-S-05.2-M",
  "location": "新北市三重區",
  "category": "國道"
}
```

### 方法 2：YouTube 直播監控器

從 tw.live 網站取得 YouTube 直播：

1. 存取 https://tw.live/
2. 找到有 YouTube 直播的監控點
3. 在頁面上找到 YouTube 播放器
4. **右鍵點擊播放器** → 選取「複製影片網址」
5. 從網址中提取影片 ID（例如：`https://www.youtube.com/watch?v=RttyIGHbN_w` 中的 `RttyIGHbN_w`）
6. 將影片 ID 填入組態檔

**設定範例：**

```json
{
  "id": "2",
  "name": "陽明書屋台北盆地",
  "description": "陽明山國家公園 YouTube 直播",
  "type": "youtube",
  "youtubeId": "RttyIGHbN_w",
  "location": "台北市北投區",
  "category": "景點"
}
```

**YouTube 直播特點：**
- 即時影像串流，無需重新整理
- 自動播放（靜音模式）
- 帶有紅色 "LIVE" 標誌
- 可以點擊播放器控制播放

### 方法 3：HLS (M3U8) 串流監控器

從 tw.live 網站取得 HLS 串流：

1. 存取 https://tw.live/
2. 找到使用 HLS 串流的監控點
3. 按 **F12** 開啟開發者工具
4. 切換到「Network」（網路）標籤頁
5. 在篩選器中輸入 `.m3u8` 或 `m3u8`
6. 重新整理頁面，找到類似的 `live.m3u8` 請求
7. 右鍵點擊請求 → 「Copy」 → 「Copy URL」
8. 將完整 URL 填入組態檔

**設定範例：**

```json
{
  "id": "3",
  "name": "市府路松壽路口",
  "description": "台北市信義區 HLS 串流",
  "type": "hls",
  "hlsUrl": "https://jtmctrafficcctv2.gov.taipei/NVR/de868bf6-b954-447d-8c11-c5348092a1aa/live.m3u8",
  "location": "台北市信義區",
  "category": "市區"
}
```

**HLS 串流特點：**
- 高品質即時影像串流
- 自動播放（靜音模式）
- 帶有藍色 "HLS LIVE" 標誌
- 支援播放控制和全螢幕
- 適用於台北市政府等提供的監控點

## 設定說明

### 基本設定

| 欄位 | 說明 | 範例值 |
|------|------|--------|
| `title` | 頁面標題 | "我的監視器牆" |
| `autoRefresh` | 是否自動重新整理 | `true` 或 `false` |
| `refreshInterval` | 重新整理間隔（秒） | `60` |

### 版面設定

| 版面設定 | columns | rows | 總監控數 |
|----------|---------|------|----------|
| 2x2 四宮格 | 2 | 2 | 4 |
| 3x2 六宮格 | 3 | 2 | 6 |
| 3x3 九宮格 | 3 | 3 | 9 |
| 4x3 十二宮格 | 4 | 3 | 12 |

### 攝影機設定

每個攝影機需要包含以下欄位：

**靜態圖片監控器（預設）：**

```json
{
  "id": "唯一識別符",
  "name": "顯示名稱",
  "description": "詳細描述",
  "type": "image",
  "imageUrl": "圖片 URL",
  "location": "地理位置",
  "category": "分類標籤（國道/省道/市區/景點）"
}
```

**YouTube 直播監控器：**

```json
{
  "id": "唯一識別符",
  "name": "顯示名稱",
  "description": "詳細描述",
  "type": "youtube",
  "youtubeId": "YouTube 影片 ID",
  "location": "地理位置",
  "category": "分類標籤（國道/省道/市區/景點）"
}
```

**HLS/M3U8 串流監控器：**

```json
{
  "id": "唯一識別符",
  "name": "顯示名稱",
  "description": "詳細描述",
  "type": "hls",
  "hlsUrl": "HLS 串流 URL（.m3u8）",
  "location": "地理位置",
  "category": "分類標籤（國道/省道/市區/景點）"
}
```

**欄位說明：**
- `type`: 監控器類型
  - `image` 或省略：靜態圖片（需要定期重新整理）
  - `youtube`：YouTube 直播（即時串流）
  - `hls`：HLS/M3U8 串流（即時串流）
- `imageUrl`: 仅用於 `type: "image"`，靜態圖片的 URL
- `youtubeId`: 仅用於 `type: "youtube"`，YouTube 影片的 ID
- `hlsUrl`: 仅用於 `type: "hls"`，M3U8 串流的完整 URL

## 操作說明

### 手動重新整理

點擊頁面右上角的「重新整理」按鈕可立即更新所有監控畫面。

### 自動重新整理

- 點擊「啟用自動重新整理」按鈕開啟自動重新整理
- 重新整理間隔可在 `viewpoints.json` 中的 `refreshInterval` 設定（單位：秒）
- 點擊「停止自動重新整理」可以關閉

### 全螢幕查看

- 點擊任何監控畫面可以全螢幕查看
- 按 ESC 鍵或點擊右上角的 X 關閉全螢幕

## 常見問題

### Q：顯示「CORS 請求未使用 http 通訊協定」錯誤？

A：這是瀏覽器的安全性策略。**不要直接雙擊開啟 HTML 檔案**，必須透過本機伺服器執行：

```bash
python3 start-server.py
```

### Q：監控畫面顯示「載入失敗」？

A：可能的原因：
1. 監控器 URL 不正確
2. 該監控點暫時離線
3. 網路連線問題

解決方法：點擊錯誤提示可重新載入，或到 tw.live 確認該監控點是否正常。

### Q：如何找到 HLS 串流的 M3U8 URL？

A：有兩種方法：

**方法 1：使用開發者工具（推薦）**
1. 存取 tw.live 上的監控頁面
2. 按 **F12** 開啟開發者工具
3. 切換到 **Network**（網路）標籤頁
4. 在篩選器中輸入 `m3u8`
5. 重新整理頁面
6. 找到 `live.m3u8` 的請求
7. 右鍵 → Copy → Copy URL
8. 貼上到組態檔的 `hlsUrl` 欄位

**方法 2：查看頁面原始碼**
1. 在監控頁面上右鍵 →「查看網頁原始碼」
2. 按 Ctrl+F 搜尋 `.m3u8`
3. 找到完整的 URL（通常在 `<source src="...">` 標籤中）
4. 複製完整 URL

**常見 HLS URL 格式：**
- 台北市：`https://jtmctrafficcctv2.gov.taipei/NVR/[UUID]/live.m3u8`
- 其他縣市可能有不同格式

### Q：HLS 串流和 YouTube 直播有什麼區別？

A：
- **HLS 串流：**
  - 來自政府機關的監控系統（如台北市交通局）
  - 使用 M3U8 格式
  - 需要 Video.js 播放器
  - 通常延遲較低
  - 藍色 "HLS LIVE" 標誌

- **YouTube 直播：**
  - 來自 YouTube 平台
  - 使用 YouTube 嵌入式播放器
  - 可能有廣告
  - 紅色 "LIVE" 標誌

### Q：為什麼 HLS 串流無法播放？

A：可能的原因：
1. **URL 過期**：某些 HLS URL 包含時效性 token，需要重新取得
2. **網路限制**：某些串流可能有地理或網路限制
3. **瀏覽器不支援**：建議使用 Chrome、Firefox 或 Edge 最新版本

解決方法：
- 重新從 tw.live 取得最新的 M3U8 URL
- 檢查瀏覽器控制台（F12）的錯誤資訊
- 確認本機伺服器正常執行

### Q：如何找到 YouTube 直播的影片 ID？

A：有兩種方法：
1. **從播放器取得**：在 YouTube 播放器上右鍵 →「複製影片網址」→ 從 URL 中提取 ID
   - 範例 URL：`https://www.youtube.com/watch?v=RttyIGHbN_w`
   - 影片 ID：`RttyIGHbN_w`（`v=` 後面的部分）

2. **從 tw.live 頁面原始碼取得**：按 F12 → 搜尋 `youtube.com/embed/` → 複製 ID
   - 範例：`youtube.com/embed/RttyIGHbN_w`
   - 影片 ID：`RttyIGHbN_w`

### Q：YouTube 直播會自動重新整理嗎？

A：不需要！YouTube 直播是即時影像串流，會持續播放，無需重新整理。自動重新整理功能僅對靜態圖片監控器有效。

### Q：可以同時使用靜態圖片、YouTube 和 HLS 嗎？

A：可以！您可以在同一個監視器牆中混合使用三種類型。

### Q：如何找到更多監控點？

A：存取 https://tw.live/ 瀏覽以下分類：
- 國道路況：國道一號～十號
- 省道路況：各縣市省道
- 市區路況：六都市區道路
- 旅遊景點：合歡山、陽明山、阿里山等
- 國家公園：雪霸、玉山、太魯閣等

### Q：可以監控幾個地點？

A：建議根據螢幕大小選取：
- 電腦大螢幕：4-12 個（2x2 到 4x3）
- 筆記型電腦：4-6 個（2x2 或 3x2）
- 手機：2-4 個

### Q：重新整理間隔設定多少比較好？

A：建議設定：
- 路況監控：30-60 秒
- 景點天氣：60-120 秒
- 避免設定太短（<30秒），以免給伺服器造成負擔

## AI 整合 (MCP Server)

Viewpoints 內建 **MCP (Model Context Protocol) Server**，可以將監視器資料連線到 Claude Desktop 或其他 AI 助手。

### 特色功能

- **智能查詢**：讓 AI 幫你搜尋監視器（例：「林口路段現在塞車嗎？」）
- **視覺分析**：AI 可以獲取監視器截圖，直接分析畫面中的車流、天氣
- **自然語言**：用日常對話的方式與 AI 討論路況

### 設定方式

請參考 [MCP_GUIDE.md](./MCP_GUIDE.md) 完整教學。

## 技術說明

- 純前端實作，無需後端伺服器
- 使用原生 JavaScript，無外部相依
- 響應式 CSS Grid 版面設定
- 支援所有現代瀏覽器

## 授權與宣告

本專案僅為個人學習和使用目的。監控畫面版權歸原提供方所有。

**影像來源：**
- 交通部高速公路局
- 公路總局
- 各縣市政府
- 國家公園管理處
- tw.live 網站

## 更新日誌

請參考 [CHANGELOG.md](./CHANGELOG.md)
