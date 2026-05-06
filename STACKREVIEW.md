Viewpoints 登入登出管理權限技術堆疊分析
前端認證實作 (auth.js)
- 技術: Vanilla JavaScript ES6 模組
- 儲存機制: localStorage (viewpoints_token, viewpoints_username)
- 認證流程: 
  - 登入/註冊透過 /api/auth/login 和 /api/auth/register 端點
  - 自動在API請求中加入 Authorization: Bearer <token> header
  - 401錯誤自動導向登出並重新導向至登入頁
- 介面: login.html 提供登入/註冊切換表單，使用CSS授權玻璃效果
後端認證實作 (start-server-fastapi.py)
- 框架: FastAPI (現代、高效Python Web框架)
- 認證標準: JWT (JSON Web Token) 使用 HS256 演算法
- 密碼安全: 
  - Passlib 的 pbkdf2_sha256 帶鹽雜湊
  - 29,000 次迭代 (符合現代安全標準)
- 使用者儲存: users.json 檔案（開發/小規模使用適當）
- API端點:
  - POST /api/auth/register - 使用者註冊
  - POST /api/auth/login - 取得JWT token (7天有效期)
  - GET /api/auth/me - 取得目前使用者資訊
- 安全機制: OAuth2PasswordBearer 標準實作
權限管理現狀
目前系統缺乏正式的角色基礎存取控制(RBAC):
1. 使用者隔離透過檔案: 每個使用者有專屬 viewpoints_{username}.json 配置檔案
2. 統一權限: 所有經認證使用者擁有相同權限（讀寫自己的配置）
3. 無角色區分: 沒有管理員/一般使用者之別
4. 無細緻權限: 無法設定特定監控點或功能的存取權限
技術堆疊優勢
- ✅ 現代標準：JWT + bcrypt-style密碼雜湊
- ✅ 前後端分離：清晰的API介面
- ✅ 無狀態認證：適合水平擴展
- ✅ 輕量級部署：單一Python檔案實作
- ✅ CORS支援：允許跨域前端請求
改進方向思考
若要增強權限管理，可考慮：
1. 角色基礎存取控制(RBAC):
   - 新增角色欄位 (admin/user) 在 users.json 中
   - 在後端API加入角色檢查 decorator
   - 前端根據角色顯示/隱藏功能
2. 細緻權限系統:
   - 權限資源: 監控點ID、功能模組
   - 權限類型: 讀取、寫入、刪除
   - 使用權限矩陣或ACL（存取控制清單）
3. 進階會話管理:
   - Refresh token 機制延長會話
   - 會話失效清單（登出所有裝置）
   - 異地登入偵測
4. 監控與審計:
   - 登入/失敗登入記錄
   - 權限變更審計追蹤
   - 異常行為警報機制
這個基礎實作其實相當堅固，使用了業界最佳實踐。主要的改進空間在於將權限從簡單的使用者隔離提升到正式的角色和資源基礎存取控制。
