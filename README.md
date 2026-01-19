# 監視器墙 - 個人化 CCTV 監控面板

基於 tw.live 的客制化監視器墙系统，可透過 JSON 組態檔輕鬆管理您關注的監控点。

## 功能特色

- 🎯 2x2 四宮格版面設定（可擴展到 3x2、3x3、4x3）
- 🔄 自動重新整理功能（可自訂重新整理間隔）
- 📱 回應式設計，支援手機和電腦
- 🖼️ 點擊圖片可全螢幕查看
- ⚙️ 透過 JSON 檔案輕鬆設定監控点
- ⏰ 顯示每个監控畫面的最后更新時間
- 🤖 **AI 整合** - 支援 MCP Server，让 AI 助手帮你分析路况

## 🤖 AI 整合 (MCP Server)

Viewpoints 内建 **MCP (Model Context Protocol) Server**，可以将監視器資料連線到 Claude Desktop 或其他 AI 助手。

### 特色功能

- **智能查詢**：讓 AI 幫你搜尋監視器（例：「林口路段現在塞車嗎？」）
- **視覺分析**：AI 可以獲取監視器截圖，直接分析畫面中的車流、天氣
- **自然語言**：用日常對話的方式與 AI 討論路況

### 設定方式

請參考 [MCP_GUIDE.md](./MCP_GUIDE.md) 完整教學。

## 快速開始

### 1. 啟動本機伺服器

由于浏览器的安全性限制（CORS），需要透過本機伺服器来執行。

**方法 A: 使用 Python（推荐）**

```bash
# 直接執行啟動指令碼
python3 start-server.py

# 或使用 Python 内置伺服器
python3 -m http.server 8000
```

**方法 B: 使用 Node.js**

```bash
node start-server.js
```

**方法 C: 使用其他工具**

如果您安装了其他工具：
```bash
# 使用 npx（Node.js 自带）
npx http-server -p 8000

# 使用 PHP
php -S localhost:8000
```

啟動后，浏览器会自動打开 `http://localhost:8000`，或手动存取该位址。

按 `Ctrl+C` 可停止伺服器。

### 2. 修改監控点

编辑 `viewpoints.json` 檔案来更换您想要監控的地点：

```json
{
  "title": "我的監視器墙",
  "autoRefresh": true,
  "refreshInterval": 60,
  "layout": {
    "columns": 2,
    "rows": 2
  },
  "cameras": [
    {
      "id": "1",
      "name": "監控点名称",
      "description": "監控点描述",
      "imageUrl": "監控圖片URL",
      "location": "地理位置",
      "category": "分類別標籤"
    }
  ]
}
```

## 如何取得監控器 URL

### 方法 1: 靜態圖片監控器

从 tw.live 网站取得靜態監控畫面：

1. 存取 https://tw.live/
2. 找到您想要的監控点（例如：國道一号、阳明山等）
3. 在監控畫面上**右键點擊** → 選取"在新標籤页中打开圖片"
4. 複製浏览器位址栏中的 URL
5. 将這個 URL 填入 `viewpoints.json` 的 `imageUrl` 字段

設定範例：
```json
{
  "id": "1",
  "name": "國道一号三重段",
  "type": "image",
  "imageUrl": "https://cctv1.freeway.gov.tw/abs2jpg.php?sn=1040-S-05.2-M",
  "location": "新北市三重区",
  "category": "國道"
}
```

**注意**：`type` 字段可以省略，預設为 `image`。

### 方法 2: YouTube 直播監控器

从 tw.live 网站取得 YouTube 直播：

1. 存取 https://tw.live/
2. 找到有 YouTube 直播的監控点（例如：https://tw.live/cam/?id=ymswyttbpd）
3. 在页面上找到 YouTube 播放器
4. **右键點擊播放器** → 選取"複製影片网址"
5. 从网址中提取影片 ID（例如：`https://www.youtube.com/watch?v=RttyIGHbN_w` 中的 `RttyIGHbN_w`）
6. 将影片 ID 填入組態檔

設定範例：
```json
{
  "id": "2",
  "name": "阳明书屋台北盆地",
  "description": "阳明山国家公园 YouTube 直播",
  "type": "youtube",
  "youtubeId": "RttyIGHbN_w",
  "location": "台北市北投区",
  "category": "景點"
}
```

