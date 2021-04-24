from socket import *
import sys  # In order to terminate the program


SERVER = gethostbyname(gethostname())
PORT = 18888
ADDR = (SERVER, PORT)

BUFSIZE = 4096
FORMAT = 'UTF-8'

serverSocket = socket(AF_INET, SOCK_STREAM) #Prepare a sever socket
serverSocket.bind(ADDR)

while True:
    print('Ready to serve...')
    serverSocket.listen()
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(BUFSIZE).decode(FORMAT)

        filename = message.split()[1]

        f = open(filename[1:])

        outputdata = f.readlines()

        # Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode(FORMAT))

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        # Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 Not found\r\n\r\n'.encode(FORMAT))
        connectionSocket.send('文件不存在\r\n'.encode(FORMAT))
        # Close client socket
        connectionSocket.close()

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data
