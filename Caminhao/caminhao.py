import socket


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