**YouTube 直播特点**：
- 即時视频流，无需重新整理
- 自動播放（静音模式）
- 带有红色 "LIVE" 标志
- 可以點擊播放器控制播放

### 方法 3: HLS (M3U8) 串流監控器

从 tw.live 网站取得 HLS 串流：

1. 存取 https://tw.live/
2. 找到使用 HLS 串流的監控点（例如：https://tw.live/cam/?id=BOT137）
3. 按 **F12** 打开开发者工具
4. 切換到 "Network"（網路）標籤页
5. 在篩選器中輸入 `.m3u8` 或 `m3u8`
6. 重新整理页面，找到類別似 `live.m3u8` 的請求
7. 右键點擊請求 → "Copy" → "Copy URL"
8. 将完整 URL 填入組態檔

設定範例：
```json
{
  "id": "3",
  "name": "市府路松寿路口",
  "description": "台北市信义区 HLS 串流",
  "type": "hls",
  "hlsUrl": "https://jtmctrafficcctv2.gov.taipei/NVR/de868bf6-b954-447d-8c11-c5348092a1aa/live.m3u8",
  "location": "台北市信义区",
  "category": "市區"
}
```

**HLS 串流特点**：
- 高质量即時视频流
- 自動播放（静音模式）
- 带有蓝色 "HLS LIVE" 标志
- 支援播放控制和全螢幕
- 适用于台北市政府等提供的監控点

### 方法 4: 常见監控器 URL 格式

#### 國道高速公路
```
https://cctv1.freeway.gov.tw/abs2jpg.php?sn=XXXX-X-XX.X-X
```

#### 省道公路
```
https://cctv9.freeway.gov.tw/abs2jpg.php?sn=XXXXX-X-XXX.X-X
```

#### 台北市區
```
https://cctvn.freeway.gov.tw/abs2jpg.php?id=XXXXXXX
```

## 設定說明

### 基本設定

| 字段 | 說明 | 範例值 |
|------|------|--------|
| `title` | 页面標題 | "我的監視器墙" |
| `autoRefresh` | 是否自動重新整理 | `true` 或 `false` |
| `refreshInterval` | 重新整理間隔（秒） | `60` |

### 版面設定設定

| 版面設定 | columns | rows | 总監控数 |
|------|---------|------|----------|
| 2x2 四宮格 | 2 | 2 | 4 |
| 3x2 六宮格 | 3 | 2 | 6 |
| 3x3 九宮格 | 3 | 3 | 9 |
| 4x3 十二宮格 | 4 | 3 | 12 |

### 攝影機設定

每个攝影機需要套件含以下字段：

**靜態圖片監控器（預設）**：
```json
{
  "id": "唯一識別符",
  "name": "顯示名称",
  "description": "详细描述",
  "type": "image",
  "imageUrl": "圖片 URL",
  "location": "地理位置",
  "category": "分類別（國道/省道/市區/景點）"
}
```

**YouTube 直播監控器**：
```json
{
  "id": "唯一識別符",
  "name": "顯示名称",
  "description": "详细描述",
  "type": "youtube",
  "youtubeId": "YouTube 影片 ID",
  "location": "地理位置",
  "category": "分類別（國道/省道/市區/景點）"
}
```

**HLS/M3U8 串流監控器**：
```json
{
  "id": "唯一識別符",
  "name": "顯示名称",
  "description": "详细描述",
  "type": "hls",
  "hlsUrl": "HLS 串流 URL（.m3u8）",
  "location": "地理位置",
  "category": "分類別（國道/省道/市區/景點）"
}
```

**字段說明**：
- `type`: 監控器類型
  - `image` 或省略：靜態圖片（需要定期重新整理）
  - `youtube`：YouTube 直播（即時串流）
  - `hls`：HLS/M3U8 串流（即時串流）
- `imageUrl`: 仅用于 `type: "image"`，靜態圖片的 URL
- `youtubeId`: 仅用于 `type: "youtube"`，YouTube 影片的 ID
- `hlsUrl`: 仅用于 `type: "hls"`，M3U8 串流的完整 URL

## 使用范例

### 范例 1: 上班通勤路线監控

監控您每天的通勤路线：

```json
{
  "title": "通勤路线監控",
  "cameras": [
    {
      "name": "国一五股",
      "imageUrl": "...",
      "category": "國道"
    },
    {
      "name": "台北市民大道",
      "imageUrl": "...",
      "category": "市區"
    },
    {
      "name": "内湖交流道",
      "imageUrl": "...",
      "category": "國道"
    },
    {
      "name": "公司附近路口",
      "imageUrl": "...",
      "category": "市區"
    }
  ]
}
```

