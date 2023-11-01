import socket

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"


class Client:
    def __init__(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("CLIENT SIDE")
        self.status = self.init_connection()
        print("Status:", self.status)

    def init_connection(self):
        try:
            self.soc.connect((HOST, SERVER_PORT))
            self.soc.sendall("REQUEST".encode(FORMAT))

            rec = self.soc.recv(1024).decode(FORMAT)
            return rec
        except:
            return None

    def send_message(self, message):
        self.soc.sendall(message.encode(FORMAT))

        return self.soc.recv(1024).decode(FORMAT)
