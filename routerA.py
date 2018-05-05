from socket import *   # used for socket configurations 
import sys              # used to get arguments on command line
import time             # used to find current time

import numpy as np
import networkx as nx
import numpy as np

graph = np.array([[0,4,3,0,7,0,0,0],[4,0,6,0,0,0,0,5], [3,6,0,11,0,0,0,0],
          [0,0,11,0,0,6,10,9], [7,0,0,0,0,0,5,0], [0,0,0,6,0,0,0,5],
          [0,0,0,10,5,0,0,0],[0,5,0,9,0,5,0,0]])


G = nx.from_numpy_matrix(graph, create_using=nx.DiGraph())
def dijAlg(route, node):
    
    print("for Router",route[node], ":")
    
    
    print("Destination      Distance       Shortest Path")
    for i in range(8):
        
        result = []
        path = nx.dijkstra_path(G, node, i)
        ix =[[path[i],path[i+1]] for i in range(len(path)-1)]
        total = sum([graph[i[0]][i[1]] for i in ix])
        for j in range (0, len(path)):
            num = path[j]
            
            #print(counter)
            result.append(route[num])    
        print(route[i],"               ", total, "             ", result)
        total = 0
       
routers = ['A','B','C','D','E','F','G','L']

dijAlg (routers, 0)

port = 8080                      
serverName = "localhost"
clientSocket = socket(AF_INET, SOCK_STREAM)     # AF_INET = IPv4, SOCK_STREAM = TCP socket
clientSocket.connect((serverName, port))        # connects the client and the server together

# extract path from data
def getPathAndMessage(data):
    data = data.decode()               # decode message because the data is coming as a bytes            
    data = data.split('/')
    path = data[0]
    message = data[1]
    return (path, message)

# find the next path to send message
def getNextData(path, message):
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

    return data, port

# sends and receive data
def sendRecv(connectionSocket, data, port):
    # send data to next client/server
    print("message sent on port", port, "from Router A")
    connectionSocket.send(data.encode())
    time.sleep(2)

    # recieve data and send it to next port
    data = connectionSocket.recv(1024)      # new incoming message (server end)
    path, message = getPathAndMessage(data) # send data for processing to get path and message
    print("path = ", path)
    print("message = ", message)  

    # since we got the data using the server, we send it using the client
    data, port = getNextData(path, message)       # get next path for which the message should go
    print("message sent on port", port, "from Router A") 
    clientSocket.send(data.encode())
    time.sleep(2)

# send and receive data
connectedFlagAnn = False       # use to check is server is already in use
connectedFlagJan = False       # use to check is server is already in use
while 1:
    data = clientSocket.recv(1024)      # recieve message from sender
    print("Router A: Message received from Ann.")

    path, message = getPathAndMessage(data)
    print("path = ", path)
    print("message = ", message)

    data, port = getNextData(path, message)       # get next path for which the message should go


    if (connectedFlagJan != True and port == 8081):
        #prepare server socket
        print("In Jan connection")
        janServerSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
        janServerSocket.bind((serverName, port))  # bind the socket to the local address
        janServerSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        janServerSocket.listen(5)
        janConnectionSocket, addr = janServerSocket.accept()
        connectedFlagJan = True

    if (connectedFlagAnn != True and port == 8086):
        #prepare server socket
        #print("In Jan connection")
        chanServerSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
        chanServerSocket.bind((serverName, port))  # bind the socket to the local address
        chanServerSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        chanServerSocket.listen(5)
        chanConnectionSocket, addr = chanServerSocket.accept()
        connectedFlagAnn = True

    # send message to Jan
    if(port == 8081):
        sendRecv(janConnectionSocket, data, port)

    # send message to Chan
    if(port == 8086):
        sendRecv(chanConnectionSocket, data, port) 
