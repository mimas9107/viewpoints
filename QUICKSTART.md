# 监视器墙 - 快速开始

## 一分钟快速启动

### 1. 启动服务器

```bash
cd viewpoints
python3 start-server.py
```

浏览器会自动打开 `http://localhost:8000`

### 2. 停止服务器

按 `Ctrl+C` 即可停止

## 文件说明

```
viewpoints/
├── index.html              # 主页面
├── viewpoints.json         # 配置文件（可随时修改）
├── start-server.py         # Python 服务器启动脚本
├── start-server.js         # Node.js 服务器启动脚本
├── README.md              # 完整使用说明
└── QUICKSTART.md          # 本文件
```

## 修改监控点

编辑 `viewpoints.json` 文件，修改其中的监控点信息。

### 三种监控类型

#### 1. 静态图片（默认）
```json
{
  "name": "监控点名称",
  "imageUrl": "https://example.com/image.jpg",
  "location": "地点",
  "category": "分类"
}
```

#### 2. YouTube 直播
```json
{
  "name": "监控点名称",
  "type": "youtube",
  "youtubeId": "影片ID",
  "location": "地点",
  "category": "分类"
}
```

#### 3. HLS 串流
```json
{
  "name": "监控点名称",
  "type": "hls",
  "hlsUrl": "https://example.com/stream.m3u8",
  "location": "地点",
  "category": "分类"
}
```

## 常见问题

### Q: 页面显示"无法加载配置文件"？
A: 确保您是通过 `python3 start-server.py` 启动的，而不是直接双击打开 HTML 文件。

### Q: 如何更改布局？
A: 编辑 `viewpoints.json` 中的 `layout` 字段：
```json
"layout": {
  "columns": 2,  // 列数
  "rows": 2      // 行数
}
```

### Q: 如何找到监控点 URL？
A: 访问 https://tw.live/ 找到监控点，详细方法请看 README.md

## 更多信息

详细使用说明请参考 [README.md](README.md)
