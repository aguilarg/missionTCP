# =============================================================================
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Mon Apr 30 16:27:30 2018
# 
# @author: gracielaaguilar
# """
# 
# # import modules
# from socket import *   # used for socket configurations 
# import sys             # used to get arguments on command line 
# import time
# 
# 
# def webserver(connectionSocket):
#     while True:
#         try:
#             #data =  connectionSocket.recv(1024)   # recieve message that the client sent
#             #data = data.decode()               # decode message because the data is coming as a bytes            
#             #data = data.split('/')
# 
#             #path = data[0]
#             #message = data[1]
# 
#             #print("path = ", path)
#             #print("message = ", message)
# 
#             #path = path + "/"
#             #data = path + message
# 
#             path = "8083 8082 8081/"
#             message = "Hi, i got your message!"
#             data = path + message
#             
#             # Send the content of the requested file to the client
#             connectionSocket.send(data.encode())
#             print("Message sent from Jan.")
#             time.sleep(2)
#             #connectionSocket.close() # close client socket
#             return 1
#         except IOError:
#             # Send response message for file not found
#             connectionSocket.send(b"Error found")  
#             # Close client socket
#             connectionSocket.close()    
#             return 0
#         
#     
# janToAnn = []
# janToChan = []
# 
# fp = open('Jan-_Ann.txt') 
# janToAnn = fp.read().split("\n") 
# fp.close() 
# fp = open('Jan-_Chan.txt') 
# janToChan = fp.read().split("\n") 
# fp.close() 
# 
# 
# 
# # Prepare a sever socket
# serverPort = 8084
# serverName = "localhost"
# serverSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
# 
# serverSocket.bind((serverName, serverPort))  # bind the socket to the local address
# serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# # specify the number of unaccepted connections that the system will allow before refusing new connections
# serverSocket.listen(5)
# 
# while 1:
#     # Establish the connection
#     print ("Jan: Ready to serve on port " + str(serverPort) + "...")
#     connectionSocket, addr = serverSocket.accept()
#     print("")
#     #serverSocket.settimeout(120) # system will timeout after 120 seconds
#     webserver(connectionSocket)
# serverSocket.close() # close server socket
# =============================================================================
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 12:19:14 2018

@author: gracielaaguilar
"""

from socket import *    # used for socket configurations 
import sys              # used to get arguments on command line
import time             # used to find current time


port = 8084        
serverName = "localhost"

clientBsocket = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
clientBsocket.connect((serverName, port)) # connects the client and the server together

# now that we have the client and the server connected, we can then send and receive messages

while 1:
    data = clientBsocket.recv(1024) # recieve the bytes from the server
    print("jan : Message received from Router F.")

    # extract path from data
    data = data.decode()               # decode message because the data is coming as a bytes
    data = "8083 8082 8081 8080/"            
    data = data.split('/')
    path = data[0]
    message = data[1]
    
    print("path = ", path)
    print("message = ", message)

    nextPath = path.split()
    port = int(nextPath[0])

    # fix path; pop from list
    newPath = ""
    i = 1
    while i < len(nextPath):
        newPath = newPath + " " + nextPath[i]
        i += 1

    path = newPath + "/"
    data = path + message

    #prepare server socket
    serverSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
    serverSocket.bind((serverName, port))  # bind the socket to the local address
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.listen(5)

    #establish connection
    connectionSocket, addr = serverSocket.accept()
    print("message sent on port", port, "from Router L")
    connectionSocket.send(data.encode())
    time.sleep(2)


