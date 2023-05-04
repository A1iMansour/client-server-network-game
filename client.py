import select
import socket
import sys
import time
#Disconection error handling written by Ali Mansour and Adam Sabra
# This part was written by Christophe Kassab 
# specify the server's IP address and port number
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9889

# create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))

# receive the welcome message from the server
welcome_message = client_socket.recv(1024)
print(welcome_message.decode('ascii'))

for round_num in range(3):
    # receive the random number from the server
    try:
        random_number = client_socket.recv(1024)
    except ConnectionResetError:
            print(f"Game ended")

    print(f"Round {round_num + 1}:{random_number.decode('ascii')}")
    print('Type the number and press Enter: ')# prompt the user to input the number
    
#This part was written by Ali Mansour
    timer=time.time()                                        #get time at at which the number is send to calculate RTT
    waiting=0
    number=None
    # send the number to the server and record the start time
    while True:             #for 10 seconds timeout
        waiting=time.time()
        
        if number==None and waiting-timer<9.9: #9.9 to avoid error if user send just before 10 seconds
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                number = input("")
            pass
        elif number!=None:  
            try:  
                client_socket.send(number.encode('ascii'))
            except ConnectionResetError:
                print(f"Game ended")
            break
        
        elif waiting-timer>9.9:    #timeout                        
            break               

# This part was written by Christophe Kassab
    try:
        result = client_socket.recv(1024)# receive the round message from the server 
    except ConnectionResetError:
        print(f"Game ended")
    # display the result and the round trip time
    print(f"Result: Round {round_num + 1} : {result.decode('ascii')}")
    
    # receive and display the cumulative scores after each round
    try:
        cumulative_scores = client_socket.recv(1024)
    except ConnectionResetError:
        print(f"Game ended")
        round_num=4# exit loop
        break
    print(f"Cumulative scores after Round {round_num + 1}:\n{cumulative_scores.decode('ascii')}")

#display the final result
try:
    result = client_socket.recv(1024)
except ConnectionResetError:
    print(f"Game ended")
print(f"{result.decode('ascii')}")
# close the socket
client_socket.close()