import tkinter as tk
from client import Client
from tkinter.filedialog import askopenfile
import threading


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


class Dead_Page(tk.Frame):
    def __init__(self, parrent, app_controller):
        tk.Frame.__init__(self, parrent)

        self.label_notice = tk.Label(self, text="Server is dead")
        self.label_notice.pack()


class Start_Page(tk.Frame):
    def __init__(self, parrent, app_controller):
        tk.Frame.__init__(self, parrent)

        self.label_welcome = tk.Label(
            self, text="Welcome to our file-sharing app")
        self.label_welcome.pack()

        self.label_option = tk.Label(self, text="Choose your option:")
        self.label_option.pack()

        self.button_share = tk.Button(
            self, text="Share your file", command=lambda: app_controller.show_page(Share_Page))
        self.button_share.pack()

        self.button_download = tk.Button(
            self, text="Download file", command=lambda: app_controller.show_page(Download_Page))
        self.button_download.pack()


class Share_Page(tk.Frame):
    def __init__(self, parrent, app_controller):
        tk.Frame.__init__(self, parrent)

        self.app_controller = app_controller

        self.button_back = tk.Button(
            self, text="Back", command=lambda: app_controller.show_page(Start_Page))
        self.button_back.pack()

        self.label_work = tk.Label(self, text="Choose your file:")
        self.label_work.pack()

        self.button_choose = tk.Button(
            self, text="Select file", command=self.publish)
        self.button_choose.pack()

        self.label_file = tk.Label(self, text="Nothing to share")
        self.label_file.pack()

    def publish(self):
        file = askopenfile()
        local_name = file.name
        file_name = local_name.split("/")[-1]
        self.label_file["text"] = "Waiting to publish"
        self.update_idletasks()

        pub = self.app_controller.client.publish(file_name, local_name)
        if pub:
            self.label_file["text"] = "Publish sucessfully, share new file"
            self.update_idletasks()
        else:
            self.label_file["text"] = "Publish failed, share new file"
            self.update_idletasks()


class Download_Page(tk.Frame):
    def __init__(self, parrent, app_controller):
        tk.Frame.__init__(self, parrent)

        self.app_controller = app_controller

        self.button_back = tk.Button(
            self, text="Back", command=lambda: app_controller.show_page(Start_Page))
        self.button_back.pack()

        self.label_work = tk.Label(self, text="Input name file to download:")
        self.label_work.pack()

        self.entry_file_name_var = tk.StringVar()

        self.entry_file_name = tk.Entry(
            self, textvariable=self.entry_file_name_var)
        self.entry_file_name.pack()

        self.button_get = tk.Button(
            self, text="Download", command=self.download_file)
        self.button_get.pack()

        self.label_notice = tk.Label(self, text="")
        self.label_notice.pack()

    def download_file(self):
        file_name = self.entry_file_name_var.get()
        self.entry_file_name_var.set("")

        if file_name == "":
            return

        self.label_notice["text"] = "Downloading " + file_name + "..."
        self.update_idletasks()

        get = self.app_controller.client.fetch(file_name)

        if get:
            self.label_notice["text"] = "Your file in " + \
                get + ", download new file"
            self.update_idletasks()
        else:
            self.label_notice["text"] = "Download failed, download new file"
            self.update_idletasks()


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.client = Client()

        self.title("File Sharing Application")
        self.geometry("300x150")
        # self.resizable(width=False, height=False)

        self.container = tk.Frame()

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in {Dead_Page, Start_Page, Share_Page, Download_Page}:
            frame = f(self.container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[f] = frame
        if self.client.status:
            self.frames[Start_Page].tkraise()
        else:
            self.frames[Dead_Page].tkraise()

    def show_page(self, frame):
        self.frames[frame].tkraise()

    def __del__(self):
        try:
            self.client.send_message("END")
            self.client.soc.close()
        except:
            None

    def app_run(self):
        thread1 = threading.Thread(target=self.client.client_run)
        thread1.daemon = False
        thread1.start()

        self.mainloop()
        self.client.socket_client.close()
        self.client.status = False


app = App()
app.app_run()
