import socket


class SocketClient:
    def __init__(self, server_host, port):
        self.__server_host = server_host
        self.__port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    def send_message(self, msg):
        try:
            print("veio4")
            self.__tcp.send(msg)
            resp = self.__tcp.recv(2048)
            return resp
        except Exception as e:
            print("Error ao realizar a comunicação com o servidor. ", e.args)

    def close_connection(self):
        print("connection close")
        self.__tcp.close()
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_host(self):
        return self.my_host
    
    def get_port(self):
        return self.my_port

