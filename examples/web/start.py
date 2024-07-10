#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from os import system, getlogin
from picar_4wd import getIPs

user_name = getlogin()

def start_http_server():
    system(f"cd /home/{user_name}/picar-4wd/examples/web/client && sudo python3 -m http.server 80 2>&1 1>/dev/null &")#开启服务器

def close_http_server():
    system("sudo kill $(ps aux | grep 'http.server' | awk '{ print $2 }') 2>&1 1>/dev/null")

def start_websocket():
    # print("start_websocket")
    system(f"cd /home/{user_name}/picar-4wd/examples/web/server && sudo python3 web_server.py 2>&1 1>/dev/null &")
    # system(f"cd /home/{user_name}/picar_4wd/examples/web/server && sudo python3 web_server.py &")

def close_websocket():
    # print("close_websocket")
    system("sudo kill $(ps aux | grep 'web_server.py' | awk '{ print $2 }') 2>&1 1>/dev/null")

class restartServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # print("do_get successed")
        if self.path == '/restart':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            # self.send_header("Content-Length", str(len(self.Page)))
            self.end_headers()
            close_websocket()
            start_websocket()
            # print("Restart websocket")
            self.wfile.write("OK".encode())
        else:
            print('error', self.path)
            self.send_response(200)
            self.send_header('Content-type', 'text/html'.encode())
            self.end_headers()
            self.wfile.write('<html><head></head><body>'.encode())
            self.wfile.write(
                '<h1>{0!s} not found</h1>'.format(self.path).encode())
            self.wfile.write('</body></html>'.encode())

if __name__ == '__main__':
    try:
        # soft_reset()
        for _ in range(10):
            ips = getIPs()
            if ips:
                break
            time.sleep(1)
        port = 9000
        start_http_server()
        start_websocket()
        urls = ["http://" + ip for ip in ips]
        print("Web example starts") 
        print(f"Open {' or '.join(urls)} in your web browser to control the car!") 
        server = HTTPServer((ips[0], port), restartServer)
        server.serve_forever()
      
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        print("Finished")
        server.socket.close()
        close_http_server()
        close_websocket()
