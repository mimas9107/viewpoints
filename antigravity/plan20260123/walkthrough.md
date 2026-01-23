# Walkthrough - 使用者權限控制與個人化監視牆

我已成功為 Viewpoints 專案實作了使用者系統，現在多位使用者可以獨立管理各自的監視牆配置。

## 完工功能摘要

### 1. 後端認證與 API 安全
- **JWT 認證**: 實作了基於 `jose` 的 JWT Token 驗證機制。
- **使用者管理**: 新增 `users.json` 儲存加密後的密碼（使用 `pbkdf2_sha256` 方案）。
- **權限控制**: 所有 `/api/config/*` 路由現在都需要有效的 JWT Token 才能存取。
- **數據隔離**: 不同使用者擁有獨立的配置檔案（格式為 `viewpoints_<username>.json`）。

### 2. 前端登入體驗
- **現代化登入頁**: 新增 `login.html`，具備美觀的 Glassmorphism 設計與流暢動畫。
- **整合註冊與登入**: 使用者可以直接在介面切換註冊與登入模式。
- **認證狀態管理**: 透過 `js/auth.js` 自動管理 Token 並處理請求攔截。

### 3. 全站整合
- **index.html**: 實作了認證檢查，未登入者會自動導向登入頁，並在標題列顯示目前使用者與登出按鈕。
- **picker.html** & **upload.html**: 同步整合了權限檢查與 API 認證。

## 驗證結果

我執行了一個自動化測試腳本 `verify_auth.py`，驗證了以下情境：
- [x] 指定使用者註冊與登入流程。
- [x] 多使用者之間的配置數據完全隔離。
- [x] 未授權（無 Token）存取 API 會正確返回 401。

### 核心程式碼變更

#### [start-server-fastapi.py](file:///home/mimas/projects/viewpoints/start-server-fastapi.py)
加入認證依賴、使用者管理邏輯與受保護的路由。

#### [js/auth.js](file:///home/mimas/projects/viewpoints/js/auth.js)
核心認證邏輯與 `fetch` 封裝。

#### [login.html](file:///home/mimas/projects/viewpoints/login.html)
全新的使用者入口頁面。

## 如何開始使用
1. 確保已安裝新依賴：`uv pip install python-jose[cryptography] passlib`
2. 啟動伺服器：`uv run python3 start-server-fastapi.py`
3. 存取首頁，系統會引導您進行註冊。
