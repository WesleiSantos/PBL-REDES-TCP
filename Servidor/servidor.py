import socket
import select
import sys
import queue as queue
import mysql.connector
import json
from mysql.connector import errorcode
from mysql.connector import Error


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
            self._tcp.listen(5)
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
                        con, client = sock.accept()
                        con.setblocking(0)
                        inputs.append(con)
                        message_queues[con] = queue.Queue()
                        print('Concetado por ', client)
                    else:
                        data = sock.recv(2048)
                        msg_s = str(data.decode('utf-8'))

                        headers = msg_s.split('\n')
                        method = headers[0].split()[0]
                        route = headers[0].split()[1]

                        print("header ", headers)
                        print("filename ", route)
                        print("method ", method)

                        response = self.api(method, route, '')
                        '''
                        if(msg_s):
                            data_json = json.loads(msg_s)
                            if (data_json['topic'] == "lixeira"):
                                sql = "INSERT INTO lixeira(id,host,port,status,coord_x,coord_y, capacity, qtd_used) VALUES(%s, %s,%s, %s,%s, %s,%s,%s) ON DUPLICATE KEY UPDATE host = VALUES (host),port = VALUES (port),status = VALUES (status) ,coord_x = VALUES (coord_x),coord_y = VALUES (coord_y), capacity = VALUES (capacity), qtd_used = VALUES (qtd_used)"
                                values = (data_json['id'], data_json['host'],
                                          data_json['port'], data_json['status'],
                                          data_json['coords'][0],
                                          data_json['coords'][1],
                                          data_json['capacity'],
                                          data_json['qtd_used'])
                                try:
                                    cursor = self._db.cursor()
                                    cursor.execute(sql, values)
                                    self._db.commit()
                                except Exception as e:
                                    print('Error ', e.args)
                        '''
                        if data:
                            message_queues[sock].put(response)
                            if sock not in outputs:
                                outputs.append(sock)
                            else:
                                if sock in outputs:
                                    outputs.remove(sock)
                                inputs.remove(sock)
                                sock.close()
                                del message_queues[sock]

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

    def api(self, method, route, payload):
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
