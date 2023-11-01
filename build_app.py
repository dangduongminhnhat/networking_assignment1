import tkinter as tk
from tkinter.simpledialog import askstring
from client import Client


class Client_Page(tk.Frame):
    def __init__(self, parrent):
        tk.Frame.__init__(self, parrent)

        self.label_title = tk.Label(self, text="Client Side")
        self.label_title.grid(row=0, column=0)

        self.label_chat = tk.Label(self, text="input message")
        self.label_chat.grid(row=1, column=0)

        self.entry_message_var = tk.StringVar()

        self.entry_message = tk.Entry(
            self, textvariable=self.entry_message_var)
        self.entry_message.grid(row=2, column=0)

        self.label_notice = tk.Label(self, text="")
        self.label_notice.grid(row=3, column=0)

        self.button_chat = tk.Button(
            self, text="chat", command=self.chat)
        self.button_chat.grid(row=4, column=0)

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
            message = self.entry_message_var.get()
            self.entry_message_var.set("")
            self.label_notice["text"] = "Waiting Server"
            self.update_idletasks()
            if message == "":
                return
            self.client.send_message(message)
        except:
            self.__del__()

    def receive_message(self):
        rec = self.client.receive_message()
        self.label_notice["text"] = "Server responses: " + rec
        self.update_idletasks()

    def chat(self):
        self.send_message()
        self.receive_message()


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("File Sharing Application")
        self.geometry("500x200")
        # self.resizable(width=False, height=False)

        self.container = tk.Frame()
        self.client_page = Client_Page(self.container)

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.client_page.grid(row=0, column=0, sticky="nsew")

        self.client_page.tkraise()


app = App()
app.mainloop()
