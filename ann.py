# import modules
from socket import *   # used for socket configurations 
import sys             # used to get arguments on command line 
import time


def getPathAndMessage(data):
    # extract path from data
    data = data.decode()               # decode message because the data is coming as a bytes            
    data = data.split('/')
    path = data[0]
    message = data[1]
    
    return (path, message)


    
annToChan = [] 


annToJan = []

for i in range(9):
    annToJan.append("g")
fp = open('Ann-_Chan.txt') 
annToChan = fp.read().split("\n") 
fp.close() 
fp = open('Ann-_Jan.txt') 
annToJan = fp.read().split("\n") 
fp.close() 



# Prepare a sever socket
serverPort = 8080
serverName = "localhost"
serverSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
serverSocket.bind((serverName, serverPort))  # bind the socket to the local address
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.listen(5)

print("Communication setup successfully.")
print ("Ann: Ready to serve on port " + str(serverPort) + "...\n")  
connectionSocket, addr = serverSocket.accept()   

while True:
    try:
        choice = input("Press 0 for Jan or 1 for Chan: ")
        choice = int(choice)
        # go to the path for chan
        if(choice):
            path = "8086 8087/"   
        # go to Jan path 
        else:
            path = "8081 8082 8083 8085/"
            
        print("path = ", path)
        
        var = input("Ann's message: ")
        #print("You entered " + str(var))
        message = str(var)
        data = path + message
            
        # Send data with message and path
        connectionSocket.send(data.encode())
        print("Ann:", message)
        print("Message sent.")
            
            # receive message from sender
        receivedData =  connectionSocket.recv(1024)
        path, message = getPathAndMessage(receivedData)
        time.sleep(1)   # wait 1 second the print message
        print("\nMessage received.")
        print("Jan:", message)
          
            

    except IOError:
        # Send response message for file not found
        connectionSocket.send(b"Error found")  
        # Close client socket
        connectionSocket.close()  

