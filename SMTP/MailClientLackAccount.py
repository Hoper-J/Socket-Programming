"""
非 SSL 加密
邮箱账户按自己的填写（E-mail account according to your own fill）
"""
import base64

from socket import *

msg = "\r\n I love computer networks!" # 信息前面需空行
endmsg = "\r\n.\r\n"
recv = []

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.163.com"

# Create socket called sslClientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 25))

recv.append(clientSocket.recv(1024).decode())

if recv[-1][:3] != '220':
    print('220 reply not received from server.')
print(recv[-1])

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv.append(clientSocket.recv(1024).decode())
print(recv[-1])

# Login
LoginCommand = 'AUTH LOGIN\r\n' # 要加\r\n，否则会报 504 错误
User = b'你的账户'
Psw = b'你的密码'

UserB64 = base64.b64encode(User) # 账号密码需要base64加密
PswB64 = base64.b64encode(Psw)

clientSocket.send(LoginCommand.encode())
recv.append(clientSocket.recv(1024).decode())
print(recv[-1])

clientSocket.send(UserB64 + b'\r\n')
recv.append(clientSocket.recv(1024).decode())
print(recv[-1])

clientSocket.send(PswB64 + b'\r\n')
recv.append(clientSocket.recv(1024).decode())
print(recv[-1])

# Send MAIL FROM command and print server response.

FromCommand = 'mail from: <your_email_address>\r\n'
clientSocket.send(FromCommand.encode())
recv.append(clientSocket.recv(1024).decode())
print(recv[-1])

# Send RCPT TO command and print server response.
ToCommand = 'rcpt to: <recipient_email_address>\r\n'
clientSocket.send(ToCommand.encode())
recv.append(clientSocket.recv(1024).decode())
print(recv[-1])

# Send DATA command and print server response.
DataCommand = 'data'
clientSocket.send(DataCommand.encode())

# Send message data.
header = f'''
from: <your_email_address>
to: <recipient_email_address>
subject: test
'''
clientSocket.send((header + msg).encode())

# Message ends with a single period.
clientSocket.send(endmsg.encode())
recv.append(clientSocket.recv(1024).decode())
print(recv[-1])

# Send QUIT command and get server response.
QuitCommand = 'QUIT\r\n'
clientSocket.send(QuitCommand.encode())
recv.append(clientSocket.recv(1024).decode())
print(recv[-1])
recv.append(clientSocket.recv(1024).decode())
print(recv[-1])