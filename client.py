import socket
import json

HOST = "192.168.56.1"
SERVER_PORT = 65432
FORMAT = "utf8"


class Client:
    def __init__(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("CLIENT SIDE")
        self.status = self.init_connection()
        print(self.status)

    def init_connection(self):
        try:
            self.soc.connect((HOST, SERVER_PORT))
            self.send_message("REQUEST CONNECTION")

            rec = self.receive_message()
            return rec
        except:
            return None

    def send_message(self, message):
        self.soc.sendall(message.encode(FORMAT))

    def receive_message(self):
        return self.soc.recv(1024).decode(FORMAT)

    def publish(self, file_name, local_name):
        self.send_message("REQUEST PUBLISH")

        rec = self.receive_message()
        print(rec)

        if rec == "RESPONSE 200":
            file_package = {"file_name": file_name, "local_name": local_name}
            file_package = json.dumps(file_package)

            self.send_message(file_package)

            rec = self.receive_message()
            print(rec)

            if rec == "RESPONSE 200":
                return True
            else:
                print("------")
                return False
        else:
            return False