### 范例 2: 周末旅游路线

監控您常去的景點：

```json
{
  "title": "周末旅游路线",
  "cameras": [
    {
      "name": "国五雪山隧道",
      "imageUrl": "...",
      "category": "國道"
    },
    {
      "name": "宜兰头城",
      "imageUrl": "...",
      "category": "省道"
    },
    {
      "name": "阳明山竹子湖",
      "imageUrl": "...",
      "category": "景點"
    },
    {
      "name": "北宜公路",
      "imageUrl": "...",
      "category": "省道"
    }
  ]
}
```

### 范例 3: 混合監控（靜態圖片 + YouTube + HLS）

```json
{
  "title": "完整監控系统",
  "layout": {
    "columns": 3,
    "rows": 2
  },
  "cameras": [
    {
      "name": "国一五股",
      "type": "image",
      "imageUrl": "https://cctv1.freeway.gov.tw/abs2jpg.php?sn=...",
      "category": "國道"
    },
    {
      "name": "阳明山直播",
      "type": "youtube",
      "youtubeId": "RttyIGHbN_w",
      "category": "景點"
    },
    {
      "name": "市府路口",
      "type": "hls",
      "hlsUrl": "https://jtmctrafficcctv2.gov.taipei/NVR/.../live.m3u8",
      "category": "市區"
    },
    {
      "name": "台北101",
      "type": "image",
      "imageUrl": "https://cctvn.freeway.gov.tw/abs2jpg.php?id=...",
      "category": "市區"
    },
    {
      "name": "合欢山直播",
      "type": "youtube",
      "youtubeId": "YOUR_YOUTUBE_ID",
      "category": "景點"
    },
    {
      "name": "信义区路口",
      "type": "hls",
      "hlsUrl": "https://jtmctrafficcctv2.gov.taipei/NVR/.../live.m3u8",
      "category": "市區"
    }
  ]
}
```

### 范例 4: 多地点天氣監控

```json
{
  "title": "台湾各地天氣",
  "layout": {
    "columns": 3,
    "rows": 3
  },
  "cameras": [
    {
      "name": "台北",
      "location": "台北市",
      "category": "市區"
    },
    {
      "name": "台中",
      "location": "台中市",
      "category": "市區"
    },
    {
      "name": "台南",
      "location": "台南市",
      "category": "市區"
    },
    {
      "name": "高雄",
      "location": "高雄市",
      "category": "市區"
    },
    {
      "name": "宜兰",
      "location": "宜兰县",
      "category": "省道"
    },
    {
      "name": "花莲",
      "location": "花莲县",
      "category": "省道"
    },
    {
      "name": "合欢山",
      "location": "南投县",
      "category": "景點"
    },
    {
      "name": "阿里山",
      "location": "嘉义县",
      "category": "景點"
    },
    {
      "name": "垦丁",
      "location": "屏东县",
      "category": "景點"
    }
  ]
}
```

## 操作說明

### 手动重新整理
點擊页面右上角的"手动重新整理"按鈕可立即更新所有監控畫面。

### 自動重新整理
- 點擊"啟用自動重新整理"按鈕开启自動重新整理
- 重新整理間隔可在 `viewpoints.json` 中的 `refreshInterval` 設定（单位：秒）
- 點擊"停止自動重新整理"可以关闭

### 全螢幕查看
- 點擊任何監控畫面可以全螢幕查看
- 按 ESC 键或點擊右上角的 × 关闭全螢幕

## 常见问题

### Q: 顯示"CORS 請求未使用 http 通讯协定"錯誤？

A: 这是浏览器的安全性策略。**不要直接双击打开 HTML 檔案**，必須透過本機伺服器執行：
```bash
python3 start-server.py
```

### Q: 監控畫面顯示"載入失敗"？

A: 可能的原因：
1. 監控器 URL 不正确
2. 该監控点暂时離線
3. 網路連線问题

解决方法：點擊錯誤提示可重新載入，或到 tw.live 確認该監控点是否正常。

### Q: 如何找到 HLS 串流的 M3U8 URL？

A: 有两种方法：

