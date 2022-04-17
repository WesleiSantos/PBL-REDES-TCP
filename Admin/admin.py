import socket
import json
from services import Services


class Admin():

    #Inicializa conexão
    def start(self, server_host, port):
        self.service = Services(server_host, port)
    
    #Lista as lixeira disponíveis
    def get_list_trash(self, data=''):
        response = self.service.GET("/list-trash?", data)
        return response

    #Seta lixeira para o caminhão
    def set_trunck(self, data):
        response = self.service.POST("/set-truck", json.dumps(data))

    #atualiza estado das lixeiras
    def update_state(self, data):
        response = self.service.POST(
            "/dumps/status", json.dumps({"coord_x": data[0], "coord_y": data[1], "status": data[2]}), )
    
    #Lista caminhões
    def get_list_truck(self, data=''):
        response = self.service.GET("/list-truck?", data)
        return response
    
    #disconecta admin
    def disconnect(self):
        self.service.close()
