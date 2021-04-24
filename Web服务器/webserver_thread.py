import sys  # In order to terminate the program
import threading

from socket import *

SERVER = gethostbyname(gethostname())
PORT = 18888
ADDR = (SERVER, PORT)

HEADER = 64
BUFSIZE = 4096
FORMAT = 'UTF-8'
CLOSE_CONNECTION = '!QUIT'

serverSocket = socket(AF_INET, SOCK_STREAM) #Prepare a sever socket
serverSocket.bind(ADDR)


def start():
    print('Ready to serve...')
    serverSocket.listen()
    while True:
        connectionSocket, addr = serverSocket.accept()
        thread = threading.Thread(target=handle_client, args=(connectionSocket,))
        thread.start()
        print(f"[当前连接数量]: {threading.activeCount() - 1}") # 去除创立的线程

def handle_client(connectionSocket):
    while True:
        try:
            message = connectionSocket.recv(BUFSIZE).decode(FORMAT)
            if message == CLOSE_CONNECTION:
                break

            filename = message.split()[0]

            f = open(filename[1:])

            outputdata = f.readlines()

            # Send one HTTP header line into socket
            connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode(FORMAT))

            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())

            # connectionSocket.close()

        except (OSError, IOError):
            # Send response message for file not found

            connectionSocket.send('HTTP/1.1 404 Not found\r\n\r\n'.encode(FORMAT))
            # connectionSocket.send('文件不存在\r\n'.encode(FORMAT))

    # Close client socket
    connectionSocket.close()

start()
serverSocket.close()
sys.exit()


