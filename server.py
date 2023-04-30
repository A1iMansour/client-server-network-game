import random
import socket
import socketserver
import time

import numpy as np

"""Remaining to do:
handle erors:
1-if some clients left game
2- if client or server didnt recieve answer
3- if client did'nt answer after long duration
...
Also,
should score and cumulative score be RTT
what is player was disqualified? 


"""


host= '127.0.0.1'##IP address for local host.
port=9589 ##Port number.

serv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)##socket to accept connections.

serv.bind((host,port))
serv.listen()
clients=[] #[(player1,0),(player2,1),(player3,2)]
scores={0:0,1:0,2:0} #values are  score and keys are players ID
roundnumber=0
cumulative_score={0:0,1:0,2:0}# values are cumulative score and keys are players ID
sortedcumulative_score={}
sortedscores={}
 ##Incase some player left the game

##Function to connect clients to server.
def connection():
    global sortedcumulative_score
    playernumber=1
    gamestarts=False
    while True:
        print("while loop entered")
        if gamestarts==False:#to avoid waiting for clients in next rounds
            csocket,address=serv.accept()##communication socket,each connection gets its socket.
            csocket.sendall("Welcome to the ultimate gaming experience!".encode('ascii'))##sending welcome message.
            clients.append((csocket,f"Player{playernumber}"))
            playernumber+=1

        print(f"while loop round number {roundnumber}")

        if len(clients)==3 and roundnumber<3:#Game acceptss 3 players, and three rounds
            gamestarts=True
            gamestarted()
        elif roundnumber>=3:##GAME ended.
            Final_score=next(iter(sortedcumulative_score))
            winner=f"Winner Winner chicken Dinner: Player{Final_score} with score:{sortedcumulative_score[Final_score]},s"
            print(winner)
            # disconnect remaining players
            for i in range(len(clients)):
             clients[i][0].sendall(f"{winner}".encode('ascii'))
             clients[i][0].close()
            csocket.close()
            break

##Function that handles game's logic.
def gamestarted():
    global cumulative_score
    global scores
    global roundnumber 
    global sortedscores
    global sortedcumulative_score
    roundnumber +=1
    randomnumber=random.randint(0,9)
    print(randomnumber)
    # totalScores=[] # array to save cumulative scores
    maxrtt=0 # to be used for player who is diqualified
    disqualified=[]
    for i in range(len(clients)):
        print( f"player:{i}")
        timesend=time.time()##To calculate RTT.
        clients[i][0].sendall(f"{str(randomnumber)}".encode('ascii'))

        answer=clients[i][0].recv(1024).decode('ascii')##Recieving player's answer.

        ##+ add timer for player
        timereceived=time.time()
        print(f"time send:{timesend} , time recieved:{timereceived}")
        RTT=timereceived-timesend
        if RTT>maxrtt:
            maxrtt=RTT
        if int(answer)==randomnumber:
            congrats = 'BRAVOO!!'
            clients[i][0].send(congrats.encode('ascii'))
            scores[i]= RTT
            #totalScores.append((clients, RTT)) # add current round score to total score
            cumulative_score[i]+=scores[i] # add current round score to total score
        else:#wrong answer, Player disqualified from round. 

            disqualified.append(i)#store diqualified players
            disqualify_msg = 'You entered the wrong number and are disqualified from this round.'
            clients[i][0].send(disqualify_msg.encode('ascii'))
    
    for i in range(len(disqualified)):
        scores[disqualified[i]]=maxrtt+1#disqualified player recieves highest RTT of current round + penalty
        cumulative_score[disqualified[i]]+=scores[disqualified[i]] # add current round score to total score
    # send results and cumulatives after each round
    print(f'Results for round {roundnumber} :')

    #sorting cumulative_score in ascending order
    key=list(cumulative_score.keys())#create list of keys
    score=list(cumulative_score.values())#create list of values
    indicesofsortedvalues=np.argsort(score)#get indices of values in ascending order
    sortedcumulative_score={key[i]: score[i] for i in indicesofsortedvalues}#sort dictionary based on indices
    
    #sorting scores of current round in ascending order
    key=list(scores.keys())#create list of keys
    score=list(scores.values())#create list of values
    indicesofsortedvalues=np.argsort(score)#get indices of values in ascending order
    sortedscores={key[i]: score[i] for i in indicesofsortedvalues}#sort dictionary based on indices
    #descending order, highest score is player with min RTT
    #printing in descending order this round's scores
    for j in sortedscores :
        print('Round ', roundnumber, ': Player ', j, ':', scores[j], 'seconds')
   
    #printing in descending order cumulative scores
    for j in sortedcumulative_score :
        print('Overall Score', 'Player ',j,':',cumulative_score[j], 's')   

"""the results of the current round and the cumulative scores of
each player in descending order must be displayed. After the three rounds, the
server should declare the winner and close the connection."""

##Main function.
def main():
    connection()

if __name__=='__main__':
    main()