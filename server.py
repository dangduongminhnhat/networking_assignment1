import socket
import threading
import json

HOST = "192.168.56.1"
IP = "192.168.1.12"
SERVER_PORT = 65432
FORMAT = "utf8"


print("SERVER SIDE")
print("server:", HOST, SERVER_PORT)
print("Waiting for Client")


class Server:
    def __init__(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.soc.bind((HOST, SERVER_PORT))
        self.soc.listen()

        self.clients = {}
        self.file_names = {}

    def server_run(self):
        nClient = 0
        while nClient < 1:
            try:
                conn, addr = self.soc.accept()

                thr = threading.Thread(
                    target=self.handle_client, args=(conn, addr))
                thr.daemon = False
                thr.start()

            except:
                print("Error")

            nClient += 1

    def handle_client(self, conn, addr):
        print("client address:", addr)
        print("conn:", conn.getsockname())

        accept = self.accept_connection(conn, addr)

        while accept:
            end = self.receive_message(conn, addr)
            if end:
                break
        print("client", addr, "finished")
        print(conn.getsockname(), "closed")
        conn.close()

    def accept_connection(self, conn, addr):
        rec = conn.recv(1024).decode(FORMAT)
        print("client:", addr, ", talks:", rec)
        if rec == "REQUEST CONNECTION":
            conn.sendall("RESPONSE 200".encode(FORMAT))
            return True
        else:
            conn.sendall("RESPONSE 404".encode(FORMAT))
            return False

    def receive_message(self, conn, addr):
        try:
            message = conn.recv(1024).decode(FORMAT)
            print("client:", addr, ", talks:", message)
            if message == "END":
                return True
            elif message == "REQUEST PUBLISH":
                self.publish(conn, addr)
            return False
        except:
            return True

    def publish(self, conn, addr):
        rec = conn.recv(1024).decode(FORMAT)
        rec = json.loads(rec)

        if not "file_name" in rec or not "local_name" in rec:
            conn.sendall("RESPONSE 404".encode(FORMAT))
            return
        elif not addr in self.clients:
            self.clients[addr] = {rec["file_name"]: rec["local_name"]}
        else:
            if rec["file_name"] in self.clients[addr]:
                conn.sendall("RESPONSE 404".encode(FORMAT))
                return
            self.clients[addr][rec["file_name"]] = rec["local_name"]
        if rec["file_name"] not in self.file_names:
            self.file_names[rec["file_name"]] = [addr]
        else:
            self.file_names.append(addr)
        conn.sendall("RESPONSE 200".encode(FORMAT))


server = Server()
server.server_run()
server.soc.close()
