import socket
import json


class Lixeira():

    def __init__(self, id, server_host, port, x, y, capacity):
        self.__id = id
        self.__server_host = server_host
        self.__port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__status = True
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



    def ___send_message(self):
        try:
            #self.__tcp.send(bytes(str(msg),'utf-8'))
            data = json.dumps({"topic":"lixeira","id":self.__id,"host":self.my_host,"port":self.my_port,"status":self.__status,"coords":self.__coords,"capacity":self.__capacity,"qtd_used":self.__qtd_used})
            self.__tcp.send(bytes(data,'utf-8'))
            resp = self.__tcp.recv(2048)
            print("= ", resp.decode('utf-8'))
        except Exception as e:
            print("Error ao realizar a comunicação com o servidor. ", e.args)

    def close_connection(self):
        self.__tcp.close()

    def set_trash(self,qtd):
        self.__qtd_used += qtd
        if self.__qtd_used < 0:
            self.__qtd_used = 0
        self.___send_message()

    def get_trash(self):
        if self.__qtd_used > 0:
            return (self.__qtd_used/self.__capacity)*100
        else:
            return 0   

    def set_state(self,status):
        self.__status = status

    def get_state(self):
        return self.__status

    def get_capacity(self):
        return self.__capacity 




