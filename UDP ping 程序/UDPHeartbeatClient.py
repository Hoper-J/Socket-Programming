import socket
import threading
import time


PORT = 12000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

noTransferSequence = True
sequenceLength = 5  # 指定message的发送格式，以序列 12 为例：f"   12{TIME}"


def listen_recv():
    while True:
        print(client.recv(2048).decode())


def send_length():
    global noTransferSequence
    while noTransferSequence:
        client.sendto(str(sequenceLength).encode(FORMAT), ADDR)
        status = client.recv(2048).decode()
        if status == 'Length OK':
            noTransferSequence = False
            # 创建线程监听收到的信息
            threading.Thread(target=listen_recv).start()

        print(status)


def send(msg):
    send_length()
    client.sendto(msg.encode(FORMAT), ADDR)
    time.sleep(0.1)


i = 0
while True:
    message = f"{i:{sequenceLength}}{time.time()}"  # message[:sequenceLength]存放序列号
    send(message)
    i += 1

# send(input())