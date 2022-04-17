from math import trunc
import json
from service import Services


class Caminhao():
    #Inicializa dados do caminhão
    def __init__(self, x, y, capacity):
        self.id = None
        self.__coords = (x, y)
        self.__capacity = capacity
        self.__qtd_used = 0
        self.trash = None

    #Registra caminhão no banco de dados
    #Parametro server_host endereço do servidor
    #Parametro port porta do servidor
    def register(self, server_host, port):
        self.service = Services(server_host, port)
        data = json.dumps({"status": True,
                          "coords": self.__coords, "capacity": self.__capacity, "qtd_used": self.__qtd_used})
        response = self.service.POST("/truck/register", data)
        if not response.done:
            raise Exception("Não há lixeiras em funcionamento!")
        self.trash = response.trash
        self.id = response.truck_id
        return response

 
    #Coleta lixo da lixeira
    def collect_garbage(self):
        qtd = self.__qtd_used+self.trash[7]
        if qtd <= self.__capacity:
            data = json.dumps({"coord": (
                self.trash[4], self.trash[5]), "qtd_used": qtd, "id": self.id})
            response = self.service.POST("/truck/collect-garbage", data)
            return response
        else:
            raise Exception("Não é possível fazer a coleta, pois o caminhão atingiu a capacidade máxima!")

    #Seta a próxima lixeira 
    def next_garbage(self):
        response = self.service.POST(
            "/truck/next-garbage", json.dumps({"coords": self.__coords, "id": self.id}))
        trash = response.next_trash
        self.trash = trash
        print("response : ", response)
        return trash

    #deleta caminhão do banco de dados
    def delete(self):
        response = self.service.POST(
            "/truck/delete", json.dumps({"id": self.id}))

    #Descarrega caminhão
    def unload_truck(self):
        response = self.service.POST(
            "/truck/unload", json.dumps({"id": self.id}))
        self.__qtd_used = 0
        return response

    #Atualiza estado do caminhão
    def updateState(self):
        response = self.service.GET("/truck?", {"id": self.id})
        truck = response.truck
        self.__coords = (truck[2], truck[3])
        self.__capacity = truck[4]
        self.__qtd_used = truck[5]
        return response.Done

    #Atualiza estado da lixeira atual
    def status_trash(self):
        response = self.service.GET("/truck/trash?", {"id": self.id})
        trash = response.trash
        self.trash = trash
        return trash
    
    #disconecta caminhão
    def disconnect(self):
        self.service.close()

    #Getters e setters 
    def get_capacity(self):
        return self.__capacity

    def get_coords(self):
        return self.__coords

    def get_qtd_used(self):
        return self.__qtd_used
    
    def get_capacity(self):
        return self.__capacity
