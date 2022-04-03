import socket
import json
from services import Services


class Caminhao():
    def __init__(self, x, y, capacity):
        self.__coords = (x, y)
        self.__capacity = capacity
        self.__qtd_used = 0

    def start(self, server_host, port):
        self.service = Services(server_host, port)

    def get_capacity(self):
        return self.__capacity

    def get_list_trash(self, data):
        response = self.service.GET("/list-trash", data)
        return response

    def collect_garbage(self, data):
        response = self.service.POST("/collect_garbage", data)
        return response
