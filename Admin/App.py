from tkinter import *
from tkinter import messagebox
from turtle import width
from admin import Admin
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

        self.seventhContainer = Frame(master)
        self.seventhContainer["pady"] = 20
        self.seventhContainer.pack()

        self.title = Label(self.primaryContainer,
                           text="Conectar painel admistrativo")
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

        self.confirm = Button(self.seventhContainer)
        self.confirm["text"] = "Criar"
        self.confirm["font"] = ("Calibri", "8")
        self.confirm["width"] = 12
        self.confirm["command"] = self.startAdmin
        self.confirm.pack()

        self.message = Label(self.seventhContainer,
                             text="", font=self.fontePadrao)
        self.message.pack()

    # Método para criar admin
    def startAdmin(self):
        host = self.host.get()
        port = self.port.get()

        try:
            self.admin = Admin()
            self.admin.start(host, int(port))
            x = threading.Thread(target=self.thread_function, args=(), daemon=True)
            x.start()

        except Exception as e:
            self.message["text"] = "Dados inválidos ".join(e.args)
            self.message["bg"] = "red"
        

    def renderTrash(self, row, row_idx):

        frame = Frame(
            master=root,
            relief=RAISED,
            borderwidth=1,
            width=500, height=50
        )
        frame.grid(row=row_idx, column=0, columnspan=4, padx=5, pady=5)
        orderLabel = Label(frame, text="Prioridade")
        orderLabel.pack(side=LEFT)
        order = Label(frame, text=str(row_idx)+"º")
        order.pack(side=LEFT)
        statusLabel = Label(frame, text="Status:")
        statusLabel.pack(side=LEFT)
        status = Label(frame, text='', width=5, padx=5)
        if bool(row[2]):
            status["bg"] = 'green'
        else:
            status["bg"] = 'red'
        status.pack(side=LEFT)
        capacityLabel = Label(frame, text="Capacidade:")
        capacityLabel.pack(side=LEFT)
        capacity = Label(frame, text=row[5], padx=5)
        capacity.pack(side=LEFT)
        coord_xLabel = Label(frame, text="Posição x:")
        coord_xLabel.pack(side=LEFT)
        coord_x = Label(frame, text=row[3], padx=5)
        coord_x.pack(side=LEFT)
        coord_yLabel = Label(frame, text="Posição y:")
        coord_yLabel.pack(side=LEFT)
        coord_y = Label(frame, text=row[4], padx=5)
        coord_y.pack(side=LEFT)
        qtd_usedLabel = Label(frame, text="Quantidade utilizada:")
        qtd_usedLabel.pack(side=LEFT)
        qtd_used = Label(frame, text=str(row[6])+'%', padx=5)
        qtd_used.pack(side=LEFT)
        collect = Button(frame)
        collect["text"] = "Coletar"
        collect["font"] = ("Calibri", "8")
        collect["width"] = 18
        collect["command"] = lambda: [self.collect_garbage((row[3], row[4]))]
        collect.pack()
        collect = Button(frame)
        collect["text"] = "Bloquear/Desbloquear"
        collect["font"] = ("Calibri", "8")
        collect["width"] = 18
        collect["command"] = lambda: [
            self.admin.update_state((row[3], row[4], not bool(row[2])))]
        collect.pack()

    def setStateTrash(self):
        data = json.dumps({"state": False, "id": 2})
        self.admin.get_list_trash(data)

    def listTrash(self):
        try:
            self.primaryContainer.destroy()
            self.secondContainer.destroy()
            self.thirdContainer.destroy()
            self.seventhContainer.destroy()
            list = self.admin.get_list_trash()
            for row_idx, row in enumerate(list):
                self.renderTrash(row, row_idx)
            print(list)
            
        except Exception as e:
            self.error(e.args)

    def error(self,error):
        messagebox.showerror("Title", "Erro na comunicação! "+str(error))


        

    def collect_garbage(self, coord):
        payload = json.dumps({"coord": coord})
        resp = self.admin.collect_garbage(payload)
        print(resp)

    def thread_function(self):
        while True:
            self.listTrash()
            time.sleep(10)


root = Tk()
root.title("admin")
root.geometry("900x400+100+100")
Application(root)
root.mainloop()
