import random
import socket
import socketserver
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
    # totalScores=[] # array to save cumulative scores
    for i in range(len(clients)):
        timesend=time.ctime()##To calculate RTT.
        clients[i].sendall(f"the number is: {str({randomnumber})}".encode('ascii'))

        answer=clients[i].recv(1024).decode('ascii')##Recieving player's answer.
        ##+ add timer for player
        timereceived=time.ctime()
        RTT=timesend-timereceived
        if answer==randomnumber:
            scores[i]= RTT
            #totalScores.append((clients, RTT)) # add current round score to total score
            cumulative_score[i]+=scores[i] # add current round score to total score
        else:
            scores[i]==0##Player disqualified from round.
            disqualify_msg = 'You entered the wrong number and are disqualified from this round.'
            clients.send(disqualify_msg.encode())

        #cumulative_score[i]+=scores[i]
        # send results and cumulatives after each round
        print(f'Results for round {i+1} :')
        cumulative_score[i].sort(key=lambda x: x[1])
        for i, cumulative_score in enumerate(clients):
            print('Round ', i+1, ': Player ', i+1, ':', scores[1], 'seconds')
            print('Overall Score', cumulative_score[1], 's')


#Function that displays final scores and closes connections
def broadcast():
    winner = max(cumulative_score, key=cumulative_score.get)
    print('The Final Score Is: ')
    for client, cumulative_score in cumulative_score.items():
        print(f'Player {clients.index(clients)+1} : {cumulative_score}s')
    print(f'The Winner is ... {clients.index(winner)+1} !!!')

    # disconnect remaining players
    for client in clients:
        client.close()
    socketserver.close()
