import socket
import json
from services import Services


class Caminhao():
    def __init__(self, x, y, capacity):
        self.id = None
        self.__coords = (x, y)
        self.__capacity = capacity
        self.__qtd_used = 0
        self.trash = None

    def register(self, server_host, port):
        self.service = Services(server_host, port)
        data = json.dumps({"status": True,
                          "coords": self.__coords, "capacity": self.__capacity, "qtd_used": self.__qtd_used})
        response = self.service.POST("/truck/register", data)
        self.trash = response.trash
        print("register: ", response)

        self.id = response.truck_id
        print("register: ", response)
        return response

    def get_capacity(self):
        return self.__capacity

    def collect_garbage(self, data):
        response = self.service.POST("/truck/collect-garbage", data)
        print("response collect: ", response)
        return response
    
    def next_garbage(self):
        response = self.service.POST("/truck/next-garbage",json.dumps({"coords":self.__coords, "id": self.id}))
        print("response collect: ", response)
        trash = response.next_trash
        self.trash = trash
        return trash

    def status_trash(self):
        response = self.service.GET("/truck/trash?", {"id": self.id})
        trash = response.trash
        self.trash = trash
        print("Trash status: ", response)
        return trash
