from tkinter import *
from turtle import width
from caminhao import Caminhao
import json
import threading
import time


class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primaryContainer = Frame(master)
        self.primaryContainer["pady"] = 10
        self.primaryContainer.pack()

        self.secondContainer = Frame(master)
        self.secondContainer["padx"] = 20
        self.secondContainer["pady"] = 10
        self.secondContainer.pack()

        self.thirdContainer = Frame(master)
        self.thirdContainer["padx"] = 20
        self.thirdContainer["pady"] = 10
        self.thirdContainer.pack()

        self.fourthContainer = Frame(master)
        self.fourthContainer["padx"] = 20
        self.fourthContainer["pady"] = 10
        self.fourthContainer.pack()

        self.fifthContainer = Frame(master)
        self.fifthContainer["padx"] = 20
        self.fifthContainer["pady"] = 10
        self.fifthContainer.pack()

        self.sixthContainer = Frame(master)
        self.sixthContainer["padx"] = 20
        self.sixthContainer["pady"] = 10
        self.sixthContainer.pack()

        self.seventhContainer = Frame(master)
        self.seventhContainer["pady"] = 20
        self.seventhContainer.pack()

        self.title = Label(self.primaryContainer,
                           text="Dados iniciais da caminhao")
        self.title["font"] = ("Arial", "10", "bold")
        self.title.pack()

        self.hostLabel = Label(self.secondContainer,
                               text="Host", font=self.fontePadrao, width=20)
        self.hostLabel.pack(side=LEFT)

        self.host = Entry(self.secondContainer)
        self.host.insert(0, "localhost")
        self.host["width"] = 25
        self.host["font"] = self.fontePadrao
        self.host.pack(side=LEFT)

        self.portLabel = Label(self.thirdContainer,
                               text="Port", font=self.fontePadrao,  width=20)
        self.portLabel.pack(side=LEFT)

        self.port = Entry(self.thirdContainer)
        self.port.insert(0, "9000")
        self.port["width"] = 25
        self.port["font"] = self.fontePadrao
        self.port.pack(side=LEFT)

        self.cordXLabel = Label(
            self.fourthContainer, text="Coordenada inicial X", font=self.fontePadrao, width=20)
        self.cordXLabel.pack(side=LEFT)

        self.cordX = Entry(self.fourthContainer)
        self.cordX.insert(0, "100")
        self.cordX["width"] = 25
        self.cordX["font"] = self.fontePadrao
        self.cordX.pack(side=LEFT)

        self.cordYLabel = Label(
            self.fifthContainer, text="Coordenada inicial Y", font=self.fontePadrao,  width=20)
        self.cordYLabel.pack(side=LEFT)

        self.cordY = Entry(self.fifthContainer)
        self.cordY.insert(0, "100")
        self.cordY["width"] = 25
        self.cordY["font"] = self.fontePadrao
        self.cordY.pack(side=LEFT)

        self.capacityLabel = Label(
            self.sixthContainer, text="Capacidade (M³)", font=self.fontePadrao,  width=20)
        self.capacityLabel.pack(side=LEFT)

        self.capacity = Entry(self.sixthContainer)
        self.capacity.insert(0, "100")
        self.capacity["width"] = 25
        self.capacity["font"] = self.fontePadrao
        self.capacity.pack(side=LEFT)

        self.confirm = Button(self.seventhContainer)
        self.confirm["text"] = "Criar"
        self.confirm["font"] = ("Calibri", "8")
        self.confirm["width"] = 12
        self.confirm["command"] = self.createGarbageTruck
        self.confirm.pack()

        self.message = Label(self.seventhContainer,
                             text="", font=self.fontePadrao)
        self.message.pack()

    # Método para criar caminhao

    def createGarbageTruck(self):
        host = self.host.get()
        port = self.port.get()
        cordX = self.cordX.get()
        cordY = self.cordY.get()
        capacity = self.capacity.get()

        try:
            self.caminhao = Caminhao(int(cordX), int(cordY), int(capacity))
            self.caminhao.start(host, int(port))

            '''self.message["text"] = self.caminhao.start(host, int(port))
            self.message["bg"] = "green" '''

            self.createWindowsActions()

        except Exception as e:
            self.message["text"] = "Dados inválidos ".join(e.args)
            self.message["bg"] = "red"

    def createWindowsActions(self):
        global root
        self.newWindow = Toplevel(root)
        self.newWindow.title("Caminhao")
        self.newWindow.geometry("900x400+100+100")
        x = threading.Thread(target=self.thread_function, args=(), daemon=True)
        x.start()

    def renderTrash(self, row, row_idx):
        frame = Frame(
            master=self.newWindow,
            relief=RAISED,
            borderwidth=1,
            width=450, height=50
        )
        frame.grid(row=row_idx, column=0, columnspan=4, padx=5, pady=5)
        orderLabel = Label(frame, text="Prioridade")
        orderLabel.pack(side=LEFT)
        order = Label(frame, text=str(row_idx)+"º")
        order.pack(side=LEFT)
        idLabel = Label(frame, text="Identificação:")
        idLabel.pack(side=LEFT)
        id = Label(frame, text=row[0])
        id.pack(side=LEFT)
        statusLabel = Label(frame, text="Status:")
        statusLabel.pack(side=LEFT)
        status = Label(frame, text=row[3])
        status.pack(side=LEFT)
        capacityLabel = Label(frame, text="Capacidade:")
        capacityLabel.pack(side=LEFT)
        capacity = Label(frame, text=row[4])
        capacity.pack(side=LEFT)
        coord_xLabel = Label(frame, text="Posição x:")
        coord_xLabel.pack(side=LEFT)
        coord_x = Label(frame, text=row[5])
        coord_x.pack(side=LEFT)
        coord_yLabel = Label(frame, text="Posição y:")
        coord_yLabel.pack(side=LEFT)
        coord_y = Label(frame, text=row[6])
        coord_y.pack(side=LEFT)
        qtd_usedLabel = Label(frame, text="Quantidade utilizada:")
        qtd_usedLabel.pack(side=LEFT)
        qtd_used = Label(frame, text=row[7])
        qtd_used.pack(side=LEFT)
        collect = Button(frame)
        collect["text"] = "Coletar"
        collect["font"] = ("Calibri", "8")
        collect["width"] = 12
        collect["command"] = lambda: [self.collect_garbage(row[0])]
        collect.pack()

    def setStateTrash(self):
        data = json.dumps({"state": False, "id": 2})
        self.caminhao.get_list_trash(data)

    def listTrash(self):
        list = self.caminhao.get_list_trash('')
        for row_idx, row in enumerate(list):
            self.renderTrash(row, row_idx)
        print(list)

    def collect_garbage(self, id):
        payload = json.dumps({"id":id})
        resp = self.caminhao.collect_garbage(payload)
        print(resp)

    def thread_function(self):
        while True:
            self.listTrash()
            time.sleep(30)


root = Tk()
root.title("caminhao")
root.geometry("400x400+100+100")
Application(root)
root.mainloop()
