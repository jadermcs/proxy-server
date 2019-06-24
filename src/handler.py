import pathlib
import select
import http.server
import http.client
import socketserver
import socket
import threading
import requests
import utils

CACHE_FOLDER = 'cache/'


class ProxyHandler(socketserver.ThreadingMixIn,
                   http.server.SimpleHTTPRequestHandler):
    def do_CONNECT(self):
        self.log_request(200)
        self.wfile.write(bytearray(self.protocol_version +
                                   " 200 Connection established\r\n", "ascii"))
        self.wfile.write(bytearray("Proxy-agent: %s\r\n" %
                                   self.version_string(), "ascii"))
        self.wfile.write(b"\r\n")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host, port = self.path.split(':')
        port = int(port)
        s.connect((host, port))
        self.turn_to(s, 900)
        s.close()
        self.connection.close()
        # print(self.requestline)
        # conn = http.client.HTTPSConnection(self.path)
        # conn.request("GET", "/css?family=IBM+Plex+Mono:400,700")
        # r1 = conn.getresponse()
        # self.send_response(r1.status)
        # conn.close()

    def do_GET(self):
        # if self.path in self.blacklist:
        #     self.send_response(401, "Unauthorized domain.")
        # elif self.path in self.whitelist:
        #     self.send_response(200)
        req = requests.get(self.path, stream=True)
        dirpath = self.path.lstrip('http://').split('/')
        filepath = '/'.join(dirpath[:-1])
        pathlib.Path(CACHE_FOLDER + filepath).mkdir(parents=True,
                                                    exist_ok=True)
        filename = '/index.html' if not dirpath[-1] else '/'+dirpath[-1]
        with open(CACHE_FOLDER + filepath + filename, 'wb') as fout:
            for chunk in req.iter_content(1024):
                fout.write(chunk)
        with open(CACHE_FOLDER + filepath + filename, 'rb') as fin:
            self.wfile.write(fin.read())
            self.send_response(200)


    def turn_to(self, s, timeout = 60):
        iw = [self.connection, s]
        ow = []
        time = 0
        while time < timeout:
            time += 1
            (ins, _, exs) = select.select(iw, ow, iw, 1)
            if exs: #exception
                break
            elif ins: #input readable
                for i in ins:
                    if i is s:
                        o = self.connection
                    elif i is self.connection:
                        o = s
                    else:
                        pass
                    try:
                        data = i.recv(8192)
                    except:
                        data = None
                    if data:
                        o.send(data)
                        time = 0
                    else:
                        pass
            else: # output readable
                pass
