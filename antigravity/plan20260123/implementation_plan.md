# 實作計畫 - 使用者權限控制與個人化監視牆

本計畫旨在為 Viewpoints 專案加入使用者系統，讓不同使用者能擁有各自獨立的 `viewpoints.json` 配置。

## Proposed Changes

### [Backend] FastAPI Server (start-server-fastapi.py)

#### [MODIFY] [start-server-fastapi.py](file:///home/mimas/projects/viewpoints/start-server-fastapi.py)
- **新增使用者資料管理**: 使用 `users.json` 儲存使用者資訊（帳號、加密後密碼）。
- **新增認證 API**:
  - `POST /api/auth/register`: 註冊新使用者。
  - `POST /api/auth/login`: 驗證使用者並回傳 JWT Token。
- **修改配置 API**:
  - 更新所有 `/api/config/*` 路由，加入 `Depends(get_current_user)` 驗證。
  - 根據目前登入的使用者，讀取/儲存對應的 `viewpoints_<username>.json`。
  - 若檔案不存在，則以 `viewpoints.json.template` (或原 `viewpoints.json`) 為範本建立。

### [Frontend] Authentication & UI

#### [NEW] [login.html](file:///home/mimas/projects/viewpoints/login.html)
- 建立現代化且美觀的登入與註冊介面。

#### [NEW] [js/auth.js](file:///home/mimas/projects/viewpoints/js/auth.js)
- 實作 Token 管理（存入 `localStorage`）。
- 實作登入狀態檢查函數。
- 實作 API 請求攔截或包裝，自動加入 `Authorization` Header。

#### [MODIFY] [js/config.js](file:///home/mimas/projects/viewpoints/js/config.js)
- 修改 `fetchConfig` 以包含 JWT Token。
- 處理 401 Unauthorized 錯誤，導向至登入頁。

#### [MODIFY] [index.html](file:///home/mimas/projects/viewpoints/index.html)
- 在進入頁面時呼叫 `js/auth.js` 檢查登入狀態。
- 介面更新：顯示目前登入使用者名稱，並加入「登出」按鈕。

#### [MODIFY] [picker.html](file:///home/mimas/projects/viewpoints/picker.html) & [upload.html](file:///home/mimas/projects/viewpoints/upload.html)
- 加入登入狀態檢查。

## Verification Plan

### Automated Tests
- 使用 Python 腳本測試 `/api/auth/register` 與 `/api/auth/login`。
- 測試使用過期或無效 Token 存取 `/api/config` 應回傳 401。

### Manual Verification
1.  **登入流程**: 訪問首頁，應自動重新導向至 `login.html`。
2.  **使用者隔離**:
    - 使用 `user1` 登入，修改監控牆配置並儲存。
    - 使用 `user2` 登入，應看到預設配置（與 `user1` 不同）。
    - 切換回 `user1`，原先修改的配置應依然存在。
3.  **登出功能**: 點擊登出後，應無法再存取主頁面且 Token 被清除。
