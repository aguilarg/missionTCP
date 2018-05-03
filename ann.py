# import modules
from socket import *   # used for socket configurations 
import sys             # used to get arguments on command line 
import time


def webserver(connectionSocket):
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

            path = "8081 8082 8083/"
            message = "Hi, lets find the enemy!"
            data = path + message
            
            # Send the content of the requested file to the client
            connectionSocket.send(data.encode())
            print("Message sent from Ann.")
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



# Prepare a sever socket
serverPort = 8080
serverName = "localhost"
serverSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket

serverSocket.bind((serverName, serverPort))  # bind the socket to the local address
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# specify the number of unaccepted connections that the system will allow before refusing new connections
serverSocket.listen(5)

while 1:
    # Establish the connection
    print ("Ann: Ready to serve on port " + str(serverPort) + "...")
    connectionSocket, addr = serverSocket.accept()
    print("")
    #serverSocket.settimeout(120) # system will timeout after 120 seconds
    webserver(connectionSocket)
serverSocket.close() # close server socket

