import socket
import select
import sys
import queue as queue
import mysql.connector
import json
from mysql.connector import errorcode
from mysql.connector import Error
from types import SimpleNamespace
from urllib.parse import parse_qs


class Server():

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._db = self.connect_mysql()

    def start(self):
        orig = (self._host, self._port)
        try:
            self._tcp.setblocking(0)
            self._tcp.bind(orig)
            self._tcp.listen(20)
            inputs = [self._tcp]
            outputs = []
            message_queues = {}

            print("Servidor iniciado em ", self._host, ":", self._port)
            print("Aguardando conexão com o cliente...")

            while inputs:
                readable, writable, exceptional = select.select(
                    inputs, outputs, inputs)
                for sock in readable:
                    if sock is self._tcp:
                        print("veio1")
                        con, client = sock.accept()
                        con.setblocking(0)
                        inputs.append(con)
                        message_queues[con] = queue.Queue()
                        print('Concetado por ', client)
                    else:
                        data = sock.recv(2048)
                        msg_s = str(data.decode('utf-8'))
                        response = ''
                        print(data)
                        print("v1eio2")
                        if msg_s != "":
                            headers = msg_s.split('\n')
                            method = headers[0].split()[0]
                            route = headers[0].split()[1]
                            body = headers[1]
                            print("body", body)
                            print("header ", headers)
                            print("filename ", route)
                            print("method ", method)
                            if method == "GET":
                                params = parse_qs(route.split('?')[1])
                                route = route.split('?')[0]
                                print('route', route)
                                response = self.api(
                                    method, route, None, params)
                            else:
                                if len(body) != 0:
                                    print("veioaqui")
                                    # Parse JSON into an object with attributes corresponding to dict keys.
                                    obj = json.loads(
                                        body, object_hook=lambda d: SimpleNamespace(**d))
                                    print("body", obj)
                                    response = self.api(method, route, obj)
                        else:
                            response = "nada"
                        print("veio4")

                        if data:
                            print("veio5")
                            message_queues[sock].put(response)
                            print("veio6")
                            if sock not in outputs:
                                print("veio7")
                                outputs.append(sock)
                                print("veio8")
                        else:
                            print("veio9")
                            if sock in outputs:
                                print("veio10")
                                outputs.remove(sock)
                                print("veio11")
                            print("veio12")
                            inputs.remove(sock)
                            print("veio13")
                            sock.close()
                            print("veio14")
                            del message_queues[sock]
                            print("veio15")

                for sock in writable:
                    try:
                        next_msg = message_queues[sock].get_nowait()
                    except queue.Empty:
                        outputs.remove(sock)
                    else:
                        sock.send(bytes(next_msg, 'utf-8'))

                for sock in exceptional:
                    inputs.remove(sock)
                    if sock in outputs:
                        outputs.remove(sock)
                    sock.close()
                    del message_queues[sock]
        except Exception as e:
            print("Erro ao inicializar o servidor ", e.args)
            self._db.close()

    def api(self, method, route, payload, params=None):
        response = b"HTTP/1.1 200 OK\n\n"
        header = 'HTTP/1.1 404 Not Found\n\n'
        # ROUTE GET /list-trash
        if method == "GET" and route == "/list-trash":
            sql = "SELECT * FROM lixeira"
            try:
                cursor = self._db.cursor()
                cursor.execute(sql)
                myresult = cursor.fetchall()
                self._db.commit()
                print(myresult)
                return json.dumps(myresult)
            except Exception as e:
                print('Error ', e.args)

        # ROUTE POST /collect_garbage
        elif method == "POST" and route == "/collect_garbage":
            print("payload", payload.id)
            sql = "UPDATE lixeira SET qtd_used=%s WHERE id=%s;"
            values = ('0', str(payload.id))
            try:
                cursor = self._db.cursor()
                cursor.execute(sql, values)
                self._db.commit()
                return json.dumps({"done": True})
            except Exception as e:
                print('Error ', e.args)
                self._db.rollback()

        # ROUTE POST /register-trash
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
                self._db.commit()
                return json.dumps({"done": True})
            except Exception as e:
                print('Error ', e.args)

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

    def connect_mysql(self):
        try:
            db_connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='weslei200',
                database='CIDADE_INTELIGENTE')
            print("Conectado a base de dados!")
            return db_connection
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                print("Base de dados não existe!")
            elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Nome ou senha está inválido!")
            else:
                print(error)
