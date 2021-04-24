import socket
import time

PORT = 12000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

time_queue = []
loss_number = 0


def send(msg):
    try:
        message = msg.encode(FORMAT)
        b = time.time()
        client.sendto(message, ADDR)
        client.settimeout(0.1)
        modified_msg = client.recv(2048).decode()
        a = time.time()
        time_queue.append(a-b)
        print(f"RESPONSE: {modified_msg}")
        print(f"RTT: {time_queue[-1]}s")
    # print(client.recv(2048).decode())
    except socket.timeout:
        global loss_number
        loss_number += 1
        print("Request timed out!")


for i in range(1,11):
    send(f"Ping {i} {time.asctime()}")
else:
    client.close()
    print(f"""---ping statics---
10 transmitted, {10 - loss_number} received, {loss_number/10:.2%} loss
min/max/avg: {min(time_queue):f}/{max(time_queue):f}/{sum(time_queue)/10:f} s
    """)
# send(input())