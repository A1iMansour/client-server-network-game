import random
import socket
import time

host= "10.169.20.37"##IP address for local host.
port=9899 ##Port number.

serv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)##socket to accept connections.

serv.bind((host,port))
serv.listen()
clients=[] #[(player1,0),(player2,1),(player3,2)]
scores={0:0,1:0,2:0} #values are cumulative score and keys are players ID
roundnumber=0
cumulative_score={0:0,1:0,2:0}# values are cumulative score and keys are players ID
gamestarts=False ##Incase some player left the game
##Main function.
def main():
    connection()

if __name__=='__main__':
    main()



##Function to connect clients to server.
def connection():
    playernumber=1
    while True:
        csocket,address=serv.accept()##communication socket,each connection gets its socket.
        csocket.sendall("Welcome to the ultimate gaming experience!".encode('ascii'))##sending welcome message.
        clients.append((csocket,f"Player{playernumber}"))
        playernumber+=1



        if len(clients)==3 and roundnumber<4:#Game acceptss 3 players, and three rounds
            gamestarts=True
            gamestarted()
        elif gamestarts:##GAME ended.
            sorted_results=sorted(cumulative_score)#sorted IDs based on scores
            print(f"Winner winner chicken dinner:{sorted_results[-1]},score:{cumulative_score[sorted_results[-1]]}")

##Function that handles game's logic.
def gamestarted():
    global roundnumber 
    roundnumber +=1
    randomnumber=random.randint(0,9)
    for i in range(len(clients)):
        timesend=time.ctime()##To calculate RTT.
        clients[i].sendall(f"{str({randomnumber})}".encode('ascii'))

        answer=clients[i].recv(1024).decode('ascii')##Recieving player's answer.
        ##+ add timer for player
        timerecieved=time.ctime()
        RTT=timesend-timerecieved
        if answer==randomnumber:
            scores[i]= RTT
        else:
            scores[i]==0##Player disqualified from round.

        cumulative_score[i]+=scores[i]


#Function that sends results and cumlative scores.
def broadcast():

