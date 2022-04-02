import socket
import json


class Caminhao():

    def __init__(self, server_host, port, x, y, capacity):
        self.__server_host = server_host
        self.__port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__coords = (x,y)
        self.__capacity = capacity
        self.__qtd_used = 0

    def start(self):
        endpoint = (self.__server_host, self.__port)
        try:
            self.__tcp.connect(endpoint)
            self.my_host, self.my_port = self.__tcp.getsockname()
            print('Conexão realizada com sucesso!')
            return 'Conexão realizada!'
        except Exception as e:
            print("Error na conexão com o servidor. ", e.args)
            return 'Error na conexão com o servidor.'

    def ___send_message(self,msg):
        try:
            self.__tcp.send(bytes(str(msg),'ascii'))
            resp = self.__tcp.recv(2048)
            print("= ", resp.decode('ascii'))
        except Exception as e:
            print("Error ao realizar a comunicação com o servidor. ", e.args)

    def close_connection(self):
        self.__tcp.close()

    def set_trash(self,qtd):
        self.__qtd_used += qtd
        if self.__qtd_used < 0:
            self.__qtd_used = 0
        self.___send_message(self.__qtd_used)

    def get_trash(self):
        if self.__qtd_used > 0:
            return (self.__qtd_used/self.__capacity)*100
        else:
            return 0   

    def get_capacity(self):
        return self.__capacity 

    def POST(self, msg):
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

    def get_list_trash(self, req):
        try:
            headers = "GET /list-trash HTTP/1.1\rContent-Type: {content_type}\rHost: {host}\rParams: {params}\rConnection: close\r\r\n "            
            header_bytes = headers.format(
                content_type="application/json",
                params=req,
                host=str(self.__server_host) + ":" + str(self.__port)
            ).encode('iso-8859-1')
            payload = header_bytes
            print(payload)
            self.__tcp.send(payload)
            resp = self.__tcp.recv(2048)
            #print("= ", resp.decode('utf-8'))
            data_json = json.loads(resp)
            return data_json
        except Exception as e:
            print("Error ao realizar a comunicação com o servidor. ", e.args)




