# 監視器牆 - 快速開始

## 一分鐘快速啟動

### 1. 啟動伺服器

```bash
cd viewpoints
python3 start-server.py
```

瀏覽器會自動開啟 `http://localhost:8844`

### 2. 停止伺服器

按 `Ctrl+C` 即可停止

## 檔案說明

```
viewpoints/
├── index.html              # 主頁面
├── viewpoints.json         # 組態檔（可隨時修改）
├── picker.html             # 監控點選擇器
├── upload.html             # 上傳組態介面
├── config-server.py        # 配置管理伺服器
├── start-server.py         # Python 伺服器啟動指令碼
├── start-server.js         # Node.js 伺服器啟動指令碼
├── cameras_database.json   # 監控點資料庫
├── .env                    # 環境變數設定
├── README.md              # 完整使用說明
├── QUICKSTART.md          # 本檔案
└── PICKER_USAGE.md        # 選擇器使用說明
```

## 修改監控點

### 方法一：使用選擇器（推薦）

1. 開啟 `http://localhost:8844/picker.html`
2. 搜尋並選擇監控點
3. 點擊「儲存到伺服器」

### 方法二：使用上傳介面

1. 開啟 `http://localhost:8844/upload.html`
2. 選擇或拖曳 JSON 檔案
3. 點擊「上傳並套用配置」

### 方法三：手動編輯

編輯 `viewpoints.json` 檔案，修改其中的監控點資訊。

## 三種監控類型

### 1. 靜態圖片（預設）

```json
{
  "name": "監控點名稱",
  "type": "image",
  "imageUrl": "https://example.com/image.jpg",
  "location": "地點",
  "category": "分類標籤"
}
```

### 2. YouTube 直播

```json
{
  "name": "監控點名稱",
  "type": "youtube",
  "youtubeId": "影片ID",
  "location": "地點",
  "category": "分類標籤"
}
```

### 3. HLS 串流

```json
{
  "name": "監控點名稱",
  "type": "hls",
  "hlsUrl": "https://example.com/stream.m3u8",
  "location": "地點",
  "category": "分類標籤"
}
```

## 自訂連接埠

編輯 `.env` 檔案：

```bash
VIEWPOINTS_PORT=8080
VIEWPOINTS_CONFIG_PORT=9000
```

## 常見問題

### Q：頁面顯示「無法載入組態檔」？

A：確保您是透過 `python3 start-server.py` 啟動的，而不是直接雙擊開啟 HTML 檔案。

### Q：如何更改版面設定？

A：編輯 `viewpoints.json` 中的 `layout` 欄位：

```json
"layout": {
  "columns": 2,  // 欄數
  "rows": 2      // 列數
}
```

### Q：如何找到監控點 URL？

A：存取 https://tw.live/ 找到監控點，詳細方法請看 README.md

### Q：選擇器或上傳頁面無法開啟？

A：確保 config-server.py 也在執行：

```bash
# 終端機 1：啟動主伺服器
python3 start-server.py

# 終端機 2：啟動配置伺服器
python3 config-server.py
```

## 更多資訊

詳細使用說明請參考 [README.md](README.md)
