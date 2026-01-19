# 監視器墙 - 快速開始

## 一分鐘快速啟動

### 1. 啟動伺服器

```bash
cd viewpoints
python3 start-server.py
```

浏览器会自动打开 `http://localhost:8000`

### 2. 停止伺服器

按 `Ctrl+C` 即可停止

## 檔案說明

```
viewpoints/
├── index.html              # 主页面
├── viewpoints.json         # 組態檔（可随时修改）
├── start-server.py         # Python 伺服器啟動指令碼
├── start-server.js         # Node.js 伺服器啟動指令碼
├── README.md              # 完整使用說明
└── QUICKSTART.md          # 本檔案
```

## 修改監控点

编辑 `viewpoints.json` 檔案，修改其中的監控点資訊。

### 三种監控類型

#### 1. 靜態圖片（預設）
```json
{
  "name": "監控点名称",
  "imageUrl": "https://example.com/image.jpg",
  "location": "地点",
  "category": "分類別"
}
```

#### 2. YouTube 直播
```json
{
  "name": "監控点名称",
  "type": "youtube",
  "youtubeId": "影片ID",
  "location": "地点",
  "category": "分類別"
}
```

#### 3. HLS 串流
```json
{
  "name": "監控点名称",
  "type": "hls",
  "hlsUrl": "https://example.com/stream.m3u8",
  "location": "地点",
  "category": "分類別"
}
```

## 常见问题

### Q: 页面顯示"无法載入組態檔"？
A: 确保您是通过 `python3 start-server.py` 啟動的，而不是直接双击打开 HTML 檔案。

### Q: 如何更改版面設定？
A: 编辑 `viewpoints.json` 中的 `layout` 字段：
```json
"layout": {
  "columns": 2,  // 列数
  "rows": 2      // 行数
}
```

### Q: 如何找到監控点 URL？
A: 存取 https://tw.live/ 找到監控点，详细方法请看 README.md

## 更多資訊

详细使用說明请参考 [README.md](README.md)
