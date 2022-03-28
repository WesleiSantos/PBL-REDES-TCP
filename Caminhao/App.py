from tkinter import *
from caminhao import Caminhao


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

        self.title = Label(self.primaryContainer, text="Dados iniciais da caminhao")
        self.title["font"] = ("Arial", "10", "bold")
        self.title.pack()

        self.hostLabel = Label(self.secondContainer,text="Host", font=self.fontePadrao, width=20)
        self.hostLabel.pack(side=LEFT)

        self.host = Entry(self.secondContainer)
        self.host.insert(0, "localhost")
        self.host["width"] = 25
        self.host["font"] = self.fontePadrao
        self.host.pack(side=LEFT)

        self.portLabel = Label(self.thirdContainer, text="Port", font=self.fontePadrao,  width=20)
        self.portLabel.pack(side=LEFT)

        self.port = Entry(self.thirdContainer)
        self.port.insert(0, "9000")
        self.port["width"] = 25
        self.port["font"] = self.fontePadrao
        self.port.pack(side=LEFT)

        self.cordXLabel = Label(self.fourthContainer, text="Coordenada inicial X", font=self.fontePadrao, width=20)
        self.cordXLabel.pack(side=LEFT)
        
        self.cordX = Entry(self.fourthContainer)
        self.cordX.insert(0, "100")
        self.cordX["width"] = 25
        self.cordX["font"] = self.fontePadrao
        self.cordX.pack(side=LEFT)

        self.cordYLabel = Label(self.fifthContainer, text="Coordenada inicial Y", font=self.fontePadrao,  width=20)
        self.cordYLabel.pack(side=LEFT)

        self.cordY = Entry(self.fifthContainer)
        self.cordY.insert(0, "100")
        self.cordY["width"] = 25
        self.cordY["font"] = self.fontePadrao
        self.cordY.pack(side=LEFT)

        self.capacityLabel = Label(self.sixthContainer, text="Capacidade (M³)", font=self.fontePadrao,  width=20)
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

        self.message = Label(self.seventhContainer, text="", font=self.fontePadrao)
        self.message.pack()

    #Método para criar caminhao
    def createGarbageTruck(self):
        host=self.host.get()
        port=self.port.get()
        cordX=self.cordX.get()
        cordY=self.cordY.get()
        capacity=self.capacity.get()
       
        try:
            self.caminhao = Caminhao(host,int(port),int(cordX),int(cordY),int(capacity))
            self.message["text"] =self.caminhao.start()
            self.message["bg"] = "green"
            self.createWindowsActions()

        except Exception as e:
                self.message["text"] = "Dados inválidos ".join(e.args)
                self.message["bg"] = "red"


    def createWindowsActions(self):
        newWindow = Toplevel(root)
        newWindow.title("Caminhao")
        newWindow.geometry("400x400+100+100")

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

        self.capacityLabel = Label(self.container1,text = "Capacidade:" , font=self.fontePadrao, width=20)
        self.capacityLabel["font"] = ("Arial", "10", "bold")
        self.capacityLabel.pack()

        capacity = self.caminhao.get_capacity()
        self.qtdCapacity = Label(self.container1,text = capacity , font=self.fontePadrao, width=10)
        self.qtdCapacity["font"] = ("Arial", "10", "bold")
        self.qtdCapacity.pack()
        

        self.qtdLabel = Label(self.container2,text = "Usado:" , font=self.fontePadrao, width=10)
        self.qtdLabel["font"] = ("Arial", "10", "bold")
        self.qtdLabel.pack()

        qtd = str(self.caminhao.get_trash()) + "%"
        self.qtdUsed = Label(self.container2,text=qtd , font=self.fontePadrao, width=10)
        self.qtdUsed["font"] = ("Arial", "10", "bold")
        self.qtdUsed.pack()

        adcTrash = Button(self.container3, text = "+", font= self.fontePadrao, width=12)
        adcTrash["command"] = self.adcTrash
        adcTrash.pack(side=LEFT)
        removeTrash = Button(self.container3, text = "-", font= self.fontePadrao, width=12)
        removeTrash["command"] = self.removeTrash
        removeTrash.pack(side=LEFT)

    def adcTrash(self):
        self.caminhao.set_trash(1)
        qtd = self.caminhao.get_trash()
        self.qtdUsed['text'] = str(qtd) + "%" 
    
    def removeTrash(self):
        self.caminhao.set_trash(-1)
        qtd = self.caminhao.get_trash()
        self.qtdUsed['text'] = str(qtd) + "%"


root = Tk()
root.title("caminhao")
root.geometry("400x400+100+100")
Application(root)
root.mainloop()