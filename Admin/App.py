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

        self.frameMaster = Frame(master)
        self.frameMaster.pack()

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
            x = threading.Thread(
                target=self.thread_function, args=(), daemon=True)
            x.start()

        except Exception as e:
            self.message["text"] = "Dados inválidos ".join(e.args)
            self.message["bg"] = "red"

    def renderTrash(self, row, row_idx):
        frame = Frame(
            master=self.frameMaster,
            relief=RAISED,
            borderwidth=1,
            width=500, height=50
        )
        frame.grid(row=(row_idx+1), column=0, columnspan=4, padx=5, pady=5)
        orderLabel = Label(frame, text="Lixeira")
        orderLabel.pack(side=LEFT)
        order = Label(frame, text=str((row_idx+1)))
        order.pack(side=LEFT)
        statusLabel = Label(frame, text="Status:")
        statusLabel.pack(side=LEFT)
        status = Label(frame, text='', width=5, padx=5)
        if bool(row[3]):
            status["bg"] = 'green'
        else:
            status["bg"] = 'red'
        status.pack(side=LEFT)
        capacityLabel = Label(frame, text="Capacidade:")
        capacityLabel.pack(side=LEFT)
        capacity = Label(frame, text=row[6], padx=5)
        capacity.pack(side=LEFT)
        coord_xLabel = Label(frame, text="Posição x:")
        coord_xLabel.pack(side=LEFT)
        coord_x = Label(frame, text=row[4], padx=5)
        coord_x.pack(side=LEFT)
        coord_yLabel = Label(frame, text="Posição y:")
        coord_yLabel.pack(side=LEFT)
        coord_y = Label(frame, text=row[5], padx=5)
        coord_y.pack(side=LEFT)
        qtd_usedLabel = Label(frame, text="Quantidade utilizada:")
        qtd_usedLabel.pack(side=LEFT)
        qtd_used = Label(frame, text=str(row[7])+'%', padx=5)
        qtd_used.pack(side=LEFT)
        collect = Button(frame)
        collect["text"] = "Setar coleta"
        collect["font"] = ("Calibri", "8")
        collect["width"] = 18
        collect["command"] = lambda: [self.setTruck(row[0], row[3])]
        collect.pack()
        collect = Button(frame)
        collect["text"] = "Bloquear/Desbloquear"
        collect["font"] = ("Calibri", "8")
        collect["width"] = 18
        collect["command"] = lambda: [
            self.admin.update_state((row[4], row[5], not bool(row[3])))]
        collect.pack()

    def renderTruck(self, row, row_idx):
        frame = Frame(
            master=self.frameMaster,
            relief=RAISED,
            borderwidth=1,
            width=500, height=50
        )
        frame.grid(row=(row_idx+1), column=0,
                   columnspan=4, padx=5, pady=5)
        statusLabel = Label(frame, text="Status:")
        statusLabel.pack(side=LEFT)
        status = Label(frame, text='', width=5, padx=5)
        if bool(row[1]):
            status["bg"] = 'green'
        else:
            status["bg"] = 'red'
        status.pack(side=LEFT)
        capacityLabel = Label(frame, text="Capacidade:")
        capacityLabel.pack(side=LEFT)
        capacity = Label(frame, text=row[4], padx=5)
        capacity.pack(side=LEFT)
        coord_xLabel = Label(frame, text="Posição x:")
        coord_xLabel.pack(side=LEFT)
        coord_x = Label(frame, text=row[2], padx=5)
        coord_x.pack(side=LEFT)
        coord_yLabel = Label(frame, text="Posição y:")
        coord_yLabel.pack(side=LEFT)
        coord_y = Label(frame, text=row[3], padx=5)
        coord_y.pack(side=LEFT)
        qtd_usedLabel = Label(frame, text="Quantidade utilizada:")
        qtd_usedLabel.pack(side=LEFT)
        qtd_used = Label(frame, text=str(row[5])+'%', padx=5)
        qtd_used.pack(side=LEFT)

        next_trashLabel = Label(frame, text="Pŕoxima lixeira:")
        next_trashLabel.pack(side=LEFT)
        next_trash = Label(frame, text=str(row[6]), padx=5)
        next_trash.pack(side=LEFT)

    def setStateTrash(self):
        data = json.dumps({"state": False, "id": 2})
        self.admin.get_list_trash(data)

    def setTruck(self, id, status):
        if status:
            self.admin.set_trunck({"id": id})
        else:
            self.alert("Lixeira bloqueada!")

    def listTrash(self):
        try:
            self.destroyContainers()
            frame = Frame(
                master=self.frameMaster,
                relief=RAISED,
                borderwidth=1,
                width=500, height=50
            )
            frame.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
            title = Label(frame,
                          text="Lista de lixeiras")
            title["font"] = ("Arial", "10", "bold")
            title.pack()
            list_trash = self.admin.get_list_trash()
            count = 1
            for row_idx, row in enumerate(list_trash):
                self.renderTrash(row, row_idx)
                count = row_idx+2

            frame2 = Frame(
                master=self.frameMaster,
                relief=RAISED,
                borderwidth=1,
                width=500, height=50
            )
            frame2.grid(row=count, column=0, columnspan=4, padx=5, pady=5)
            title2 = Label(frame2,
                           text="Lista de caminhões")
            title2["font"] = ("Arial", "10", "bold")
            title2.pack()
            list_truck = self.admin.get_list_truck()
            for row_idx, row in enumerate(list_truck):
                self.renderTruck(row, row_idx+count)
                count = count + 2
            
            newFrame = Frame(self.frameMaster)
            newFrame.grid(row=count+2, column=0, columnspan=4, padx=5, pady=5)
            self.exit = Button(newFrame)
            self.exit["text"] = "Sair"
            self.exit["font"] = ("Calibri", "8")
            self.exit["width"] = 12
            self.exit["command"] = lambda: [root.destroy()]
            self.exit.pack()


        except Exception as e:
            self.error(e.args)

    def destroyContainers(self):
        self.primaryContainer.destroy()
        self.secondContainer.destroy()
        self.thirdContainer.destroy()
        self.seventhContainer.destroy()
        self.frameMaster.destroy()
        self.frameMaster = Frame(root)
        self.frameMaster.pack()

    def error(self, error):
        messagebox.showerror("Title", "Erro na comunicação! "+str(error))

    def alert(self, error):
        messagebox.showwarning("Title", str(error))

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
