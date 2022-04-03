import socket
import json

class service:
    
    def __init__(self, server_host, port):
        self.__server_host = server_host
        self.__port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    

    def GET():

    def POST(msg):
        try:
            headers = "POST /desactive-trash HTTP/1.1\rContent-Type: {content_type}\rContent-Length: {content_length}\rHost: {host}\rConnection: close\r\r\n "
            body = msg
            body_bytes = body.encode('utf-8')
            header_bytes = headers.format(
                content_type="application/json",
                content_length=len(body_bytes),
                host=str(self.__server_host) + ":" + str(self.__port)
            ).encode('iso-8859-1')
            payload = header_bytes + body_bytes
            print(payload)
            self.__tcp.send(payload)
            resp = self.__tcp.recv(2048)
            print("= ", resp.decode('utf-8'))
        except Exception as e:
            print("Error ao realizar a comunicação com o servidor. ", e.args)
    
    def PUT():