**方法 1: 使用开发者工具（推荐）**
1. 存取 tw.live 上的監控页面（例如：https://tw.live/cam/?id=BOT137）
2. 按 **F12** 打开开发者工具
3. 切換到 **Network**（網路）標籤页
4. 在篩選器中輸入 `m3u8`
5. 重新整理页面
6. 找到 `live.m3u8` 的請求
7. 右键 → Copy → Copy URL
8. 貼上到組態檔的 `hlsUrl` 字段

**方法 2: 查看页面源程式碼**
1. 在監控页面上右键 → "查看网页源程式碼"
2. 按 Ctrl+F 搜尋 `.m3u8`
3. 找到完整的 URL（通常在 `<source src="...">` 標籤中）
4. 複製完整 URL

**常见 HLS URL 格式**：
- 台北市：`https://jtmctrafficcctv2.gov.taipei/NVR/[UUID]/live.m3u8`
- 其他县市可能有不同格式

### Q: HLS 串流和 YouTube 直播有什麼区别？

A: 
- **HLS 串流**：
  - 来自政府机关的監控系统（如台北市交通局）
  - 使用 M3U8 格式
  - 需要 Video.js 播放器
  - 通常延遲较低
  - 蓝色 "HLS LIVE" 标志

- **YouTube 直播**：
  - 来自 YouTube 平台
  - 使用 YouTube 嵌入式播放器
  - 可能有广告
  - 红色 "LIVE" 标志

### Q: 为什麼 HLS 串流无法播放？

A: 可能的原因：
1. **URL 過期**：某些 HLS URL 套件含时效性 token，需要重新取得
2. **網路限制**：某些串流可能有地理或網路限制
3. **浏览器不支援**：建议使用 Chrome、Firefox 或 Edge 最新版本

解决方法：
- 重新从 tw.live 取得最新的 M3U8 URL
- 檢查浏览器控制台（F12）的錯誤資訊
- 確認本機伺服器正常執行

### Q: 如何找到 YouTube 直播的影片 ID？

A: 有两种方法：
1. **从播放器取得**：在 YouTube 播放器上右键 → "複製影片网址" → 从 URL 中提取 ID
   - 範例 URL：`https://www.youtube.com/watch?v=RttyIGHbN_w`
   - 影片 ID：`RttyIGHbN_w`（`v=` 后面的部分）

2. **从 tw.live 页面源程式碼取得**：按 F12 → 搜尋 `youtube.com/embed/` → 複製 ID
   - 範例：`youtube.com/embed/RttyIGHbN_w`
   - 影片 ID：`RttyIGHbN_w`

### Q: YouTube 直播会自動重新整理吗？

A: 不需要！YouTube 直播是即時视频流，会持续播放，无需重新整理。自動重新整理功能仅对靜態圖片監控器有效。

### Q: 可以同时使用靜態圖片、YouTube 和 HLS 吗？

A: 可以！您可以在同一个監視器墙中混合使用三种類型。参考"范例 3: 混合監控"。

### Q: 如何找到更多監控点？

A: 存取 https://tw.live/ 浏览以下分類別：
- 國道路况：國道一号～十号
- 省道路况：各县市省道
- 市區路况：六都市區道路
- 旅游景點：合欢山、阳明山、阿里山等
- 国家公园：雪霸、玉山、太鲁阁等

### Q: 可以監控几个地点？

A: 建议根据屏幕大小選取：
- 電腦大屏幕：4-12 个（2x2 到 4x3）
- 笔记本：4-6 个（2x2 或 3x2）
- 手機：2-4 个

### Q: 重新整理間隔設定多少比較好？

A: 建议設定：
- 路况監控：30-60 秒
- 景點天氣：60-120 秒
- 避免設定太短（<30秒），以免给伺服器造成负担

## 技术說明

- 纯前端實作，无需后端伺服器
- 使用原生 JavaScript，无外部相依
- 回應式 CSS Grid 版面設定
- 支援所有现代浏览器

## 授權与宣告

本專案仅为个人学习和使用目的。監控畫面版权归原提供方所有。

影像来源：
- 交通部高速公路局
- 公路总局
- 各县市政府
- 国家公园管理处
- tw.live 网站

## 更新日誌

### v1.0.0 (2026-01-19)
- 初始版本發布
- 支援 2x2 四宮格版面設定
- 自動/手动重新整理功能
- 全螢幕查看功能
- JSON 組態檔支援
