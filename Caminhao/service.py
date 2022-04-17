import json
from mysocket import SocketClient
from types import SimpleNamespace
from urllib.parse import urlencode


class Services:
    #Inicia conexão socket
    def __init__(self, server_host, port):
        self.mysocket = SocketClient(server_host, port)
        self.mysocket.start()
    
    #Fecha conexão    
    def close(self):
        self.mysocket.close_connection()

    #Método GET
    def GET(self, route, params):
        try:
            route = route + urlencode(params, doseq=True)
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
            resp = json.loads(resp.decode(
                'utf-8'), object_hook=lambda d: SimpleNamespace(**d))
            print("response: ", resp)
            return resp
        except Exception as e:
            self.mysocket.close_connection()
            self.mysocket.start()
            print("Error ao realizar a comunicação com o servidor. ", e.args)
            raise "Error ao realizar a comunicação com o servidor. "

    #Método POST
    def POST(self, route, body):
        try:
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
            resp_json = json.loads(resp.decode(
                'utf-8'), object_hook=lambda d: SimpleNamespace(**d))

            return resp_json
        except Exception as e:
            self.mysocket.close_connection()
            self.mysocket.start()
            print("Error ao realizar a comunicação com o servidor. ", e.args)
            raise "Error ao realizar a comunicação com o servidor. "
