# import modules
from socket import *   # used for socket configurations 
import sys             # used to get arguments on command line 
import time
    
# connect to port with incomming messages 
port = 8088              # this router, F, gets connected to port 8084 as a client        
serverName = "localhost"

clientSocket = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
clientSocket.connect((serverName, port)) # connects the client and the server together
print("sucessfully connected. Ready to send message on port " + str(port) + "...")

while True:
    # receive message from sender
    message = clientSocket.recv(1024) 
    message = message.decode()

    # close connection if Jan sends that command
    if(message == "close"):
        clientSocket.close()
        print("terminating...")
        sys.exit()

    print("\nMessage received.")
    print("Jan:", message)
    print("")
    var = input("H's message: ")
    message = str(var)

    # Send data with message and path
    clientSocket.send(message.encode())
    print("airforceH:", message)
    print("Message sent.")

#clientSocket.close()  # close the socket since we are done using it