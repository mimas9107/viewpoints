# 上傳介面使用說明

## 功能概述

上傳介面讓您可以上傳自訂的 JSON 設定檔案，輕鬆套用到監視器牆。無需手動編輯 JSON 檔案或重新部署。

## 檔案說明

```
viewpoints/
├── index.html              # 主監控牆頁面
├── picker.html             # 監控點選擇器
├── upload.html             # 上傳組態介面
├── viewpoints.json         # 目前設定
├── start-server-fastapi.py # 統一伺服器（推薦）
├── .backups/               # 備份目錄（自動建立）
└── README.md              # 使用說明
```

## 使用流程

### 步驟 1：啟動伺服器（推薦）

```bash
cd viewpoints
pip install -r requirements.txt
python3 start-server-fastapi.py
```

### 步驟 2：開啟上傳介面

在瀏覽器開啟：

```
http://localhost:8844/upload.html
```

### 步驟 3：選擇或拖曳檔案

**方式一：點擊選擇**

1. 點擊虛線框內的區域
2. 選擇您的 JSON 檔案

**方式二：拖曳上傳**

1. 將 JSON 檔案拖曳到虛線框內
2. 放開滑鼠即可

### 步驟 4：上傳並套用

1. 確認選擇的檔案正確
2. 點擊「上傳並套用配置」按鈕
3. 等待上傳完成

### 步驟 5：查看監控牆

重新整理 `http://localhost:8844`，您的設定就會生效！

## 介面功能

### 目前配置狀態

頁面頂部顯示目前正在使用的設定資訊：
- 設定名稱
- 監控點數量
- 自動重新整理狀態
- 整理間隔

### 檔案選擇區

- 支援點擊選擇檔案
- 支援拖曳上傳
- 顯示已選擇的檔案資訊
- 顯示監控點數量預覽

### 操作按鈕

- **上傳並套用配置** - 上傳並覆寫目前設定
- **下載目前配置** - 下載目前的 viewpoints.json
- **檢視備份** - 瀏覽歷史備份檔案

## 檔案格式要求

上傳的 JSON 檔案必須符合以下格式：

```json
{
  "title": "我的監視器牆",
  "autoRefresh": true,
  "refreshInterval": 60,
  "layout": {
    "columns": 3,
    "rows": 2
  },
  "cameras": [
    {
      "id": "ymswyttbpd",
      "name": "陽明書屋遠眺台北盆地",
      "type": "youtube",
      "youtubeId": "RttyIGHbN_w",
      "category": "陽明山"
    },
    {
      "id": "T14A-d61a0c91",
      "name": "合歡山武嶺亭",
      "type": "image",
      "imageUrl": "https://cctv-ss04.thb.gov.tw/T14A-d61a0c91",
      "location": "南投縣仁愛鄉",
      "category": "景點"
    }
  ]
}
```

**必要欄位：**
- `cameras` - 監控點陣列
- 每個監控點必須包含：`id`、`name`、`type`

**監控點類型：**
- `type: "image"` - 需要 `imageUrl` 欄位
- `type: "youtube"` - 需要 `youtubeId` 欄位
- `type: "hls"` - 需要 `hlsUrl` 欄位

## 備份機制

### 自動備份

每次成功上傳設定時，系統會自動：
1. 將目前的設定備份到 `.backups/` 目錄
2. 檔名格式：`viewpoints_YYYYMMDD_HHMMSS_xxxxxxxx.json`
3. 最多保留 10 份備份

### 復原備份

如需復原到之前的設定：

1. 聯絡管理員協助復原
2. 或使用 API 端點：

```bash
# 列出所有備份
curl http://localhost:8844/api/config/backups

# 復原指定備份
curl -X POST http://localhost:8844/api/config/backups/viewpoints_20260120_120000_abc12345.json/restore
```

## 與選擇器的比較

| 功能 | 上傳介面 (upload.html) | 選擇器 (picker.html) |
|------|------------------------|---------------------|
| 從資料庫選擇 | 否 | 是 |
| 上傳自訂 JSON | 是 | 否 |
| 拖曳上傳 | 是 | 否 |
| 顯示目前狀態 | 是 | 否 |
| 備份機制 | 自動 | 手動 |
| 適用情境 | 使用現有 JSON 檔案 | 從頭建立設定 |

## 故障排除

### 問題：上傳頁面打不開

**解決：**
1. 確認伺服器正在執行
2. 存取正確的 URL：`http://localhost:8844/upload.html`

### 問題：上傳失敗

**解決：**
1. 確認 `start-server-fastapi.py` 正在執行
2. 檢查 JSON 格式是否正確
3. 確認檔案大小不超過限制

### 問題：JSON 格式錯誤

**常見錯誤：**
1. 缺少必要的欄位（`cameras`、`id`、`name`）
2. 監控點類型與 URL 欄位不匹配
3. JSON 語法錯誤（逗號、分號）

**解決：**
1. 使用 JSON 驗證工具檢查
2. 參考本文件的「檔案格式要求」章節
3. 參考現有的 `viewpoints.json` 範例

### 問題：上傳後設定沒生效

**解決：**
1. 重新整理監控牆頁面（Ctrl+Shift+R）
2. 清除瀏覽器快取
3. 確認上傳的是正確的檔案

### 問題：如何取得範例 JSON？

**方式一：從選擇器匯出**
1. 開啟 `http://localhost:8844/picker.html`
2. 選擇監控點
3. 點擊「匯出設定」

**方式二：下載目前設定**
1. 開啟 `http://localhost:8844/upload.html`
2. 點擊「下載目前配置」

**方式三：參考專案內的檔案**
- `viewpoints.json` - 目前使用的設定

## API 參考

如果您需要透過指令列或其他程式上傳設定，可以使用以下 API：

### 讀取目前配置

```bash
curl http://localhost:8844/api/config
```

### 上傳新配置

```bash
curl -X POST http://localhost:8844/api/config \
  -H "Content-Type: application/json" \
  -d @your-config.json
```

### 下載配置檔案

```bash
curl -O http://localhost:8844/api/config/download
```

### 列出備份

```bash
curl http://localhost:8844/api/config/backups
```

## 使用情境

### 情境一：從他人處取得設定

1. 對方分享 `viewpoints.json` 給您
2. 開啟 `http://localhost:8844/upload.html`
3. 選擇或拖曳該檔案
4. 點擊「上傳並套用配置」
5. 完成！

### 情境二：備份與復原

**備份：**
每次上傳都會自動備份，無需手動操作。

**復原：**
聯絡管理員協助復原，或使用 API 端點。

### 情境三：管理多組設定

1. 分別命名並儲存不同的 JSON 檔案
   - `viewpoints_home.json` - 居家監控
   - `viewpoints_work.json` - 公司監控
   - `viewpoints_travel.json` - 旅遊監控

2. 根據需求上傳不同的檔案

## 安全性考量

- 只允許上傳 JSON 格式的檔案
- 上傳前會驗證 JSON 結構
- 備份機制防止設定遺失
- 建議定期手動備份重要的設定檔案

---

**提示：** 如有任何問題，請參考 [README.md](README.md) 或聯絡專案維護者。
