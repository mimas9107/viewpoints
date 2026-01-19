#!/usr/bin/env python3
"""
监视器墙本地服务器启动脚本
使用 Python 内置的 HTTP 服务器
"""

import http.server
import socketserver
import os
import webbrowser
import sys

PORT = 8000


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加 CORS 头，允许跨域请求
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()


def main():
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    Handler = MyHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}"
            print(f"=" * 60)
            print(f"监视器墙服务器已启动！")
            print(f"=" * 60)
            print(f"")
            print(f"访问地址: {url}")
            print(f"")
            print(f"按 Ctrl+C 停止服务器")
            print(f"=" * 60)

            # 自动在浏览器中打开
            try:
                webbrowser.open(url)
            except:
                pass

            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n")
        print("=" * 60)
        print("服务器已停止")
        print("=" * 60)
        sys.exit(0)
    except OSError as e:
        if e.errno == 48 or e.errno == 98:  # Address already in use
            print(f"错误: 端口 {PORT} 已被占用")
            print(f"请关闭占用该端口的程序，或修改脚本中的 PORT 变量")
        else:
            print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
