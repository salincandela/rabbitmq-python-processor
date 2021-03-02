import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from util.task_args import get_healthcheck_port

class HttpHealthServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == '/actuator/health') or (self.path == '/actuator/info'):
            self.send_ok_response()
        else:
            self.send_missing_response()

        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def send_ok_response(self):
        self.send_response(200)

    def send_missing_response(self):
        self.send_response(404)

    @staticmethod
    def run_thread(port=int(get_healthcheck_port())):
        http_server = HTTPServer(('', port), HttpHealthServer)
        thread = threading.Thread(name='httpd_server', target=http_server.serve_forever)
        thread.setDaemon(True)
        thread.start()