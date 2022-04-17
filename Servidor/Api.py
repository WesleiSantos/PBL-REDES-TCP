import json
from urllib.parse import parse_qs
from math import sqrt

class Api:

    #inicializa instancia do banco de dados
    def __init__(self, db) -> None:
        self._db = db

    #Faz consulta baseado na rota
    def search(self, method, route, payload, params=None):
        error = 'HTTP/1.1 404 Not Found\n\n'

        # ROUTE GET /list-trash
        if method == "GET" and route == "/list-trash":
            sql = "SELECT * FROM lixeira"
            try:
                cursor = self._db.cursor()
                cursor.execute(sql)
                myresult = cursor.fetchall()
                self._db.commit()
                return json.dumps(myresult)
            except Exception as e: 
                print('Error ', e.args)
                raise Exception(error)

        # ROUTE GET /list-truck
        if method == "GET" and route == "/list-truck":
            sql = "SELECT * FROM caminhao"
            try:
                cursor = self._db.cursor()
                cursor.execute(sql)
                myresult = cursor.fetchall()
                self._db.commit()
                return json.dumps(myresult)
            except Exception as e:
                print('Error ', e.args)
                raise Exception(error)

        # ROUTE POST /set-truck
        elif method == "POST" and route == "/set-truck":
            sql = "UPDATE caminhao SET next_trash = %s;"
            values = (str(payload.id),)
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                self._db.commit()
                return json.dumps({"done": True})
            except Exception as e:
                print('Error ', e.args)
                self._db.rollback()
                raise Exception(error)

        # ROUTE POST /dumps/register-trash
        elif method == "POST" and route == "/dumps/register-trash":
            sql = "INSERT INTO lixeira(status,coord_x,coord_y, capacity, qtd_used) VALUES(%s,%s, %s,%s,%s) ON DUPLICATE KEY UPDATE status = VALUES (status) ,coord_x = VALUES (coord_x),coord_y = VALUES (coord_y), capacity = VALUES (capacity), qtd_used = VALUES (qtd_used)"
            values = (payload.status,
                      payload.coords[0],
                      payload.coords[1],
                      payload.capacity,
                      payload.qtd_used)
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                trash = cursor.lastrowid
                self._db.commit()
                return json.dumps({"done": True, "id": trash})
            except Exception as e:
                print('Error ', e.args)
                self._db.rollback()
                raise Exception(error)

        # ROUTE POST /dumps/delete
        elif method == "POST" and route == "/dumps/delete":
            sql = "DELETE FROM lixeira WHERE id = %s;"
            values = (payload.id,)
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                self._db.commit()
                return json.dumps({"done": True})
            except Exception as e:
                print('Error ', e.args)
                self._db.rollback()
                raise Exception(error)

        # ROUTE POST /dumps/set-trash
        elif method == "POST" and route == "/dumps/set-trash":
            sql = "UPDATE lixeira SET qtd_used = %s WHERE coord_x = %s AND coord_y = %s;"
            values = (
                payload.qtd,
                payload.coords[0],
                payload.coords[1]
            )
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                self._db.commit()
                return json.dumps({"done": True})
            except Exception as e:
                print('Error ', e.args)
                self._db.rollback()
                raise Exception(error)

        # ROUTE GET /dumps/status
        elif method == "GET" and route == "/dumps/status":
            sql = "SELECT status, qtd_used FROM lixeira WHERE coord_x = %s AND coord_y = %s;"
            values = (
                params.get('coord_x')[0],
                params.get('coord_y')[0]
            )
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                myresult = cursor.fetchone()
                self._db.commit()
                return json.dumps({"status": myresult[0], "qtd_used": myresult[1]})
            except Exception as e:
                print('Error ', e.args)
                raise Exception(error)

        # ROUTE POST /dumps/status
        elif method == "POST" and route == "/dumps/status":
            sql = "UPDATE lixeira SET status = %s WHERE coord_x = %s AND coord_y = %s;"
            values = (
                payload.status,
                payload.coord_x,
                payload.coord_y
            )
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                self._db.commit()
                return json.dumps({"done": True})
            except Exception as e:
                print('Error ', e.args)
                self._db.rollback()
                raise Exception(error)

        # ROUTE GET /truck
        elif method == "GET" and route == "/truck":
            sql = "SELECT * FROM caminhao WHERE id = %s;"
            values = (
                params.get('id')[0],
            )
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                myresult = cursor.fetchone()
                self._db.commit()
                return json.dumps({"Done": True, "truck": myresult})
            except Exception as e:
                print('Error ', e.args)
                raise Exception(error)

        # ROUTE POST /truck/register
        elif method == "POST" and route == "/truck/register":
            trash = self.next_trash(payload.coords)
            if len(trash) != 0:
                sql = "INSERT INTO caminhao(status,coord_x,coord_y, capacity, qtd_used, next_trash) VALUES(%s,%s, %s,%s,%s, %s) ON DUPLICATE KEY UPDATE status = VALUES (status) ,coord_x = VALUES (coord_x),coord_y = VALUES (coord_y), capacity = VALUES (capacity), qtd_used = VALUES (qtd_used), next_trash = VALUES (next_trash)"
                values = (payload.status,
                          trash[4],
                          trash[5],
                          payload.capacity,
                          payload.qtd_used,
                          trash[0]
                          )
                try:
                    cursor = self._db.cursor()
                    cursor.execute(sql, values)
                    garbage_truck = cursor.lastrowid
                    self._db.commit()
                    return json.dumps({"done": True, "trash": trash, "truck_id": garbage_truck})
                except Exception as e:
                    print('Error ', e.args)
                    self._db.rollback()
                    raise Exception(error)
            else:
                return json.dumps({"done": False}) 

        # ROUTE POST /truck/delete
        elif method == "POST" and route == "/truck/delete":
            sql = "DELETE FROM caminhao WHERE id = %s;"
            values = (payload.id,)
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                self._db.commit()
                return json.dumps({"done": True})
            except Exception as e:
                print('Error ', e.args)
                self._db.rollback()
                raise Exception(error)

        # ROUTE GET /truck/trash
        elif method == "GET" and route == "/truck/trash":
            sql = "SELECT l.* FROM caminhao as c INNER JOIN lixeira as l ON c.next_trash = l.id WHERE c.id = %s;"
            values = (
                params.get('id')[0],
            )
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                myresult = cursor.fetchone()
                self._db.commit()
                return json.dumps({"Done": True, "trash": myresult})
            except Exception as e:
                print('Error ', e.args)
                raise Exception(error)

        # ROUTE POST /truck/collect_garbage
        elif method == "POST" and route == "/truck/collect-garbage":
            sql = "UPDATE lixeira SET qtd_used=%s WHERE coord_x = %s AND coord_y = %s;"
            values = ('0', str(payload.coord[0]), str(payload.coord[1]))
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                self._db.commit()
                resp = self.update_truck(payload.id, payload.qtd_used)
                return resp
            except Exception as e:
                print('Error ', e.args)
                self._db.rollback()
                raise Exception(error)

        # ROUTE POST /truck/next-garbage
        elif method == "POST" and route == "/truck/next-garbage":
            trash = self.next_trash(payload.coords)
            sql = "UPDATE caminhao SET next_trash=%s,coord_x = %s, coord_y = %s WHERE id=%s;"
            values = (str(trash[0]), str(trash[4]),
                      str(trash[5]), str(payload.id))
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                self._db.commit()
                return json.dumps({"Done": True, "next_trash": trash})
            except Exception as e:
                print('Error ', e.args)
                self._db.rollback()
                raise Exception(error)

        # ROUTE POST /truck/unload
        elif method == "POST" and route == "/truck/unload":
            sql = "UPDATE caminhao SET qtd_used=%s WHERE id=%s;"
            values = ('0', str(payload.id))
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                self._db.commit()
                return json.dumps({"Done": True})
            except Exception as e:
                print('Error ', e.args)
                self._db.rollback()
                raise Exception(error)
    
    #Faz comparação entre distancia e quantidade de lixo utilizada
    def comp(item):  # primeiro item em ordem decrescente, segundo em ordem crescente
        return -item[8], item[7]

    #Atualiza quantidade de lixo no caminhão 
    def update_truck(self, id, qtd):
        sql = "UPDATE caminhao SET qtd_used=%s WHERE id=%s;"
        values = (str(qtd), str(id))
        try:
            cursor = self._db.cursor()
            cursor.execute(sql, values)
            self._db.commit()
            return json.dumps({"Done": True})
        except Exception as e:
            print('Error ', e.args)
            self._db.rollback()

    #Método pega todas as lixeira, calcula a distancia delas para o caminhão e seleciona a que está mais próxima e com maior quantidade de lixo
    #Parâmetro dist coordenadas do caminhão para o calculo da distância
    def next_trash(self, dist):
        sql = "SELECT * FROM lixeira"
        try:
            cursor = self._db.cursor()
            cursor.execute(sql)
            myresult = cursor.fetchall()
            self._db.commit()
            if len(myresult) == 0:
                return myresult
            list_trash = list()
            for trash in myresult:
                trash = list(trash)
                # Calculando a distância
                distXY = sqrt((int(dist[0])-int(trash[4]))
                              ** 2) + ((int(dist[1])-int(trash[5]))**2)
                trash.append(distXY)
                list_trash.append(trash)
            sortedLista = sorted(
                list_trash, key=lambda item: (-item[7], item[8])) #Faz a ordenação das lixeiras com base na distancia e quantidade de lixo usado
            return sortedLista[0] #retorna o primeiro da lista
        except Exception as e:
            print('Error ', e.args)