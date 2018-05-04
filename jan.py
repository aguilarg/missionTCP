# import modules
from socket import *   # used for socket configurations 
import sys             # used to get arguments on command line 
import time
    
janToAnn = []
janToChan = []

fp = open('Jan-_Ann.txt') 
janToAnn = fp.read().split("\n") 
fp.close() 
fp = open('Jan-_Chan.txt') 
janToChan = fp.read().split("\n") 
fp.close() 

# connect to port with incomming messages 
port = 8085             # this router, F, gets connected to port 8084 as a client        
serverName = "localhost"

clientSocket = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
clientSocket.connect((serverName, port)) # connects the client and the server together
print("sucessfully connected. Ready to send message on port " + str(port) + "...")

def getPathAndMessage(data):
    # extract path from data
    data = data.decode()               # decode message because the data is coming as a bytes            
    data = data.split('/')
    path = data[0]
    message = data[1]
    
    return (path, message)
i = 0
print(len(janToAnn))
while i < len(janToAnn):
    # receive message from sender
    data = clientSocket.recv(1024) 
    path, message = getPathAndMessage(data)
    time.sleep(1)   # wait 1 second the print message
    print("\nMessage received.")
    print("Ann:", message)
    print("")
    """
    print("____________________________________")
    print("\nDebugging Details (received data):")
    print("path = ", path)
    print("message = ", message,"\n")
    print("____________________________________")
    """

    path = "8083 8082 8081 8080/"
    message = janToAnn[i]
    data = path + message

    # Send data with message and path
    clientSocket.send(data.encode())
    print("Jan:", message)
    print("Message sent.")
    time.sleep(1)
    i +=1
#clientSocket.close()  # close the socket since we are done using it