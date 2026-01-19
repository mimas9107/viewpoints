# Viewpoints MCP Server 指南

Viewpoints 不僅是一個網頁應用，還內建了 **MCP (Model Context Protocol) Server**。
這意味著你可以將它連接到 Claude Desktop 或其他 AI 助手，讓 AI 擁有「看見」監視器的能力。

## 🤖 這是什麼？

透過 MCP，AI 可以：
1. **查詢監視器**：搜尋特定地點（如「林口」、「陽明山」）的監視器。
2. **獲取影像連結**：取得即時影像的截圖 URL。
3. **視覺分析**：結合 AI 的視覺能力 (Vision)，直接分析畫面中的車流、天氣或人潮。

## 🚀 如何安裝到 Claude Desktop

### 1. 確保環境準備好
- 安裝 [Node.js](https://nodejs.org/) (v16 以上)
- 確保專案依賴已安裝：
  ```bash
  cd viewpoints
  npm install
  ```

### 2. 編輯 Claude Desktop 配置檔
找到你的 Claude Desktop 設定檔：
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

新增以下配置：

```json
{
  "mcpServers": {
    "viewpoints": {
      "command": "node",
      "args": ["/你的專案絕對路徑/viewpoints/start-server.js"]
    }
  }
}
```

> ⚠️ 注意：請將 `/你的專案絕對路徑/` 替換為實際的檔案路徑。

### 3. 重啟 Claude Desktop
重新啟動應用程式後，你會看到一個 🔌 圖示，表示 MCP Server 已連接。

## 💡 使用範例

連接成功後，你可以直接問 Claude：

**交通查詢：**
> "幫我看看現在國道一號林口路段塞車嗎？"
> （Claude 會搜尋林口監視器 -> 獲取截圖 -> 分析畫面 -> 回答你）

**天氣查詢：**
> "陽明山現在天氣如何？看起來有下雨嗎？"
> （Claude 會調用陽明山監視器畫面進行分析）

**旅遊建議：**
> "我想去合歡山，幫我確認一下武嶺亭現在人多嗎？"

## 🛠️ 提供的工具 (Tools)

| 工具名稱 | 描述 | 參數 |
|----------|------|------|
| `list_cameras` | 搜尋監視器 | `keyword` (關鍵字), `category` (分類) |
| `get_camera_image` | 獲取影像連結 | `id` (監視器 ID) |
| `get_current_config` | 讀取目前配置 | 無 |

---

## ⚠️ 常見問題

**Q: 為什麼 HTTP Server 也在跑？**
`start-server.js` 是雙模服務器，它會同時啟動 HTTP Server (Port 8000) 供瀏覽器使用，以及 MCP Server 供 AI 使用。

**Q: AI 無法看到 YouTube 直播畫面？**
目前工具回傳的是 YouTube 的縮圖 URL。對於即時動態分析，AI 只能看到最近的縮圖快照。

**Q: HLS 串流支援嗎？**
HLS 串流 (m3u8) 較難直接截圖，工具會嘗試回傳縮圖，若無縮圖則僅提供 URL。
