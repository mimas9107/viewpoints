# 监视器墙 - 个人化 CCTV 监控面板

基于 tw.live 的客制化监视器墙系统，可通过 JSON 配置文件轻松管理您关注的监控点。

## 功能特色

- 🎯 2x2 四宫格布局（可扩展到 3x2、3x3、4x3）
- 🔄 自动刷新功能（可自定义刷新间隔）
- 📱 响应式设计，支持手机和电脑
- 🖼️ 点击图片可全屏查看
- ⚙️ 通过 JSON 文件轻松配置监控点
- ⏰ 显示每个监控画面的最后更新时间
- 🤖 **AI 整合** - 支援 MCP Server，让 AI 助手帮你分析路况

## 🤖 AI 整合 (MCP Server)

Viewpoints 内建 **MCP (Model Context Protocol) Server**，可以将监视器数据连接到 Claude Desktop 或其他 AI 助手。

### 特色功能

- **智能查詢**：讓 AI 幫你搜尋監視器（例：「林口路段現在塞車嗎？」）
- **視覺分析**：AI 可以獲取監視器截圖，直接分析畫面中的車流、天氣
- **自然語言**：用日常對話的方式與 AI 討論路況

### 設定方式

請參考 [MCP_GUIDE.md](./MCP_GUIDE.md) 完整教學。

## 快速开始

### 1. 启动本地服务器

由于浏览器的安全限制（CORS），需要通过本地服务器来运行。

**方法 A: 使用 Python（推荐）**

```bash
# 直接运行启动脚本
python3 start-server.py

# 或使用 Python 内置服务器
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

启动后，浏览器会自动打开 `http://localhost:8000`，或手动访问该地址。

按 `Ctrl+C` 可停止服务器。

### 2. 修改监控点

编辑 `viewpoints.json` 文件来更换您想要监控的地点：

```json
{
  "title": "我的监视器墙",
  "autoRefresh": true,
  "refreshInterval": 60,
  "layout": {
    "columns": 2,
    "rows": 2
  },
  "cameras": [
    {
      "id": "1",
      "name": "监控点名称",
      "description": "监控点描述",
      "imageUrl": "监控图片URL",
      "location": "地理位置",
      "category": "分类标签"
    }
  ]
}
```

## 如何获取监控器 URL

### 方法 1: 静态图片监控器

从 tw.live 网站获取静态监控画面：

1. 访问 https://tw.live/
2. 找到您想要的监控点（例如：国道一号、阳明山等）
3. 在监控画面上**右键点击** → 选择"在新标签页中打开图片"
4. 复制浏览器地址栏中的 URL
5. 将这个 URL 填入 `viewpoints.json` 的 `imageUrl` 字段

配置示例：
```json
{
  "id": "1",
  "name": "国道一号三重段",
  "type": "image",
  "imageUrl": "https://cctv1.freeway.gov.tw/abs2jpg.php?sn=1040-S-05.2-M",
  "location": "新北市三重区",
  "category": "国道"
}
```

**注意**：`type` 字段可以省略，默认为 `image`。

### 方法 2: YouTube 直播监控器

从 tw.live 网站获取 YouTube 直播：

1. 访问 https://tw.live/
2. 找到有 YouTube 直播的监控点（例如：https://tw.live/cam/?id=ymswyttbpd）
3. 在页面上找到 YouTube 播放器
4. **右键点击播放器** → 选择"复制影片网址"
5. 从网址中提取影片 ID（例如：`https://www.youtube.com/watch?v=RttyIGHbN_w` 中的 `RttyIGHbN_w`）
6. 将影片 ID 填入配置文件

配置示例：
```json
{
  "id": "2",
  "name": "阳明书屋台北盆地",
  "description": "阳明山国家公园 YouTube 直播",
  "type": "youtube",
  "youtubeId": "RttyIGHbN_w",
  "location": "台北市北投区",
  "category": "景点"
}
```

**YouTube 直播特点**：
- 实时视频流，无需刷新
- 自动播放（静音模式）
- 带有红色 "LIVE" 标志
- 可以点击播放器控制播放

### 方法 3: HLS (M3U8) 串流监控器

