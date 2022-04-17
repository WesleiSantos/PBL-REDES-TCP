import socket
import select
import queue as queue
import mysql.connector
import json
from mysql.connector import errorcode
from mysql.connector import Error
from types import SimpleNamespace
from urllib.parse import parse_qs
from Api import Api


class Server():

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._db = self.connect_mysql()
        self.api = Api(self._db)

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
                        con, client = sock.accept()
                        con.setblocking(0)
                        inputs.append(con)
                        message_queues[con] = queue.Queue()
                        print('Concetado por ', client)
                    else:
                        data = sock.recv(2048)
                        msg_s = str(data.decode('utf-8'))
                        response = ''
                        if msg_s != "":
                            headers = msg_s.split('\n')
                            method = headers[0].split()[0]
                            route = headers[0].split()[1]
                            body = headers[1]
                            print("header ", headers)
                            if method == "GET":
                                params = parse_qs(route.split('?')[1])
                                route = route.split('?')[0]
                                print('route', route)
                                response = self.api.search(
                                    method, route, None, params)
                            else:
                                if len(body) != 0:
                                    # Parse JSON into an object with attributes corresponding to dict keys.
                                    obj = json.loads(
                                        body, object_hook=lambda d: SimpleNamespace(**d))
                                    print("body", obj)
                                    response = self.api.search(method, route, obj)
                        else:
                            response = ""

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

if __name__ == '__main__':
    serv = Server('localhost', 9000)
    serv.start()