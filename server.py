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
"""

# This part was written by Maya Chami
host= '127.0.0.1'##IP address for local host
port=9989 ##Port number.
serv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)##socket to accept connections.
serv.bind((host,port))
serv.listen()

# This part was written by Ali Mansour
clients=[]              #list of tuples to store socket and player with number as follows[(socket,player1),(socket,player2)...]
scores={0:0,1:0,2:0}    #dictionary where values are round's score and keys are player's ID
roundnumber=0           #initialize round number to 0
cumulative_score={0:0,1:0,2:0}#dictionary where values are cumulative score and keys are players ID
sortedcumulative_score={}     #sorted dictionary where values are cumulative score and keys are players ID
sortedscores={}               #sorted dictionary where values are round's score and keys are player's ID

#Function to connect clients to server.
def connection():
    global sortedcumulative_score
    playernumber=1                          #initializing playernumber to 1
    gamestarts=False                        #initializing gamestarts to False
    while True:
        if gamestarts==False:               #check if game starts, to avoid waiting for clients at the end of each round
            csocket,address=serv.accept()   #communication socket,each connection gets its socket.
            csocket.sendall("Welcome to the ultimate gaming experience!".encode('ascii'))   #sending welcome message.
            clients.append((csocket,f"Player{playernumber}"))               #add the client info to list
            playernumber+=1                                                 #increment playernumber                             

        if len(clients)==3 and roundnumber<3:#check if reached number of clients required (3) and if round number is less than 3
            gamestarts=True                  #set gamestarts to True
            gamestarted()                    #call gamestarted function



        # This part was written by Maya Chami
        elif roundnumber>=3:                                #check if roundnumber>3, in that case GAME ended
            Final_score=next(iter(sortedcumulative_score))  #git number of player with highest score
            winner=f"Winner Winner chicken Dinner: Player{Final_score} with score:{sortedcumulative_score[Final_score]},s"
            print(winner)                                   #displaying winner with score
            # disconnect remaining players
            for i in range(len(clients)):                   
                clients[i][0].sendall(f"{winner}".encode('ascii'))  #send to all clients who is winner
                clients[i][0].close()                               #close connection with client
            csocket.close()                     #close socket
            break                               #break loop


# This part was written by Ali Mansour
#Function that handles game's logic
def gamestarted():
    global cumulative_score
    global scores
    global roundnumber 
    global sortedscores
    global sortedcumulative_score
    roundnumber +=1                     #increment round number
    randomnumber=random.randint(0,9)    #generating random number from 0 to 9
    maxrtt=0                            # to be used for penalty for player who is diqualified
    disqualified=[]                     # to be used to store players who are diqualified
    for i in range(len(clients)):
        
        clients[i][0].sendall(f"{str(randomnumber)}".encode('ascii'))#sending random number to client
        timesend=time.time()                                        #get time at at which the number is send to calculate RTT
        answer=clients[i][0].recv(1024).decode('ascii')             #Recieving player's answer
        ##+ add timer for player
        timereceived=time.time()                                    #get time at at which the answer is recieved to calculate RTT
        print(f"time send:{timesend}, time recieved:{timereceived}")#printing time send and time recieved just to track
        RTT=timereceived-timesend                                   #calculating RTT
        if RTT>maxrtt:                                              #check if we need to update maxrtt
            maxrtt=RTT                                              #update maxrtt
        if int(answer)==randomnumber:                               #check if answer is correct
            congrats = 'BRAVOO!!'
            clients[i][0].send(congrats.encode('ascii'))            #sends congrats to client
            scores[i]= RTT                                          #store this round's score
            cumulative_score[i]+=scores[i]                          #add current round score to total score
        else:                                                       #wrong answer, Player disqualified from round 
            disqualified.append(i)                                  #store diqualified players
            disqualify_msg = 'You entered the wrong number and are disqualified from this round.'
            clients[i][0].send(disqualify_msg.encode('ascii'))      #sending disqualified message to client
    
    for i in range(len(disqualified)):
        scores[disqualified[i]]=maxrtt+5                                #disqualified player recieves penalty: highest RTT of current round +  5
        cumulative_score[disqualified[i]]+=scores[disqualified[i]]      #add current round score to total score
    # send results and cumulatives after each round

    #sorting cumulative_score in ascending order
    key=list(cumulative_score.keys())                                           #create list of keys
    score=list(cumulative_score.values())                                       #create list of values
    indicesofsortedvalues=np.argsort(score)                                     #get indices of values in ascending order
    sortedcumulative_score={key[i]: score[i] for i in indicesofsortedvalues}    #sort dictionary based on indices
    
    #sorting scores of current round in ascending order
    key=list(scores.keys())                                         #create list of keys
    score=list(scores.values())                                     #create list of values
    indicesofsortedvalues=np.argsort(score)                         #get indices of values in ascending order
    sortedscores={key[i]: score[i] for i in indicesofsortedvalues}  #sort dictionary based on indices
    #descending order, highest score is player with min RTT


# This part was written by Maya Chami 
    #printing in descending order this round's scores and sending them to clients
    result=f'Results for round {roundnumber} :'+"\n"
    for j in sortedscores :
        result+='Round '+str(roundnumber)+  ': Player '+  str(j)+  ':'+  str(scores[j])+  ' seconds\n'
   
    #printing in descending order cumulative scores
    for j in sortedcumulative_score :
        result+='Overall Score:  Round '+  str(roundnumber)+ ': Player '+ str(j)+ ':'+ str(scores[j])+ ' seconds\n'

    print(result)   
    for i in range(len(clients)):
        clients[i][0].sendall(result.encode('ascii'))


#Main function
def main():
    connection()

if __name__=='__main__':
    main()