从 tw.live 网站获取 HLS 串流：

1. 访问 https://tw.live/
2. 找到使用 HLS 串流的监控点（例如：https://tw.live/cam/?id=BOT137）
3. 按 **F12** 打开开发者工具
4. 切换到 "Network"（网络）标签页
5. 在过滤器中输入 `.m3u8` 或 `m3u8`
6. 刷新页面，找到类似 `live.m3u8` 的请求
7. 右键点击请求 → "Copy" → "Copy URL"
8. 将完整 URL 填入配置文件

配置示例：
```json
{
  "id": "3",
  "name": "市府路松寿路口",
  "description": "台北市信义区 HLS 串流",
  "type": "hls",
  "hlsUrl": "https://jtmctrafficcctv2.gov.taipei/NVR/de868bf6-b954-447d-8c11-c5348092a1aa/live.m3u8",
  "location": "台北市信义区",
  "category": "市区"
}
```

**HLS 串流特点**：
- 高质量实时视频流
- 自动播放（静音模式）
- 带有蓝色 "HLS LIVE" 标志
- 支持播放控制和全屏
- 适用于台北市政府等提供的监控点

### 方法 4: 常见监控器 URL 格式

#### 国道高速公路
```
https://cctv1.freeway.gov.tw/abs2jpg.php?sn=XXXX-X-XX.X-X
```

#### 省道公路
```
https://cctv9.freeway.gov.tw/abs2jpg.php?sn=XXXXX-X-XXX.X-X
```

#### 台北市区
```
https://cctvn.freeway.gov.tw/abs2jpg.php?id=XXXXXXX
```

## 配置说明

### 基本设置

| 字段 | 说明 | 示例值 |
|------|------|--------|
| `title` | 页面标题 | "我的监视器墙" |
| `autoRefresh` | 是否自动刷新 | `true` 或 `false` |
| `refreshInterval` | 刷新间隔（秒） | `60` |

### 布局设置

| 布局 | columns | rows | 总监控数 |
|------|---------|------|----------|
| 2x2 四宫格 | 2 | 2 | 4 |
| 3x2 六宫格 | 3 | 2 | 6 |
| 3x3 九宫格 | 3 | 3 | 9 |
| 4x3 十二宫格 | 4 | 3 | 12 |

### 摄像头配置

每个摄像头需要包含以下字段：

**静态图片监控器（默认）**：
```json
{
  "id": "唯一标识符",
  "name": "显示名称",
  "description": "详细描述",
  "type": "image",
  "imageUrl": "图片 URL",
  "location": "地理位置",
  "category": "分类（国道/省道/市区/景点）"
}
```

**YouTube 直播监控器**：
```json
{
  "id": "唯一标识符",
  "name": "显示名称",
  "description": "详细描述",
  "type": "youtube",
  "youtubeId": "YouTube 影片 ID",
  "location": "地理位置",
  "category": "分类（国道/省道/市区/景点）"
}
```

**HLS/M3U8 串流监控器**：
```json
{
  "id": "唯一标识符",
  "name": "显示名称",
  "description": "详细描述",
  "type": "hls",
  "hlsUrl": "HLS 串流 URL（.m3u8）",
  "location": "地理位置",
  "category": "分类（国道/省道/市区/景点）"
}
```

**字段说明**：
- `type`: 监控器类型
  - `image` 或省略：静态图片（需要定期刷新）
  - `youtube`：YouTube 直播（实时串流）
  - `hls`：HLS/M3U8 串流（实时串流）
- `imageUrl`: 仅用于 `type: "image"`，静态图片的 URL
- `youtubeId`: 仅用于 `type: "youtube"`，YouTube 影片的 ID
- `hlsUrl`: 仅用于 `type: "hls"`，M3U8 串流的完整 URL

## 使用范例

### 范例 1: 上班通勤路线监控

监控您每天的通勤路线：

```json
{
  "title": "通勤路线监控",
  "cameras": [
    {
      "name": "国一五股",
      "imageUrl": "...",
      "category": "国道"
    },
    {
      "name": "台北市民大道",
      "imageUrl": "...",
      "category": "市区"
    },
    {
      "name": "内湖交流道",
      "imageUrl": "...",
      "category": "国道"
    },
    {
      "name": "公司附近路口",
      "imageUrl": "...",
      "category": "市区"
    }
  ]
}
```

