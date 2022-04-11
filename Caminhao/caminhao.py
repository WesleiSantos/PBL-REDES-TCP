import socket
import json
from services import Services


class Caminhao():
    def __init__(self, x, y, capacity):
        self.__coords = (x, y)
        self.__capacity = capacity
        self.__qtd_used = 0
        self.trash=None
    
    def register(self, server_host, port):
        self.service = Services(server_host, port)
        data = json.dumps({"status": True,
                          "coords": self.__coords, "capacity": self.__capacity, "qtd_used": self.__qtd_used})
        response = self.service.POST("/register-garbage-truck", data)
        self.trash = response.trash
        print("register: ", response)
        return response

    def get_capacity(self):
        return self.__capacity

    def collect_garbage(self, data):
        response = self.service.POST("/collect_garbage", data)
        print("response collect: ", response)
        self.trash = response.next_trash
        return response
