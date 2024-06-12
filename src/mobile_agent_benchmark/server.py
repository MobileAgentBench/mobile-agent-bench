from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
from enum import Enum

class AppEventType(Enum):
    Unknown = 0
    Click = 1
    WindowStateChange = 2

class AppEvent:
    def __init__(self):
        self.type = AppEventType.Unknown
        self.package = ''
        self.id_str = ''
        self.content_desc = ''
        self.text_list = []
    
    def __str__(self) -> str:
        return f"Event - type: {self.type}, id_str: '{self.id_str}', content_desc: '{self.content_desc}', text_list: {self.text_list}, package: {self.package}"

def request_handler_class(callback_fn):
    class HTTPRequestHandler(BaseHTTPRequestHandler):
        def _set_response(self):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

        def log_message(self, format, *args):
            # disable default log prints
            pass

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])  # Gets the size of data
            post_data = self.rfile.read(content_length)  # Gets the data itself
            data = json.loads(post_data.decode('utf-8'))  # Decode and load JSON data

            event = AppEvent()
            type = data['eventType']
            if type == 0:
                event.type = AppEventType.Click
            elif type == 1:
                event.type = AppEventType.WindowStateChange
            
            event.package = data['packageStr']
            event.id_str = data['idStr']
            event.text_list = data['text']
            event.content_desc = data['contentDescription'] if data['contentDescription'] != 'null' else ''

            # Print received JSON data
            print("Received:", event)
            callback_fn(event)

            # Send response back to client
            self._set_response()
            response = {'status': 'OK'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

    return HTTPRequestHandler

def run(callback_fn, server_class=HTTPServer, port=8888):
    server_address = ('', port)
    handler_class=request_handler_class(callback_fn)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {port}")
    httpd.serve_forever()

def start_server(callback_fn):
    server_thread = threading.Thread(target=run, args=(callback_fn,))
    server_thread.daemon = True  # Daemonize thread
    server_thread.start()
    print("Server started in a background thread.")