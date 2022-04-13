import socket
import json
from services import Services


class Lixeira():

    def __init__(self, x, y, capacity):
        self.__status = True
        self.__coords = (x, y)
        self.__capacity = capacity
        self.__qtd_used = 0

    def register(self, server_host, port):
        self.service = Services(server_host, port)
        data = json.dumps({"status": self.__status,
                          "coords": self.__coords, "capacity": self.__capacity, "qtd_used": self.__qtd_used})
        response = self.service.POST("/dumps/register-trash", data)
        print("register: ", response)
        return response


    def update_state(self):
        response = self.service.GET("/dumps/status?", {"coord_x": self.__coords[0],"coord_y": self.__coords[1]})
        self.__status = bool(response.status)
        self.__qtd_used = response.qtd_used

    def set_trash(self, qtd):
        qtd_used = self.__qtd_used
        qtd_used += qtd
        if qtd_used <= self.__capacity:
            if qtd_used < 0:
                qtd_used = 0
            response = self.service.POST(
                "/dumps/set-trash", json.dumps({"coords": self.__coords, 'qtd': qtd_used}))
            if response.done:
                self.__qtd_used = qtd_used
        else:
            raise "Error"

    def get_trash(self):
        if self.__qtd_used > 0:
            return (self.__qtd_used/self.__capacity)*100
        else:
            return 0

    def set_state(self, status):
        self.__status = status

    def get_state(self):
        return self.__status

    def get_capacity(self):
        return self.__capacity
