import tkinter as tk
from client import Client
from tkinter.filedialog import askopenfile
import threading
from tkinter import ttk
import json


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

        self.button_list = tk.Button(
            self, text="List file", command=lambda: app_controller.show_page(List_Page))
        self.button_list.pack()


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
            self, text="Select file", command=self.select_file)
        self.button_choose.pack()

        self.label_choose = tk.Label(self, text="Input your file name:")
        self.label_choose.pack()

        self.entry_local_name_var = tk.StringVar()

        self.entry_local_name = tk.Entry(
            self, textvariable=self.entry_local_name_var)
        self.entry_local_name.pack()

        self.button_publish = tk.Button(
            self, text="Publish", command=self.publish)
        self.button_publish.pack()

        self.label_file = tk.Label(self, text="Nothing to share")
        self.label_file.pack()

    def select_file(self):
        self.file = askopenfile()

        self.label_file["text"] = "Your selected file is " + self.file.name
        self.update_idletasks()

    def publish(self):
        try:
            local_name = self.file.name
            self.file = None
        except:
            self.label_file["text"] = "You have to select file"
            self.update_idletasks()

            return
        file_name = self.entry_local_name_var.get()

        if "." in local_name:
            post_fix_local = local_name.split(".")[-1]
            if not "." in file_name:
                self.label_file["text"] = "Your file's name has to be *." + \
                    post_fix_local
                self.update_idletasks()

                return
            post_fix_file = file_name.split(".")[-1]
            if post_fix_file != post_fix_local:
                self.label_file["text"] = "Your file's name has to be *." + \
                    post_fix_local
                self.update_idletasks()

                return

        self.label_file["text"] = "Waiting to publish"
        self.entry_local_name_var.set("")
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


class List_Page(tk.Frame):
    def __init__(self, parrent, app_controller):
        tk.Frame.__init__(self, parrent)

        self.app_controller = app_controller

        self.button_back = tk.Button(
            self, text="Back", command=lambda: app_controller.show_page(Start_Page))
        self.button_back.pack()

        self.scroll = tk.Scrollbar(self)
        self.scroll.pack(side='right', fill='y')

        self.scroll = tk.Scrollbar(self, orient='horizontal')
        self.scroll.pack(side='bottom', fill='x')

        self.table = ttk.Treeview(
            self, yscrollcommand=self.scroll.set, xscrollcommand=self.scroll.set)
        self.table.pack()

        self.scroll.config(command=self.table.yview)
        self.scroll.config(command=self.table.xview)

        self.table['columns'] = ('File Name', 'Host Name')

        self.table.column("#0", width=0,  stretch=False)
        self.table.column("File Name", anchor="center", width=200)
        self.table.column("Host Name", anchor="center", width=200)

        self.table.heading("#0", text="", anchor="center")
        self.table.heading("File Name", text="File Name", anchor="center")
        self.table.heading("Host Name", text="Host Name", anchor="center")

        self.button_get = tk.Button(
            self, text="Get list", command=self.get_list)
        self.button_get.pack()

    def get_list(self):
        for row in self.table.get_children():
            self.table.delete(row)

        lis = self.app_controller.client.get_list()
        lis = json.loads(lis)

        count = 0
        for file in lis:
            self.table.insert(
                parent='', index='end', iid={count}, text='', values=(file, lis[file]))
            count += 1

        self.update_idletasks()


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.client = Client()

        self.title("File Sharing Application")
        self.geometry("500x500")

        self.container = tk.Frame()

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in {Dead_Page, Start_Page, Share_Page, Download_Page, List_Page}:
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
        try:
            self.client.socket_client.close()
            self.client.status = False
        except:
            None


app = App()
app.app_run()
