# 爬蟲使用指南

本指南詳細說明如何使用 `scraper.py` 和相關工具從 tw.live 抓取監控點資料並建立監控牆資料庫。

## 📋 目錄

- [快速開始](#快速開始)
- [技術重點整理](#技術重點整理)
- [使用步驟](#使用步驟)
- [方法文件](#方法文件)
- [技術文件參考](#技術文件參考)
- [版本宣告](#版本宣告)

---

## ✅ 技術重點整理

1. **CHANGELOG.md 更新**：添加 `[Unreleased]` 版本記錄，詳細記錄：
   - 新增工具（scraper_blueprint.py、scraper2.py）
   - 爬蟲架構重構與修復
   - HLS 串流提取改進
   - 動態圖片 URL 處理
   - 外部播放器相容性處理

2. **版本號同步**：
   - scraper.py: v2.0.1
   - scraper2.py: v2.0.1
   - scraper_blueprint.py: v2.0.1

### 🎯 核心技術點：

- **分類藍圖系統**：自動發現網站所有監控點分類頁面
- **三種監控點類型支援**：image（動態）、hls（串流）、youtube（直播）
- **去重機制**：防止重複抓取相同監控點
- **瀏覽器相容性**：處理 Firefox/Chrome HLS 差異

現在您可以使用更新後的 scraper.py 進行完整抓取，所有監控點都會有正確的格式和來源連結。

---

## 🚀 快速開始

### 前置需求

```bash
# 安裝必要套件
pip install beautifulsoup4 requests lxml
```

### 基本使用

```bash
# 執行完整抓取
python3 scraper.py
```

---

## 📖 使用步驟

### 步驟 1：發現網站結構（可選）

如果您需要重新建立分類藍圖：

```bash
python3 scraper_blueprint.py
```

**輸出**：`scraper_blueprint.json`
- 包含所有終點頁面 URL
- 總共約 80 個終點頁面

### 步驟 2：執行完整抓取

```bash
# 使用預定義的分類列表進行抓取
python3 scraper.py
```

**輸出**：`cameras_database.json`
- 所有監控點資料
- 按分類組織
- 包含來源類型和連結

### 步驟 3：測試抓取（可選）

```bash
# 使用分類藍圖進行測試抓取
python3 scraper2.py
```

**輸出**：`testoutput.json`
- 測試輸出檔案
- 用於驗證抓取邏輯

---

## 🔧 方法文件

### TWLiveScraper 類

主要爬蟲類別，提供完整的抓取功能。

#### 方法：

##### `fetch_page(url)`
抓取頁面並處理錯誤。

**參數**：
- `url` (str): 要抓取的頁面 URL

**傳回**：
- `str`: HTML 內容，失敗則傳回 `None`

---

##### `extract_youtube_id(html)`
從 HTML 提取 YouTube ID。

**參數**：
- `html` (str): HTML 內容

**傳回**：
- `str`: YouTube ID，找不到則傳回 `None`

---

##### `extract_hls_url(html)`
從 HTML 提取 HLS URL。

**參數**：
- `html` (str): HTML 內容

**傳回**：
- `str`: HLS URL，找不到則傳回 `None`

---

##### `extract_static_image_url(html)`
從 HTML 提取靜態圖片 URL。

**參數**：
- `html` (str): HTML 內容

**傳回**：
- `str`: 靜態圖片 URL，找不到則傳回 `None`

---

##### `scrape_camera_detail(camera_url, camera_id)`
爬取單個監控點詳細資訊。

**參數**：
- `camera_url` (str): 監控點頁面 URL
- `camera_id` (str): 監控點 ID

**傳回**：
- `dict`: 監控點資訊字典，失敗則傳回 `None`

---

##### `extract_camera_from_stack(stack, category_name)`
從 cctv-stack 提取監控點資訊。

**參數**：
- `stack` (BeautifulSoup.Tag): cctv-stack 元素
- `category_name` (str): 分類名稱

**傳回**：
- `dict`: 監控點資訊字典，不需要的監控點則傳回 `None`

**處理邏輯**：
1. 提取監控點基本資訊（ID、名稱、URL）
2. 判斷監控點類型：
   - **YouTube**: 從 thumbnail URL 提取 YouTube ID
   - **HLS**: 從詳細頁面提取 HLS 串流 URL
   - **Image**: 處理動態圖片 URL（移除 `/snapshot` 參數）
3. 自動跳過需要外部播放器的監控點

---

##### `extract_hls_from_detail_page(detail_url)`
從詳細頁面提取 HLS URL。

**參數**：
- `detail_url` (str): 詳細頁面 URL

**傳回**：
- `str`: HLS URL，無法提取則傳回 `None`

**支援格式**：
1. `<source type="application/x-mpegURL">` 標籤
2. `<iframe src="...live.m3u8">` 元素
3. 外部播放器連結（自動跳過）

---

##### `scrape_category_page(category_url, category_name)`
爬取分類頁面的所有監控點。

**參數**：
- `category_url` (str): 分類頁面 URL
- `category_name` (str): 分類名稱

**傳回**：
- `list`: 監控點資訊列表

**處理邏輯**：
1. 判斷頁面類型（終點頁面或總覽頁面）
2. 對於終點頁面，直接提取監控點
3. 對於總覽頁面，提取子頁面連結後遞歸處理

---

##### `scrape_all_categories()`
爬取所有主要分類。

**傳回**：
- `list`: 所有監控點資訊列表

**支援分類**：
- 國道（1-10 號）
- 快速道路（台61-88 線）
- 省道
- 市區
- 國家公園
- 風景區
- 其他

---

##### `save_database(filename)`
儲存資料庫到 JSON 檔案。

**參數**：
- `filename` (str): 輸出檔案名稱（預設：`cameras_database.json`）

**輸出格式**：
```json
{
  "cameras": [...],
  "categories": {
    "分類名稱": [...]
  },
  "metadata": {
    "totalCount": 總數量,
    "lastUpdated": "更新時間",
    "version": "2.0.1",
    "source": "https://tw.live"
  }
}
```

---

## 📚 技術文件參考

### 監控點資料格式

#### 靜態圖片 (type: "image")

```json
{
  "id": "唯一ID",
  "name": "監控點名稱",
  "category": "分類",
  "location": "地點",
  "url": "https://tw.live/cam/?id=xxx",
  "thumbnail": "https://example.com/xxx/snapshot?t=123456",
  "type": "image",
  "imageUrl": "https://example.com/xxx"
}
```

**特點**：
- `imageUrl` 不包含 `/snapshot` 參數
- 每次請求都會返回最新圖片
- 支援自動更新

#### HLS 串流 (type: "hls")

```json
{
  "id": "唯一ID",
  "name": "監控點名稱",
  "category": "分類",
  "location": "地點",
  "url": "https://tw.live/cam/?id=xxx",
  "thumbnail": "https://tw.live/assets/thumbnail.png?t=123456",
  "type": "hls",
  "hlsUrl": "https://example.com/xxx/live.m3u8"
}
```

**特點**：
- 支援即時串流播放
- 使用 Video.js 播放器
- Chrome 相容性較好

#### YouTube 直播 (type: "youtube")

```json
{
  "id": "唯一ID",
  "name": "監控點名稱",
  "category": "分類",
  "location": "地點",
  "url": "https://tw.live/cam/?id=xxx",
  "thumbnail": "https://img.youtube.com/vi/xxx/maxresdefault_live.jpg?t=123456",
  "type": "youtube",
  "youtubeId": "YouTube影片ID",
  "description": "分類 YouTube 直播"
}
```

**特點**：
- 使用 YouTube 嵌入播放器
- 支援直播串流

---

### 網站結構分析

#### 頁面類型

1. **終點頁面**：直接包含監控點列表（`cctv-stack`）
2. **總覽頁面（按鈕型）**：包含「即時影像」按鈕連結到子頁面
3. **總覽頁面（分區型）**：包含 `cctv-menu` 選單連結到各區

#### 分類結構

- **國道**：按方向和路段分類（北上/南下、高架道路等）
- **市區**：按行政區分類（如台北市12區）
- **國家公園**：按公園名稱分類
- **風景區**：按風景區名稱分類

---

### 演算法技術

#### 去重機制

使用 `seen_ids` 集合追蹤已處理的監控點 ID：

```python
self.seen_ids = set()

if camera_id not in self.seen_ids:
    cameras.append(camera)
    self.seen_ids.add(camera_id)
```

#### 延遲機制

避免過度請求導致被封鎖：

```python
time.sleep(0.5)  # 每個監控點間的延遲
time.sleep(1)  # 每個分類間的延遲
```

---

### 錯誤處理

#### 網路錯誤

```python
try:
    response = self.session.get(url, timeout=10)
    response.raise_for_status()
    return response.text
except Exception as e:
    print(f"❌ 抓取失敗 {url}: {e}")
    return None
```

#### 解析錯誤

```python
try:
    # 解析邏輯
    ...
except Exception as e:
    print(f"❌ 解析失敗: {e}")
    return None
```

---

## 🌐 相關網站

- [tw.live](https://tw.live) - 監控點資料來源
- [BeautifulSoup 文件](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests 文件](https://requests.readthedocs.io/)

---

## 📝 版本宣告

**版本**：2.0.1
**最後更新**：2026-01-22

### 版本記錄

#### v2.0.1 (2026-01-22)
- ✅ 完成技術重點整理
- ✅ 新增分類藍圖發現工具
- ✅ 修復 HLS 串流提取邏輯
- ✅ 修復動態圖片 URL 處理
- ✅ 改善去重機制
- ✅ 更新文件與使用指南

#### v1.3.0 (2026-01-20)
- 初始版本發布

---

## 🔍 故障排除

### 問題：爬蟲無法抓取監控點

**可能原因**：
1. 網路連線問題
2. 網站結構變更
3. IP 被封鎖

**解決方案**：
1. 檢查網路連線
2. 執行 `python3 scraper_blueprint.py` 重新建立分類藍圖
3. 等待一段時間後重試

### 問題：監控點無法顯示

**可能原因**：
1. 監控點資料格式錯誤
2. URL 已過期
3. 外部播放器不相容

**解決方案**：
1. 檢查 `cameras_database.json` 格式
2. 執行完整抓取更新資料
3. 確認瀏覽器相容性（Chrome 推薦用於 HLS）

### 問題：圖片不會自動更新

**可能原因**：
1. 使用靜態快照 URL
2. 瀏覽器快取

**解決方案**：
1. 確認 `imageUrl` 不包含 `/snapshot` 參數
2. 清除瀏覽器快取
3. 重新載入監控牆頁面

---

## 📞 技術支援

如有問題或建議，請參考：
- `CHANGELOG.md` - 版本更新記錄
- `AGENTS.md` - AI 開發指南
- `README.md` - 專案整體說明