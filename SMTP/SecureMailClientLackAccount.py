"""
SSL 加密
邮箱账户按自己的填写（E-mail account according to your own fill）
"""
import base64
import ssl

from socket import *

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
recv = []

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.163.com"

# Create socket called sslClientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 465))

# ssl
purpose = ssl.Purpose.SERVER_AUTH
context = ssl.create_default_context(purpose)

sslClientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

recv.append(sslClientSocket.recv(1024).decode())

if recv[-1][:3] != '220':
    print('220 reply not received from server.')

print(recv[-1])
# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
sslClientSocket.send(heloCommand.encode())
recv.append(sslClientSocket.recv(1024).decode())
print(recv[-1])

# Login
LoginCommand = 'AUTH LOGIN\r\n'  # 命令要加\r\n
User = b'你的账户'
Psw = b'你的密码'

UserB64 = base64.b64encode(User)
PswB64 = base64.b64encode(Psw)

sslClientSocket.send(LoginCommand.encode())
recv.append(sslClientSocket.recv(1024).decode())
print(recv[-1])
sslClientSocket.send(UserB64 + b'\r\n')
recv.append(sslClientSocket.recv(1024).decode())
print(recv[-1])
sslClientSocket.send(PswB64 + b'\r\n')
recv.append(sslClientSocket.recv(1024).decode())
print(recv[-1])

# Send MAIL FROM command and print server response.

FromCommand = 'mail from: <your_email_address>\r\n'
sslClientSocket.send(FromCommand.encode())
recv.append(sslClientSocket.recv(1024).decode())
print(recv[-1])

# Send RCPT TO command and print server response.
ToCommand = 'rcpt to: <recipient_email_address>\r\n'
sslClientSocket.send(ToCommand.encode())
recv.append(sslClientSocket.recv(1024).decode())
print(recv[-1])

# Send DATA command and print server response.
DataCommand = 'data'
sslClientSocket.send(DataCommand.encode())

# Send message data.
header = f'''
from: <your_email_address>
to: <recipient_email_address>
subject: test
'''
sslClientSocket.send((header + msg).encode())

# Message ends with a single period.
sslClientSocket.send(endmsg.encode())
recv.append(sslClientSocket.recv(1024).decode())
print(recv[-1])

# Send QUIT command and get server response.

QuitCommand = 'QUIT\r\n'
sslClientSocket.send(QuitCommand.encode())
recv.append(sslClientSocket.recv(1024).decode())
print(recv[-1])
recv.append(sslClientSocket.recv(1024).decode())
print(recv[-1])