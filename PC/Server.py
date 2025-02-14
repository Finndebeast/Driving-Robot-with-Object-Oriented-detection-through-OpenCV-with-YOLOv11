import socketserver, subprocess, sys
from threading import Thread
from pprint import pprint
import json
import Analyzing

HOST = "0.0.0.0"
PORT = "[Any port]"


class SingleTCPHandler(socketserver.BaseRequestHandler):
    # One instance per connection.

    def handle(self):
        connection = self.request
        Analyzing.handle_connection(connection)
        connection.close()


class SimpleServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