### 范例 2: 周末旅游路线

监控您常去的景点：

```json
{
  "title": "周末旅游路线",
  "cameras": [
    {
      "name": "国五雪山隧道",
      "imageUrl": "...",
      "category": "国道"
    },
    {
      "name": "宜兰头城",
      "imageUrl": "...",
      "category": "省道"
    },
    {
      "name": "阳明山竹子湖",
      "imageUrl": "...",
      "category": "景点"
    },
    {
      "name": "北宜公路",
      "imageUrl": "...",
      "category": "省道"
    }
  ]
}
```

### 范例 3: 混合监控（静态图片 + YouTube + HLS）

```json
{
  "title": "完整监控系统",
  "layout": {
    "columns": 3,
    "rows": 2
  },
  "cameras": [
    {
      "name": "国一五股",
      "type": "image",
      "imageUrl": "https://cctv1.freeway.gov.tw/abs2jpg.php?sn=...",
      "category": "国道"
    },
    {
      "name": "阳明山直播",
      "type": "youtube",
      "youtubeId": "RttyIGHbN_w",
      "category": "景点"
    },
    {
      "name": "市府路口",
      "type": "hls",
      "hlsUrl": "https://jtmctrafficcctv2.gov.taipei/NVR/.../live.m3u8",
      "category": "市区"
    },
    {
      "name": "台北101",
      "type": "image",
      "imageUrl": "https://cctvn.freeway.gov.tw/abs2jpg.php?id=...",
      "category": "市区"
    },
    {
      "name": "合欢山直播",
      "type": "youtube",
      "youtubeId": "YOUR_YOUTUBE_ID",
      "category": "景点"
    },
    {
      "name": "信义区路口",
      "type": "hls",
      "hlsUrl": "https://jtmctrafficcctv2.gov.taipei/NVR/.../live.m3u8",
      "category": "市区"
    }
  ]
}
```

### 范例 4: 多地点天气监控

```json
{
  "title": "台湾各地天气",
  "layout": {
    "columns": 3,
    "rows": 3
  },
  "cameras": [
    {
      "name": "台北",
      "location": "台北市",
      "category": "市区"
    },
    {
      "name": "台中",
      "location": "台中市",
      "category": "市区"
    },
    {
      "name": "台南",
      "location": "台南市",
      "category": "市区"
    },
    {
      "name": "高雄",
      "location": "高雄市",
      "category": "市区"
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
      "category": "景点"
    },
    {
      "name": "阿里山",
      "location": "嘉义县",
      "category": "景点"
    },
    {
      "name": "垦丁",
      "location": "屏东县",
      "category": "景点"
    }
  ]
}
```

## 操作说明

### 手动刷新
点击页面右上角的"手动刷新"按钮可立即更新所有监控画面。

### 自动刷新
- 点击"启用自动刷新"按钮开启自动刷新
- 刷新间隔可在 `viewpoints.json` 中的 `refreshInterval` 设置（单位：秒）
- 点击"停止自动刷新"可以关闭

### 全屏查看
- 点击任何监控画面可以全屏查看
- 按 ESC 键或点击右上角的 × 关闭全屏

## 常见问题

### Q: 显示"CORS 请求未使用 http 通讯协定"错误？

A: 这是浏览器的安全策略。**不要直接双击打开 HTML 文件**，必须通过本地服务器运行：
```bash
python3 start-server.py
```

### Q: 监控画面显示"加载失败"？

A: 可能的原因：
1. 监控器 URL 不正确
2. 该监控点暂时离线
3. 网络连接问题

解决方法：点击错误提示可重新加载，或到 tw.live 确认该监控点是否正常。

### Q: 如何找到 HLS 串流的 M3U8 URL？

A: 有两种方法：

