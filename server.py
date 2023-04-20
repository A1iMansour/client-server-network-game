import socket
import time

host= "10.169.20.37"#IP address for local host
port=9899

serv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#socket to accept connections

serv.bind((host,port))
serv.listen()


while True:
    csocket,address=serv.accept()#communication socket,each connection gets its socket





    