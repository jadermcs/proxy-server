import socketserver
import threading
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import utils

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        sender = requests.Session()
        retries = Retry(total=3, backoff_factor=1)
        self.data = self.request.recv(1024).strip().decode('ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, self.data), 'ascii')
        # self.logger.info("Requested host: %s", utils.get_host(self.data))
        print(response.decode('ascii'))
        # just send back the same data, but upper-cased
        q = requests.Request('GET', 'https://jader.ml')
        sender.mount('http://', HTTPAdapter(max_retries=retries))
        sender.send(q.prepare())
        self.request.sendall(sender.response())
