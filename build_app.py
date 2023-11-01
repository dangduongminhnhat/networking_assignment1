import tkinter as tk
from client import Client


class Client_Page(tk.Frame):
    def __init__(self, parrent):
        tk.Frame.__init__(self, parrent)

        self.label_title = tk.Label(self, text="Client Side")
        self.label_title.pack()

        self.label_chat = tk.Label(self, text="input message")
        self.label_chat.pack()

        self.entry_message = tk.Entry(self)
        self.entry_message.pack()

        self.label_notice = tk.Label(self, text="")
        self.label_notice.pack()

        self.button_chat = tk.Button(
            self, text="chat", command=lambda: self.chat())
        self.button_chat.pack()

        self.client = Client()

    def __del__(self):
        try:
            self.client.send_message("END")
            print("Ending")
        except:
            print("Ending")
        self.client.soc.close()

    def send_message(self):
        try:
            message = self.entry_message.get()
            if message == "":
                return
            self.entry_message.delete(0, tk.END)
            rec = self.client.send_message(message)
            self.label_notice["text"] = "Server responses: " + rec
        except:
            self.__del__()

    def chat(self):
        self.waiting()
        self.send_message()

    def waiting(self):
        self.label_notice["text"] = "Waiting"


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("File Sharing Application")
        self.geometry("500x200")
        self.resizable(width=False, height=False)

        self.container = tk.Frame()
        self.client_page = Client_Page(self.container)

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.client_page.grid(row=0, column=0, sticky="nsew")

        self.client_page.tkraise()


app = App()
app.mainloop()
