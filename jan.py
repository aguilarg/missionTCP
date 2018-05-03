# import modules
from socket import *   # used for socket configurations 
import sys             # used to get arguments on command line 
import time


def webserver(connectionSocket):
    
    print("in function")
    while True:
        try:
            #data =  connectionSocket.recv(1024)   # recieve message that the client sent
            #data = data.decode()               # decode message because the data is coming as a bytes            
            #data = data.split('/')

            #path = data[0]
            #message = data[1]

            #print("path = ", path)
            #print("message = ", messag

            #path = path + "/"
            #data = path + message

            path = "8083 8082 8081/"
            message = "Hi, lets find the enemy!"
            data = path + message
            
            # Send the content of the requested file to the client
            connectionSocket.send(data.encode())
            print("Message sent from Jan.")
            time.sleep(2)
            #connectionSocket.close() # close client socket
            return 1
        except IOError:
            # Send response message for file not found
            connectionSocket.send(b"Error found")  
            # Close client socket
            connectionSocket.close()    
            return 0
    
annToChan = []
annToJan = []

fp = open('Ann-_Chan.txt') 
annToChan = fp.read().split("\n") 
fp.close() 
fp = open('Ann-_Jan.txt') 
annToJan = fp.read().split("\n") 
fp.close() 

# connect to port with incomming messages 
port = 8085             # this router, F, gets connected to port 8084 as a client        
serverName = "localhost"

clientSocket = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
clientSocket.connect((serverName, port)) # connects the client and the server together
print("sucessfully connected. Ready to send message on port " + str(port) + "...")


while 1:
    data = clientSocket.recv(1024) # recieve the bytes from the server
    print("Jan: Message received from Router F.")

    # extract path from data
    data = data.decode()               # decode message because the data is coming as a bytes            
    data = data.split('/')
    path = data[0]
    message = data[1]
    
    print("path = ", path)
    print("message = ", message)

    path = "8085 8083 8082 8081/"
    message = "Got your message buddy!"
    data = path + message

    # Send the content of the requested file to the client
    clientSocket.send(data.encode())
    print("Message sent from Jan.")
    time.sleep(2)
#clientSocket.close()  # close the socket since we are done using it