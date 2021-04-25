# Test URL：http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file1.html
import sys

from socket import *

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n'
          '[server_ip : It is the IP Address Of Proxy Server\n'
          'The default address is 0.0.0.0')
    IP = ''
    # sys.exit(2)
else:
    IP = sys.argv[1]

PORT = 8086
FORMAT = 'utf-8'

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((IP, PORT))
tcpSerSock.listen()

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(2048).decode()
    print(message)
    # Extract the filename from the given message print(message.split()[1])
    print(message.split()[1])
    filename = message.split()[1].partition("//")[2]
    # filename = message.split()[1].split(':')[0]
    print(filename)
    fileExist = "false"
    filetouse = "./" + filename.replace('/', '_')
    print(filetouse)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse, "r")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n".encode())

        # Send the content of the requested file to the client
        for data in outputdata:
            tcpCliSock.send(data.encode(FORMAT))
        tcpCliSock.send("\r\n".encode(FORMAT))

        print('Read from cache')

    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM) # Fill in start. # Fill in end.
            hostn = filename.replace("www.", "", 1).split('/')[0]
            print(f'Host: {hostn}')
            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))

                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                fileobj.write(message.encode())

                # Read the response into b_buffer
                b_buffer = fileobj.read() # 这里没有 decode()
                print(b_buffer)
                # Create a new file in the cache for the requested file.
                # Also send the response in the b_buffer to client socket and the corresponding file in the cache
                tcpCliSock.send(b_buffer)

                tmpFile = open("./" + filename.replace('/', '_'), "w+b") # 事实上这里的路径等于 filetouse

                # https://stackoverflow.com/questions/48639285/a-bytes-like-object-is-required-not-int
                tmpFile.write(b_buffer) # 不要对 bytes 使用 writelines
                tmpFile.close()

                fileobj.close()

            except:
                print('Illegal request')
        else:
            # HTTP response message for file not found
            tcpCliSock.send('404 not found'.encode())

    # Close the client and the server sockets
    tcpCliSock.close()
tcpSerSock.close()