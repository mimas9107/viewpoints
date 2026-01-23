#!/usr/bin/env python3
"""
Viewpoints 統一伺服器 (FastAPI 版本)

功能：
- 靜態文件服務 (index.html, picker.html, upload.html, css/, js/)
- Config API (讀取/儲存/下載/備份/恢復)

啟動方式：
    python3 start-server-fastapi.py
"""

import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext


class SPAStaticFiles(StaticFiles):
    async def __call__(self, scope, receive, send):
        try:
            response = await super().__call__(scope, receive, send)
            if (
                response is not None
                and hasattr(response, "status_code")
                and response.status_code == 404
            ):
                path = scope.get("path")
                if not path.startswith("/api/"):
                    scope["path"] = "/"
                    response = await super().__call__(scope, receive, send)
            return response
        except Exception:
            path = scope.get("path")
            if not path.startswith("/api/"):
                scope["path"] = "/"
                response = await super().__call__(scope, receive, send)
                return response
            raise


def load_env_file():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


load_env_file()

PORT = int(os.environ.get("VIEWPOINTS_PORT", 8844))
BASE_DIR = Path(__file__).parent.resolve()
CONFIG_FILE = BASE_DIR / "viewpoints.json"
USERS_FILE = BASE_DIR / "users.json"
BACKUP_DIR = BASE_DIR / ".backups"
MAX_BACKUPS = 10

# JWT Settings
SECRET_KEY = os.environ.get("SECRET_KEY", "viewpoints-secret-key-3000")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


class Camera(BaseModel):
    id: str
    name: str
    type: str
    imageUrl: Optional[str] = None
    youtubeId: Optional[str] = None
    hlsUrl: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None


class Config(BaseModel):
    title: str = "監控牆"
    autoRefresh: bool = True
    refreshInterval: int = 60
    layout: Optional[dict] = None
    cameras: List[Camera]


def validate_config(data: dict) -> bool:
    if not isinstance(data, dict):
        return False
    if "cameras" not in data:
        return False
    if not isinstance(data["cameras"], list):
        return False
    # 允許空相機列表
    return True


def get_user_config_file(username: str) -> Path:
    return BASE_DIR / f"viewpoints_{username}.json"


