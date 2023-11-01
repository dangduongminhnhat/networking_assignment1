import socket
import threading

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

        self.accept_connection(conn, addr)

        while True:
            end = self.receive_message(conn, addr)
            if end:
                break
        print("client", addr, "finished")
        print(conn.getsockname(), "closed")
        conn.close()

    def accept_connection(self, conn, addr):
        rec = conn.recv(1024).decode(FORMAT)
        print("Receive =", rec)
        if rec == "REQUEST":
            conn.sendall("RESPONSE 200".encode(FORMAT))
        else:
            conn.sendall("RESPONSE 404".encode(FORMAT))

    def receive_message(self, conn, addr):
        try:
            message = conn.recv(1024).decode(FORMAT)
            if message == "END":
                return True
            print("client:", addr, ", talks:", message)
            data = input("Send back to client" + addr[0] + ": ")

            conn.sendall(data.encode(FORMAT))

            return False
        except:
            return True


server = Server()
server.server_run()
server.soc.close()
