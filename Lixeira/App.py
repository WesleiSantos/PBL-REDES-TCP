from tkinter import *
from tkinter import messagebox
from lixeira import Lixeira
import threading
import time


class Application:
    
    #Constroi tela inicial
    def __init__(self, master=None):
        master.wm_protocol("WM_DELETE_WINDOW",self.on_delete)

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
                           text="Dados iniciais da lixeira")
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
            self.fourthContainer, text="Coordinate X", font=self.fontePadrao, width=20)
        self.cordXLabel.pack(side=LEFT)

        self.cordX = Entry(self.fourthContainer)
        self.cordX.insert(0, "100")
        self.cordX["width"] = 25
        self.cordX["font"] = self.fontePadrao
        self.cordX.pack(side=LEFT)

        self.cordYLabel = Label(
            self.fifthContainer, text="Coordinate Y", font=self.fontePadrao,  width=20)
        self.cordYLabel.pack(side=LEFT)

        self.cordY = Entry(self.fifthContainer)
        self.cordY.insert(0, "100")
        self.cordY["width"] = 25
        self.cordY["font"] = self.fontePadrao
        self.cordY.pack(side=LEFT)

        self.capacityLabel = Label(
            self.sixthContainer, text="Capacity (M³)", font=self.fontePadrao,  width=20)
        self.capacityLabel.pack(side=LEFT)

        self.capacity = Entry(self.sixthContainer)
        self.capacity.insert(0, "100")
        self.capacity["width"] = 25
        self.capacity["font"] = self.fontePadrao
        self.capacity.pack(side=LEFT)

        self.confirm = Button(self.seventhContainer)
        self.confirm["text"] = "Confirm"
        self.confirm["font"] = ("Calibri", "8")
        self.confirm["width"] = 12
        self.confirm["command"] = self.createTrash
        self.confirm.pack()

        self.message = Label(self.seventhContainer,
                             text="", font=self.fontePadrao)
        self.message.pack()

    # Método para criar lixeira
    def createTrash(self):
        host = self.host.get()
        port = self.port.get()
        cordX = self.cordX.get()
        cordY = self.cordY.get()
        capacity = self.capacity.get()

        try:
            self.lixeira = Lixeira(int(
                cordX), int(cordY), int(capacity))
            resp = self.lixeira.register(host, int(port))

            if resp.done:
                self.message["text"] = "Registrada com sucesso!"
                self.message["bg"] = "green"
                self.createWindowsActions()
                x = threading.Thread(
                    target=self.thread_function, args=(), daemon=True)
                x.start()
            else:
                self.message["text"] = "Falha ao registrar!"
                self.message["bg"] = "red"
        except Exception as e:
            self.error(e.args)
            self.message["text"] = "Dados inválidos ".join(e.args)
            self.message["bg"] = "red"
    
    #Método para renderizar informações da lixeira
    def createWindowsActions(self):
        self.destroyContainers()
        root.geometry("400x400+100+100")
        newWindow = Frame(root)
        newWindow.pack()
        self.container0 = Frame(newWindow)
        self.container0["padx"] = 30
        self.container0["pady"] = 5
        self.container0.pack()
        self.container1 = Frame(newWindow)
        self.container1["padx"] = 30
        self.container1["pady"] = 5
        self.container1.pack()
        self.container2 = Frame(newWindow)
        self.container2["padx"] = 30
        self.container2["pady"] = 5
        self.container2.pack()
        self.container3 = Frame(newWindow)
        self.container3["padx"] = 30
        self.container3["pady"] = 10
        self.container3.pack()
        self.container4 = Frame(newWindow)
        self.container4["padx"] = 30
        self.container4["pady"] = 5
        self.container4.pack()
        self.container5 = Frame(newWindow)
        self.container5["padx"] = 30
        self.container5["pady"] = 5
        self.container5.pack()
        self.container6 = Frame(newWindow)
        self.container6["padx"] = 30
        self.container6["pady"] = 5
        self.container6.pack()

        self.statusLabel = Label(
            self.container0, text="Status:", font=self.fontePadrao, width=20)
        self.statusLabel["font"] = ("Arial", "10", "bold")
        self.statusLabel.pack()

        status = self.lixeira.get_state()
        self.status = Label(self.container0, text='',
                            font=self.fontePadrao, width=10)
        self.status["font"] = ("Arial", "10", "bold")
        if status:
            self.status["bg"] = 'green'
        else:
            self.status["bg"] = 'red'
        self.status.pack()

        self.capacityLabel = Label(
            self.container1, text="Capacidade:", font=self.fontePadrao, width=20)
        self.capacityLabel["font"] = ("Arial", "10", "bold")
        self.capacityLabel.pack()

        capacity = self.lixeira.get_capacity()
        self.qtdCapacity = Label(self.container1, text=str(
            capacity) + " (M³)", font=self.fontePadrao, width=10)
        self.qtdCapacity["font"] = ("Arial", "10", "bold")
        self.qtdCapacity.pack()

        self.qtdLabel = Label(self.container2, text="Usado:",
                              font=self.fontePadrao, width=10)
        self.qtdLabel["font"] = ("Arial", "10", "bold")
        self.qtdLabel.pack()

        qtd = str(self.lixeira.get_trash()) + "%"
        self.qtdUsed = Label(self.container2, text=qtd,
                             font=self.fontePadrao, width=10)
        self.qtdUsed["font"] = ("Arial", "10", "bold")
        self.qtdUsed.pack()

        coord_xLabel = Label(self.container3, text="Posição x:")
        coord_xLabel.pack(side=LEFT)
        coord_x = Label(self.container3,
                        text=self.lixeira.get_coords()[0], padx=5)
        coord_x.pack(side=LEFT)
        coord_yLabel = Label(self.container3, text="Posição y:")
        coord_yLabel.pack(side=LEFT)
        coord_y = Label(self.container3,
                        text=self.lixeira.get_coords()[1], padx=5)
        coord_y.pack(side=LEFT)

        removeTrash = Button(self.container4, text="-",
                             font=self.fontePadrao, width=12)
        removeTrash["command"] = self.removeTrash
        removeTrash.pack(side=LEFT)

        adcTrash = Button(self.container4, text="+",
                          font=self.fontePadrao, width=12)
        adcTrash["command"] = self.adcTrash
        adcTrash.pack(side=LEFT)

        self.exit = Button(self.container5)
        self.exit["text"] = "Sair"
        self.exit["font"] = ("Calibri", "8")
        self.exit["width"] = 12
        self.exit["command"] = self.on_delete
        self.exit.pack()

    #Método para destruir os containers
    def destroyContainers(self):
        self.primaryContainer.destroy()
        self.secondContainer.destroy()
        self.thirdContainer.destroy()
        self.fourthContainer.destroy()
        self.fifthContainer.destroy()
        self.sixthContainer.destroy()
        self.seventhContainer.destroy()

    #Método para adicionar lixo a lixeira
    def adcTrash(self):
        try:
            if self.lixeira.get_state():
                self.lixeira.set_trash(8)
                qtd = self.lixeira.get_trash()
                self.qtdUsed['text'] = str(qtd) + "%"
            else:
                self.alert("lixiera bloqueada!")
        except Exception as e:
            self.alert("lixiera atingiu capacidade máxima!")

    #Método para remover lixo de lixeira
    def removeTrash(self):
        if self.lixeira.get_state():
            self.lixeira.set_trash(-8)
            qtd = self.lixeira.get_trash()
            self.qtdUsed['text'] = str(qtd) + "%"
        else:
            self.alert("lixiera bloqueada!")

    #Therad para atualizar informações da lixeira a cada 3s
    def thread_function(self):
        while True:
            try:
                self.lixeira.update_state()
                qtd = str(self.lixeira.get_trash()) + "%"
                self.qtdUsed['text'] = qtd
                status = self.lixeira.get_state()
                if status:
                    self.status["bg"] = 'green'
                else:
                    self.status["bg"] = 'red'
            except Exception as e:
                self.error(e.args)
            time.sleep(3)

    #Método que exibe mensagem de erro
    def error(self, error):
        messagebox.showerror("Atenção", "Erro na comunicação! "+str(error))
    
    #Método que exibe mensagem de alerta
    def alert(self, error):
        messagebox.showwarning("Atenção", str(error))
    
    #Método chamado ao desconectar lixeira
    def on_delete(self):
        self.lixeira.delete()
        self.lixeira.disconnect()
        root.destroy()

root = Tk()
root.title("Lixeira")
root.geometry("400x400+100+100")
Application(root)
root.mainloop()
