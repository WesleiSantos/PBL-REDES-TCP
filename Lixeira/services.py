import json
from mysocket import SocketClient
from types import SimpleNamespace
from urllib.parse import urlencode

class Services:
    def __init__(self, server_host, port):
        self.mysocket = SocketClient(server_host, port)

    def GET(self, route, params):
        try:
            self.mysocket.start()
            route = route + urlencode(params, doseq=True)
            print(route)
            headers = "GET {route} HTTP/1.1\rContent-Type: {content_type}\rHost: {host}\rConnection: close\r\r\n"
            header_bytes = headers.format(
                content_type="application/json",
                route=route,
                host=str(self.mysocket.get_host()) +
                ":" + str(self.mysocket.get_port())
            ).encode('iso-8859-1')
            payload = header_bytes
            print(payload)
            resp = self.mysocket.send_message(payload)
            self.mysocket.close_connection()
            resp = json.loads(resp.decode(
                'utf-8'), object_hook=lambda d: SimpleNamespace(**d))
            return resp
        except Exception as e:
            print("Error ao realizar a comunicação com o servidor. ", e.args)
            raise "Error ao realizar a comunicação com o servidor. "

    def POST(self, route, body):
        try:
            self.mysocket.start()
            headers = "POST {route} HTTP/1.1\rContent-Type: {content_type}\rContent-Length: {content_length}\rHost: {host}\rConnection: close\r\r\n "
            body_bytes = body.encode('utf-8')
            header_bytes = headers.format(
                route=route,
                content_type="application/json",
                content_length=len(body_bytes),
                host=str(self.mysocket.get_host()) + ":" +
                str(self.mysocket.get_port())
            ).encode('iso-8859-1')
            payload = header_bytes + body_bytes
            print(payload)
            resp = self.mysocket.send_message(payload)
            self.mysocket.close_connection()
            resp_json = json.loads(resp.decode(
                'utf-8'), object_hook=lambda d: SimpleNamespace(**d))

            return resp_json
        except Exception as e:
            print("Error ao realizar a comunicação com o servidor. ", e.args)
            raise "Error ao realizar a comunicação com o servidor. "