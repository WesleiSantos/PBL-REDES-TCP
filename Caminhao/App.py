from tkinter import *
from tkinter import messagebox
from turtle import width
from caminhao import Caminhao
import json
import threading
import time


class Application:
    def __init__(self, master=None):
        self.frame = Frame()
        self.infoFrame = Frame()
        self.titleFrame = Frame()
        self.titleTrashFrame = Frame()
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
        self.cordX.insert(0, "0")
        self.cordX["width"] = 25
        self.cordX["font"] = self.fontePadrao
        self.cordX.pack(side=LEFT)

        self.cordYLabel = Label(
            self.fifthContainer, text="Coordenada inicial Y", font=self.fontePadrao,  width=20)
        self.cordYLabel.pack(side=LEFT)

        self.cordY = Entry(self.fifthContainer)
        self.cordY.insert(0, "0")
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
            resp = self.caminhao.register(host, int(port))
            if resp.done:
                self.message["text"] = "Registrada com sucesso!"
                self.message["bg"] = "green"
                self.createWindowsActions()
            else:
                self.message["text"] = "Falha ao registrar!"
                self.message["bg"] = "red"

        except Exception as e:
            self.message["text"] = "Dados inválidos ".join(e.args)
            self.message["bg"] = "red"

    def createWindowsActions(self):
        self.destroyContainers()
        root.geometry("900x250+100+100")
        x = threading.Thread(target=self.thread_function, args=(), daemon=True)
        x.start()

    def destroyContainers(self):
        self.primaryContainer.destroy()
        self.secondContainer.destroy()
        self.thirdContainer.destroy()
        self.fourthContainer.destroy()
        self.fifthContainer.destroy()
        self.sixthContainer.destroy()
        self.seventhContainer.destroy()

    def renderTrash(self, trash):
        
        self.titleTrashFrame = Frame(master=root,
                           relief=RAISED,
                           borderwidth=1,
                           width=500, height=50)
        self.titleTrashFrame.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
        title = Label(self.titleTrashFrame,
                      text="Informações da próxima lixeira")
        title["font"] = ("Arial", "10", "bold")
        title.pack()
        self.frame = Frame(
            master=root,
            relief=RAISED,
            borderwidth=1,
            width=500, height=50
        )
        self.frame.grid(row=4, column=0, columnspan=4, padx=5, pady=5)
        orderLabel = Label(self.frame, text="Prioridade")
        orderLabel.pack(side=LEFT)
        order = Label(self.frame, text=str(1)+"º")
        order.pack(side=LEFT)
        statusLabel = Label(self.frame, text="Status:")
        statusLabel.pack(side=LEFT)
        status = Label(self.frame, text='', width=5, padx=5)
        if bool(trash[3]):
            status["bg"] = 'green'
        else:
            status["bg"] = 'red'
        status.pack(side=LEFT)
        capacityLabel = Label(self.frame, text="Capacidade:")
        capacityLabel.pack(side=LEFT)
        capacity = Label(self.frame, text=trash[6], padx=5)
        capacity.pack(side=LEFT)
        coord_xLabel = Label(self.frame, text="Posição x:")
        coord_xLabel.pack(side=LEFT)
        coord_x = Label(self.frame, text=trash[4], padx=5)
        coord_x.pack(side=LEFT)
        coord_yLabel = Label(self.frame, text="Posição y:")
        coord_yLabel.pack(side=LEFT)
        coord_y = Label(self.frame, text=trash[5], padx=5)
        coord_y.pack(side=LEFT)
        qtd_usedLabel = Label(self.frame, text="Quantidade utilizada:")
        qtd_usedLabel.pack(side=LEFT)
        qtd_used = Label(self.frame, text=str(trash[7])+'%', padx=5)
        qtd_used.pack(side=LEFT)

        collect = Button(self.frame)
        collect["text"] = "Coletar"
        collect["font"] = ("Calibri", "8")
        collect["width"] = 18
        collect["command"] = lambda: [
            self.collect_garbage(trash[3])]
        collect.pack()

        collect = Button(self.frame)
        collect["text"] = "Ir próxima"
        collect["font"] = ("Calibri", "8")
        collect["width"] = 18
        collect["command"] = lambda: [
            self.next_garbage()]
        collect.pack()

    def renderInfoTruck(self):
        self.titleFrame = Frame(master=root,
                           relief=RAISED,
                           borderwidth=1,
                           width=500, height=50)
        self.titleFrame.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
        title = Label(self.titleFrame,
                      text="Informações do caminhão")
        title["font"] = ("Arial", "10", "bold")
        title.pack()
        self.infoFrame = Frame(
            master=root,
            relief=RAISED,
            borderwidth=1,
            width=500, height=50
        )
        self.infoFrame.grid(row=2, column=0, columnspan=4, padx=5, pady=5)
        capacityLabel = Label(self.infoFrame, text="Capacidade:")
        capacityLabel.pack(side=LEFT)
        capacity = Label(
            self.infoFrame, text=self.caminhao.get_capacity(), padx=5)
        capacity.pack(side=LEFT)
        coord_xLabel = Label(self.infoFrame, text="Posição x:")
        coord_xLabel.pack(side=LEFT)
        coord_x = Label(
            self.infoFrame, text=self.caminhao.get_coords()[0], padx=5)
        coord_x.pack(side=LEFT)
        coord_yLabel = Label(self.infoFrame, text="Posição y:")
        coord_yLabel.pack(side=LEFT)
        coord_y = Label(
            self.infoFrame, text=self.caminhao.get_coords()[1], padx=5)
        coord_y.pack(side=LEFT)
        qtd_usedLabel = Label(self.infoFrame, text="Quantidade utilizada:")
        qtd_usedLabel.pack(side=LEFT)
        qtd_used = Label(self.infoFrame, text=str(
            self.caminhao.get_qtd_used())+'%', padx=5)
        qtd_used.pack(side=LEFT)
        unload = Button(self.infoFrame)
        unload["text"] = "Descarregar"
        unload["font"] = ("Calibri", "8")
        unload["width"] = 12
        unload["command"] = lambda: [self.caminhao.unload_truck()]
        unload.pack(side=LEFT)

    def listTrash(self, trash):
        print("trash", trash)
        print("id", trash[0])
        self.frame.destroy()
        self.infoFrame.destroy()
        self.titleFrame.destroy()
        self.titleTrashFrame.destroy()
        self.renderInfoTruck()
        self.renderTrash(trash)

        exitFrame = Frame(root)
        exitFrame.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
        self.exit = Button(exitFrame)
        self.exit["text"] = "Sair"
        self.exit["font"] = ("Calibri", "8")
        self.exit["width"] = 12
        self.exit["command"] = lambda: [root.destroy()]
        self.exit.pack()

    def collect_garbage(self, status):
        if status:
            try:
                resp = self.caminhao.collect_garbage()
                print(resp)
            except Exception as e:
                self.alert("Não é possível fazer a coleta, pois o caminhão atingiu a capacidade máxima!")    
        else:
            self.alert("Lixeira bloqueada!")

    def error(self, error):
        messagebox.showerror("Atenção", "Erro na comunicação! "+str(error))

    def alert(self, error):
        messagebox.showwarning("Title", str(error))

    def next_garbage(self):
        trash = self.caminhao.next_garbage()
        self.listTrash(trash)

    def thread_function(self):
        while True:
            try:
                trash = self.caminhao.status_trash()
                self.listTrash(trash)
                self.caminhao.updateState()
            except Exception as e:
                self.error(e.args)
            time.sleep(10)


root = Tk()
root.title("caminhao")
root.geometry("900x400+100+100")
Application(root)
root.mainloop()