def load_users() -> dict:
    if not USERS_FILE.exists():
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token_header: Optional[str] = Depends(oauth2_scheme),
    token: Optional[str] = None
):
    # 如果 header 沒有 token，嘗試從 query params 獲取
    actual_token = token_header
    if not actual_token and token:
        actual_token = token

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not actual_token:
        raise credentials_exception
    try:
        payload = jwt.decode(actual_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


class UserAuth(BaseModel):
    username: str
    password: str


def create_backup(username: Optional[str] = None):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    target_file = get_user_config_file(username) if username else CONFIG_FILE
    
    if not target_file.exists():
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = f"viewpoints_{username}_" if username else "viewpoints_"
    backup_filename = f"{prefix}{timestamp}_{uuid.uuid4().hex[:8]}.json"
    backup_path = BACKUP_DIR / backup_filename

    shutil.copy2(target_file, backup_path)

    backups = sorted(
        [
            f
            for f in os.listdir(BACKUP_DIR)
            if f.startswith("viewpoints_") and f.endswith(".json")
        ]
    )

    while len(backups) > MAX_BACKUPS:
        oldest = backups.pop(0)
        try:
            (BACKUP_DIR / oldest).unlink()
        except:
            pass


app = FastAPI(
    title="Viewpoints API", description="監視器牆配置管理 API", version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Auth API ---

@app.post("/api/auth/register")
def register(user: UserAuth):
    users = load_users()
    if user.username in users:
        raise HTTPException(status_code=400, detail="使用者名稱已存在")
    
    users[user.username] = {
        "password": get_password_hash(user.password),
        "created_at": datetime.now().isoformat()
    }
    save_users(users)
    return {"success": True, "message": "註冊成功"}


@app.post("/api/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users = load_users()
    user = users.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="帳號或密碼錯誤",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer", "username": form_data.username}


@app.get("/api/auth/me")
def get_me(username: str = Depends(get_current_user)):
    return {"username": username}


# --- Config API ---


@app.get("/api/config")
def get_config(username: str = Depends(get_current_user)):
    try:
        user_config = get_user_config_file(username)
        if not user_config.exists():
            # 回傳預設配置
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {"title": "我的監視器牆", "cameras": [], "autoRefresh": True, "refreshInterval": 60}

        with open(user_config, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/api/config")
def save_config(config: dict, username: str = Depends(get_current_user)):
    try:
        if not validate_config(config):
            return JSONResponse(
                content={"error": "配置文件格式驗證失敗"}, status_code=400
            )

        create_backup(username)

        user_config = get_user_config_file(username)
        with open(user_config, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "message": "配置已儲存",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.head("/api/config/download")
def download_config_head():
    if not CONFIG_FILE.exists():
        return JSONResponse(content={"error": "配置文件不存在"}, status_code=404)
    return Response(status_code=200)


@app.get("/api/config/download")
def download_config(username: str = Depends(get_current_user)):
    try:
        user_config = get_user_config_file(username)
        if not user_config.exists():
            return JSONResponse(content={"error": "配置文件不存在"}, status_code=404)

        with open(user_config, "r", encoding="utf-8") as f:
            content = f.read()

        return Response(
            content=content,
            media_type="application/json",
            headers={
                "Content-Disposition": f'attachment; filename="viewpoints_{username}.json"',
            },
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/api/config/backups")
def list_backups(username: str = Depends(get_current_user)):
    try:
        if not BACKUP_DIR.exists():
            return {"backups": []}

        backups = []
        prefix = f"viewpoints_{username}_"
        for f in os.listdir(BACKUP_DIR):
            if f.startswith(prefix) and f.endswith(".json"):
                filepath = BACKUP_DIR / f
                stat = filepath.stat()
                backups.append(
                    {
                        "filename": f,
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    }
                )

        backups.sort(key=lambda x: x["modified"], reverse=True)
        return {"backups": backups}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/api/config/backups/{filename}/restore")
def restore_backup(filename: str, username: str = Depends(get_current_user)):
    try:
        if not filename.endswith(".json"):
            filename += ".json"

        # 安全性檢查：確保檔名屬於該使用者
        if not filename.startswith(f"viewpoints_{username}_"):
            raise HTTPException(status_code=403, detail="無權存取此備份檔")

        backup_path = BACKUP_DIR / filename

        if not backup_path.exists():
            return JSONResponse(content={"error": "備份檔案不存在"}, status_code=404)

        with open(backup_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not validate_config(data):
            return JSONResponse(
                content={"error": "備份檔案格式驗證失敗"}, status_code=400
            )

        create_backup(username)

        user_config = get_user_config_file(username)
        with open(user_config, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "message": f"已從 {filename} 復原",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        return JSONResponse(content={"error": str(e)}, status_code=500)


app.mount("/", SPAStaticFiles(directory=str(BASE_DIR), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("Viewpoints 統一伺服器 (FastAPI 版本)")
    print("=" * 60)
    print("")
    print(f"存取位址: http://localhost:{PORT}")
    print("")
    print("頁面：")
    print(f"  - 監控牆:     http://localhost:{PORT}/")
    print(f"  - 選擇器:     http://localhost:{PORT}/picker.html")
    print(f"  - 上傳配置:   http://localhost:{PORT}/upload.html")
    print("")
    print("API：")
    print(f"  - GET    /api/config                 - 讀取配置")
    print(f"  - POST   /api/config                 - 儲存配置")
    print(f"  - GET    /api/config/download        - 下載配置")
    print(f"  - GET    /api/config/backups         - 列出備份")
    print(f"  - POST   /api/config/backups/{{name}}/restore - 恢復備份")
    print("")
    print("按 Ctrl+C 停止伺服器")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=PORT)
