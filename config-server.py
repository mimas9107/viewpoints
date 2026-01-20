#!/usr/bin/env python3
"""
配置管理伺服器 - Viewpoints
提供 REST API 讓前端讀取/寫入 viewpoints.json
"""

import http.server
import socketserver
import json
import os
import shutil
import uuid
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import sys

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
PORT = int(os.environ.get("VIEWPOINTS_CONFIG_PORT", 8845))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "viewpoints.json")
BACKUP_DIR = os.path.join(BASE_DIR, ".backups")


class ConfigAPIHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/":
            self.serve_upload_page()
        elif path == "/api/config":
            self.get_config()
        elif path == "/api/config/download":
            self.download_config()
        elif path == "/api/config/backup":
            self.list_backups()
        elif path.startswith("/api/config/restore/"):
            self.restore_backup(path.split("/")[-1])
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/config":
            self.save_config()
        else:
            self.send_error(404, "Not Found")

    def get_config(self):
        try:
            if not os.path.exists(CONFIG_FILE):
                self.send_json_response({"error": "配置文件不存在"}, 404)
                return

            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.send_json_response(data)
        except json.JSONDecodeError:
            self.send_json_response({"error": "配置文件格式錯誤"}, 500)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def save_config(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8"))

            if not self.validate_config(data):
                self.send_json_response({"error": "配置文件格式驗證失敗"}, 400)
                return

            self.create_backup()

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.send_json_response(
                {
                    "success": True,
                    "message": "配置已儲存",
                    "timestamp": datetime.now().isoformat(),
                }
            )
        except json.JSONDecodeError:
            self.send_json_response({"error": "無效的 JSON 格式"}, 400)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def validate_config(self, data):
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

    def create_backup(self):
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

        if not os.path.exists(CONFIG_FILE):
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"viewpoints_{timestamp}_{uuid.uuid4().hex[:8]}.json"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)

        shutil.copy2(CONFIG_FILE, backup_path)

        max_backups = 10
        backups = sorted(
            [
                f
                for f in os.listdir(BACKUP_DIR)
                if f.startswith("viewpoints_") and f.endswith(".json")
            ]
        )

        while len(backups) > max_backups:
            oldest = backups.pop(0)
            try:
                os.remove(os.path.join(BACKUP_DIR, oldest))
            except:
                pass

    def list_backups(self):
        try:
            if not os.path.exists(BACKUP_DIR):
                self.send_json_response({"backups": []})
                return

            backups = []
            for f in os.listdir(BACKUP_DIR):
                if f.startswith("viewpoints_") and f.endswith(".json"):
                    filepath = os.path.join(BACKUP_DIR, f)
                    stat = os.stat(filepath)
                    backups.append(
                        {
                            "filename": f,
                            "size": stat.st_size,
                            "modified": datetime.fromtimestamp(
                                stat.st_mtime
                            ).isoformat(),
                        }
                    )

            backups.sort(key=lambda x: x["modified"], reverse=True)
            self.send_json_response({"backups": backups})
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def restore_backup(self, filename):
        try:
            if not filename.endswith(".json"):
                filename += ".json"

            backup_path = os.path.join(BACKUP_DIR, filename)

            if not os.path.exists(backup_path):
                self.send_json_response({"error": "備份檔案不存在"}, 404)
                return

            with open(backup_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not self.validate_config(data):
                self.send_json_response({"error": "備份檔案格式驗證失敗"}, 400)
                return

            self.create_backup()

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.send_json_response(
                {
                    "success": True,
                    "message": f"已從 {filename} 復原",
                    "timestamp": datetime.now().isoformat(),
                }
            )
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def download_config(self):
        try:
            if not os.path.exists(CONFIG_FILE):
                self.send_error(404, "配置文件不存在")
                return

            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header(
                "Content-Disposition", 'attachment; filename="viewpoints.json"'
            )
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        except Exception as e:
            self.send_error(500, str(e))

    def serve_upload_page(self):
        html = """<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>上傳配置 - Viewpoints</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans TC", sans-serif;
            background: linear-gradient(135deg, #1a1a1b 0%, #2d2d2e 100%);
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: #2d2d2e;
            border-radius: 16px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }
        h1 { text-align: center; margin-bottom: 30px; font-size: 28px; }
        .upload-area {
            border: 3px dashed #4a4a4b;
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            margin-bottom: 20px;
            transition: all 0.3s;
            cursor: pointer;
        }
        .upload-area:hover, .upload-area.dragover {
            border-color: #0066cc;
            background: rgba(0,102,204,0.1);
        }
        .upload-icon { font-size: 48px; margin-bottom: 15px; }
        .upload-text { color: #aaa; margin-bottom: 10px; }
        #fileInput { display: none; }
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 10px;
            transition: all 0.2s;
        }
        .btn-primary { background: #00cc66; color: white; }
        .btn-primary:hover { background: #00dd77; }
        .btn-secondary { background: #0066cc; color: white; }
        .btn-secondary:hover { background: #0077dd; }
        .btn-outline { background: transparent; border: 2px solid #4a4a4b; color: #aaa; }
        .btn-outline:hover { border-color: #fff; color: #fff; }
        #status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            display: none;
        }
        .status-success { background: rgba(0,204,102,0.2); color: #00cc66; }
        .status-error { background: rgba(255,68,68,0.2); color: #ff4444; }
        .nav-links {
            margin-top: 30px;
            text-align: center;
        }
        .nav-links a {
            color: #0066cc;
            text-decoration: none;
            margin: 0 10px;
        }
        .nav-links a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📤 上傳配置檔案</h1>
        <div class="upload-area" id="uploadArea">
            <div class="upload-icon">📁</div>
            <div class="upload-text">點擊或拖曳 JSON 檔案到此處</div>
            <div style="color: #666; font-size: 12px;">支援 .json 檔案</div>
        </div>
        <input type="file" id="fileInput" accept=".json">

        <button class="btn btn-primary" onclick="uploadFile()">🚀 上傳並套用</button>
        <button class="btn btn-secondary" onclick="downloadConfig()">⬇️ 下載目前配置</button>
        <button class="btn btn-outline" onclick="showBackups()">📋 檢視備份</button>

        <div id="status"></div>

        <div class="nav-links">
            <a href="index.html">🏠 回監控牆</a>
            <a href="picker.html">📺 選擇器</a>
        </div>
    </div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        let selectedFile = null;

        uploadArea.onclick = () => fileInput.click();

        uploadArea.ondragover = (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        };

        uploadArea.ondragleave = () => uploadArea.classList.remove('dragover');

        uploadArea.ondrop = (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                handleFile(e.dataTransfer.files[0]);
            }
        };

        fileInput.onchange = (e) => {
            if (e.target.files.length) {
                handleFile(e.target.files[0]);
            }
        };

        function handleFile(file) {
            if (!file.name.endsWith('.json')) {
                showStatus('僅支援 JSON 檔案', 'error');
                return;
            }
            selectedFile = file;
            uploadArea.querySelector('.upload-text').textContent = `已選擇: ${file.name}`;
            uploadArea.style.borderColor = '#00cc66';
        }

        async function uploadFile() {
            if (!selectedFile) {
                showStatus('請先選擇一個 JSON 檔案', 'error');
                return;
            }

            try {
                const text = await selectedFile.text();
                const json = JSON.parse(text);

                const response = await fetch('/api/config', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(json)
                });

                const result = await response.json();

                if (response.ok) {
                    showStatus('✅ 配置已成功上傳並套用！', 'success');
                } else {
                    showStatus('❌ ' + (result.error || '上傳失敗'), 'error');
                }
            } catch (e) {
                showStatus('❌ JSON 格式錯誤: ' + e.message, 'error');
            }
        }

        async function downloadConfig() {
            window.location.href = '/api/config/download';
        }

        async function showBackups() {
            const response = await fetch('/api/config/backup');
            const result = await response.json();
            alert('備份功能開發中，可直接聯絡管理員');
        }

        function showStatus(msg, type) {
            const el = document.getElementById('status');
            el.textContent = msg;
            el.className = 'status-' + type;
            el.style.display = 'block';
        }
    </script>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(html))
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def send_json_response(self, data, status=200):
        content = json.dumps(data, ensure_ascii=False, indent=2)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


def main():
    os.chdir(BASE_DIR)

    socketserver.TCPServer.allow_reuse_address = True
    Handler = ConfigAPIHandler

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}"
            print("=" * 60)
            print("配置管理伺服器已啟動！")
            print("=" * 60)
            print("")
            print(f"管理介面: {url}")
            print(f"API 端點:")
            print(f"  GET  {url}/api/config       - 讀取配置")
            print(f"  POST {url}/api/config       - 儲存配置")
            print(f"  GET  {url}/api/config/download - 下載配置")
            print(f"  GET  {url}/api/config/backup  - 列出備份")
            print("")
            print("按 Ctrl+C 停止伺服器")
            print("=" * 60)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n伺服器已停止")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48 or e.errno == 98:
            print(f"錯誤: 連接埠 {PORT} 已被佔用")
            print(f"請關閉佔用該連接埠的程式，或修改 .env 中的 VIEWPOINTS_CONFIG_PORT")
        else:
            print(f"錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
