"""
time.time()在不同平台上可能会有不同表现，这里仅为了本地演示
ps: 对心跳包不太了解，按自己理解做了个简单的
"""

# We will need the following module to generate randomized lost packets
import random
import threading
import time
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('', 12000))

TIMEOUT = 2  # 设定心跳包间隔不超过 2 秒
sendTimeSequence = []  # 心跳包时间序列

noSequenceLength = True  # 标识是否收到序列长度
noThreadMonitoring = True  # 标识是否有线程监控超时


def handle_heatbeat(sequence_length):
    while sequence_length:
        time.sleep(0.1)
        now_time = time.time()
        latest_send = sendTimeSequence[-1]  # 获取最近一次客户端发送心跳包的时间
        if now_time - latest_send > TIMEOUT:
            serverSocket.close()
            break


def start():
    global noSequenceLength, noThreadMonitoring
    print('Ready to serve')
    latest_number = 0
    sequence_length = 0
    while True:
        try:
            # Generate random number in the range of 0 to 10
            rand = random.randint(0, 10)
            # Receive the    client packet along with the address it is coming from
            message, address = serverSocket.recvfrom(1024)
            # If rand is less is than 1, we consider the packet lost and do not respond
            if rand < 1:
                if noSequenceLength:
                    serverSocket.sendto(b'Retransmission', address)
                continue

            # Otherwise, the server responds
            msg = message.decode()
            if noSequenceLength:  # 此时已经收到序列长度，对第一次收到的序列长度进行处理
                sequence_length = int(msg[:5])
                noSequenceLength = False
                serverSocket.sendto(b'Length OK', address)
                continue

            number = int(msg[:sequence_length])
            sendTimeSequence.append(float(msg[sequence_length:]))
            if noThreadMonitoring:
                threading.Thread(target=handle_heatbeat,args=(sequence_length,)).start()
                noThreadMonitoring = False

            for i in range(latest_number + 1, number):  # 若间隔为1，则代表未丢失，不需回复
                serverSocket.sendto(f'{i} have lost'.encode(), address)
            latest_number = number
        except OSError:
            print('CLOSE')
            break


if __name__ == '__main__':
    start()