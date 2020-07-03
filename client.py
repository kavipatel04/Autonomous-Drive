import socket               
import random
host = '169.254.184.24'# ip of raspberry pi 
port = 56582
def getMSG(socket):
    msg = socket.recv(1024)
    msg.decode("utf-8")
    return msg
while True:
    s = socket.socket()          
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    msg = s.recv(1024)
    msg = msg.decode("utf-8")
    if msg == "standby":
        print(msg)
    elif msg == "request":
        s.send(bytes(str(random.randint(20, 500)), 'utf-8'))
    s.close()