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

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


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
BACKUP_DIR = BASE_DIR / ".backups"
MAX_BACKUPS = 10


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
    for cam in data["cameras"]:
        if "id" not in cam or "name" not in cam or "type" not in cam:
            return False
    return True


def create_backup():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"viewpoints_{timestamp}_{uuid.uuid4().hex[:8]}.json"
    backup_path = BACKUP_DIR / backup_filename

    shutil.copy2(CONFIG_FILE, backup_path)

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


@app.get("/api/config")
def get_config():
    try:
        if not CONFIG_FILE.exists():
            return JSONResponse(content={"error": "配置文件不存在"}, status_code=404)

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data
    except json.JSONDecodeError:
        return JSONResponse(content={"error": "配置文件格式錯誤"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/api/config")
def save_config(config: dict):
    try:
        if not validate_config(config):
            return JSONResponse(
                content={"error": "配置文件格式驗證失敗"}, status_code=400
            )

        create_backup()

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "message": "配置已儲存",
            "timestamp": datetime.now().isoformat(),
        }
    except json.JSONDecodeError:
        return JSONResponse(content={"error": "無效的 JSON 格式"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.head("/api/config/download")
def download_config_head():
    if not CONFIG_FILE.exists():
        return JSONResponse(content={"error": "配置文件不存在"}, status_code=404)
    return Response(status_code=200)


@app.get("/api/config/download")
def download_config():
    try:
        if not CONFIG_FILE.exists():
            return JSONResponse(content={"error": "配置文件不存在"}, status_code=404)

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        return Response(
            content=content,
            media_type="application/json",
            headers={
                "Content-Disposition": 'attachment; filename="viewpoints.json"',
            },
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/api/config/backups")
def list_backups():
    try:
        if not BACKUP_DIR.exists():
            return {"backups": []}

        backups = []
        for f in os.listdir(BACKUP_DIR):
            if f.startswith("viewpoints_") and f.endswith(".json"):
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
def restore_backup(filename: str):
    try:
        if not filename.endswith(".json"):
            filename += ".json"

        backup_path = BACKUP_DIR / filename

        if not backup_path.exists():
            return JSONResponse(content={"error": "備份檔案不存在"}, status_code=404)

        with open(backup_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not validate_config(data):
            return JSONResponse(
                content={"error": "備份檔案格式驗證失敗"}, status_code=400
            )

        create_backup()

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "message": f"已從 {filename} 復原",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
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
