#!/usr/bin/env python3
"""
監視器牆本地伺服器啟動腳本
使用 Python 內建的 HTTP 伺服器
"""

import http.server
import socketserver
import os
import webbrowser
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
PORT = int(os.environ.get("VIEWPOINTS_PORT", 8844))


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加 CORS 標頭，允許跨網域請求
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()


def main():
    # 切換到腳本所在目錄
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 允許立即重用連接埠，解決 TIME_WAIT 問題
    socketserver.TCPServer.allow_reuse_address = True
    Handler = MyHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}"
            print(f"=" * 60)
            print(f"監視器牆伺服器已啟動！")
            print(f"=" * 60)
            print(f"")
            print(f"存取位址: {url}")
            print(f"")
            print(f"按 Ctrl+C 停止伺服器")
            print(f"=" * 60)

            # 自動在瀏覽器中開啟
            try:
                webbrowser.open(url)
            except:
                pass

            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n")
        print("=" * 60)
        print("伺服器已停止")
        print("=" * 60)
        sys.exit(0)
    except OSError as e:
        if e.errno == 48 or e.errno == 98:  # Address already in use
            print(f"錯誤: 連接埠 {PORT} 已被佔用")
            print(f"請關閉佔用該連接埠的程式，或修改 .env 中的 VIEWPOINTS_PORT")
        else:
            print(f"錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