**方法 1: 使用开发者工具（推荐）**
1. 访问 tw.live 上的监控页面（例如：https://tw.live/cam/?id=BOT137）
2. 按 **F12** 打开开发者工具
3. 切换到 **Network**（网络）标签页
4. 在过滤器中输入 `m3u8`
5. 刷新页面
6. 找到 `live.m3u8` 的请求
7. 右键 → Copy → Copy URL
8. 粘贴到配置文件的 `hlsUrl` 字段

**方法 2: 查看页面源代码**
1. 在监控页面上右键 → "查看网页源代码"
2. 按 Ctrl+F 搜索 `.m3u8`
3. 找到完整的 URL（通常在 `<source src="...">` 标签中）
4. 复制完整 URL

**常见 HLS URL 格式**：
- 台北市：`https://jtmctrafficcctv2.gov.taipei/NVR/[UUID]/live.m3u8`
- 其他县市可能有不同格式

### Q: HLS 串流和 YouTube 直播有什么区别？

A: 
- **HLS 串流**：
  - 来自政府机关的监控系统（如台北市交通局）
  - 使用 M3U8 格式
  - 需要 Video.js 播放器
  - 通常延迟较低
  - 蓝色 "HLS LIVE" 标志

- **YouTube 直播**：
  - 来自 YouTube 平台
  - 使用 YouTube 嵌入式播放器
  - 可能有广告
  - 红色 "LIVE" 标志

### Q: 为什么 HLS 串流无法播放？

A: 可能的原因：
1. **URL 过期**：某些 HLS URL 包含时效性 token，需要重新获取
2. **网络限制**：某些串流可能有地理或网络限制
3. **浏览器不支持**：建议使用 Chrome、Firefox 或 Edge 最新版本

解决方法：
- 重新从 tw.live 获取最新的 M3U8 URL
- 检查浏览器控制台（F12）的错误信息
- 确认本地服务器正常运行

### Q: 如何找到 YouTube 直播的影片 ID？

A: 有两种方法：
1. **从播放器获取**：在 YouTube 播放器上右键 → "复制影片网址" → 从 URL 中提取 ID
   - 示例 URL：`https://www.youtube.com/watch?v=RttyIGHbN_w`
   - 影片 ID：`RttyIGHbN_w`（`v=` 后面的部分）

2. **从 tw.live 页面源代码获取**：按 F12 → 搜索 `youtube.com/embed/` → 复制 ID
   - 示例：`youtube.com/embed/RttyIGHbN_w`
   - 影片 ID：`RttyIGHbN_w`

### Q: YouTube 直播会自动刷新吗？

A: 不需要！YouTube 直播是实时视频流，会持续播放，无需刷新。自动刷新功能仅对静态图片监控器有效。

### Q: 可以同时使用静态图片、YouTube 和 HLS 吗？

A: 可以！您可以在同一个监视器墙中混合使用三种类型。参考"范例 3: 混合监控"。

### Q: 如何找到更多监控点？

A: 访问 https://tw.live/ 浏览以下分类：
- 国道路况：国道一号～十号
- 省道路况：各县市省道
- 市区路况：六都市区道路
- 旅游景点：合欢山、阳明山、阿里山等
- 国家公园：雪霸、玉山、太鲁阁等

### Q: 可以监控几个地点？

A: 建议根据屏幕大小选择：
- 电脑大屏幕：4-12 个（2x2 到 4x3）
- 笔记本：4-6 个（2x2 或 3x2）
- 手机：2-4 个

### Q: 刷新间隔设置多少比较好？

A: 建议设置：
- 路况监控：30-60 秒
- 景点天气：60-120 秒
- 避免设置太短（<30秒），以免给服务器造成负担

## 技术说明

- 纯前端实现，无需后端服务器
- 使用原生 JavaScript，无外部依赖
- 响应式 CSS Grid 布局
- 支持所有现代浏览器

## 授权与声明

本项目仅为个人学习和使用目的。监控画面版权归原提供方所有。

影像来源：
- 交通部高速公路局
- 公路总局
- 各县市政府
- 国家公园管理处
- tw.live 网站

## 更新日志

### v1.0.0 (2026-01-19)
- 初始版本发布
- 支持 2x2 四宫格布局
- 自动/手动刷新功能
- 全屏查看功能
- JSON 配置文件支持
