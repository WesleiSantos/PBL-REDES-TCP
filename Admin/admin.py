import socket
import json
from services import Services


class Admin():
    def start(self, server_host, port):
        self.service = Services(server_host, port)

    def get_capacity(self):
        return self.__capacity

    def get_list_trash(self, data=''):
        response = self.service.GET("/list-trash?", data)
        return response

    def set_trunck(self, data):
        response = self.service.POST("/set-truck", json.dumps(data))
        print(response)

    def update_state(self, data):
        response = self.service.POST(
            "/dumps/status", json.dumps({"coord_x": data[0], "coord_y": data[1], "status": data[2]}), )

    def get_list_truck(self, data=''):
        response = self.service.GET("/list-truck?", data)
        print(response)
        return response
        
    def disconnect(self):
        self.service.close()
