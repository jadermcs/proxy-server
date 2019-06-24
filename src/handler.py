import pathlib
import socketserver
import http.server
import threading
import requests
import utils

CACHE_FOLDER = 'cache/'

class ThreadedTCPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    pass

    # def handle(self):
    #     # self.request is the TCP socket connected to the client
    #     self.data = self.request.recv(1024)
    #     cur_thread = threading.current_thread()
    #     response = bytes("{}: {}".format(cur_thread.name, self.data), 'ascii')
    #     # self.logger.info("Requested host: %s", utils.get_host(self.data))
    #     print(response.decode('ascii'))
    #     # just send back the same data, but upper-cased
    #     self.request.send(self.data)


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_CONNECT(self):
        print(self.path)
        req = requests.get(self.path)
        # if not self.path.endswith(".html"):
        #     self.path = 'http://' + self.path.split(':')[0]
        #     self.path += '/index.html'

        # with open('index.html','w') as fout:
        #     fout.write(req.text)
        #     self.send_response(200)
            # self.send_header('Content type', value)
            # self.end_headers()
            # self.wfile.write(bytearray(f.read(), 'ascii'))
            # f.close()
        # else:
        #     self.send_error(404, "File not Found")

    def do_GET(self):
        # if self.path in self.blacklist:
        #     self.send_response(401, "Unauthorized domain.")
        # elif self.path in self.whitelist:
        #     self.send_response(200)
        req = requests.get(self.path)
        dirpath = self.path.lstrip('http://').split('/')
        filepath = '/'.join(dirpath[:-1])
        pathlib.Path(CACHE_FOLDER + filepath).mkdir(parents=True,
                                                    exist_ok=True)
        filename = '/index.html' if not dirpath[-1] else '/'+dirpath[-1]
        print(dirpath)
        print(CACHE_FOLDER + filepath + filename)
        with open(CACHE_FOLDER + filepath + filename, 'w') as fout:
            fout.write(req.text)
            # for k, v in req.headers.items():
            #     self.send_header(k, v)
            # self.send_header('Content type', 'text/html')
            # self.end_headers()
            self.wfile.write(bytearray(req.text, 'utf-8'))
            self.send_response(200)
