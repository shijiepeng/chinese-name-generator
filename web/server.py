#!/usr/bin/env python3
"""
简单的 HTTP 服务器，用于运行姓名生成器 Web 界面
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8080
WEB_DIR = Path(__file__).parent

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(WEB_DIR)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 服务器启动成功！")
        print(f"📍 访问地址: http://localhost:{PORT}")
        print(f"🛑 按 Ctrl+C 停止服务器")
        print("-" * 50)
        httpd.serve_forever()
