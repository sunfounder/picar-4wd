#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from os import system, getlogin

user_name = getlogin()

def start_http_server():
    print(f'start http server')
    system(f"cd /home/{user_name}/picar-4wd/examples/web/client && sudo python3 -m http.server 80 2>&1 1>/dev/null &")#开启服务器

def close_http_server():
    print('closing http server')
    system("sudo kill $(ps aux | grep 'http.server' | awk '{ print $2 }') 2>&1 1>/dev/null")

def start_websocket():
    print(f'start websocket server')
    system(f"cd /home/{user_name}/picar-4wd/examples/web/server && sudo python3 web_server.py 2>&1 1>/dev/null &")

def close_websocket():
    print('closing websocket server')
    system("sudo kill $(ps aux | grep 'web_server.py' | awk '{ print $2 }') 2>&1 1>/dev/null")

if __name__ == "__main__":
    start_http_server()
    