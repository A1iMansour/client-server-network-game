import select
import socket
import sys
import time

# This part was written by Christophe Kassab 
# specify the server's IP address and port number
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9789

# create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))

# receive the welcome message from the server
welcome_message = client_socket.recv(1024)
print(welcome_message.decode('ascii'))

for round_num in range(3):
    # receive the random number from the server
    random_number = client_socket.recv(1024)

    print(f"Round {round_num + 1}:{random_number.decode('ascii')}")
    print('Type the number and press Enter: ')# prompt the user to input the number
    
#This part was written by Ali Mansour
    timer=time.time()                                        #get time at at which the number is send to calculate RTT
    waiting=0
    number=None
    # send the number to the server and record the start time
    while True:
        waiting=time.time()
        
        if number==None and waiting-timer<9.9:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                number = input("")
            pass
        elif number!=None:    
            client_socket.send(number.encode('ascii'))
            break
        
        elif waiting-timer>9.9:    #timeout                        
            break               

# This part was written by Christophe Kassab
    result = client_socket.recv(1024)# receive the round message from the server 
    # display the result and the round trip time
    print(f"Result: Round {round_num + 1} : {result.decode('ascii')}")
    
    # receive and display the cumulative scores after each round
    cumulative_scores = client_socket.recv(1024)
    print(f"Cumulative scores after Round {round_num + 1}:\n{cumulative_scores.decode('ascii')}")

#display the final result
result = client_socket.recv(1024)
print(f"{result.decode('ascii')}")
# close the socket
client_socket.close()