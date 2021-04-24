import socket
import threading
import time

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = ('', PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
# socket.gethostname()

server = socket.socket()
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("ok你好".encode())
    conn.close()


def start():
    server.listen()
    print("[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print(conn, addr) #
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")  # 始终有一个线程在listen新链接，故 -1

start()