import socket

# This code was written by Christophe Kassab 
# specify the server's IP address and port number
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9989

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

    print(f"Round {round_num + 1}: Random number is {random_number.decode('ascii')}")

    # prompt the user to input the number
    number = input("Type the number and press Enter: ")

    # send the number to the server and record the start time
    client_socket.send(number.encode('ascii'))

    # receive the round message from the server 
    result = client_socket.recv(1024)
    

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