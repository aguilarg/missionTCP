#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 12:19:14 2018

@author: gracielaaguilar
"""

from socket import *    # used for socket configurations 
import sys              # used to get arguments on command line
import time             # used to find current time
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

dijAlg (routers, 5)



port = 8083             # this router, F, gets connected to port 8083 as a client        
serverName = "localhost"

clientBsocket = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
clientBsocket.connect((serverName, port)) # connects the client and the server together


def getPathAndMessage(data):
    # extract path from data
    data = data.decode()               # decode message because the data is coming as a bytes            
    data = data.split('/')
    path = data[0]
    message = data[1]
    
    return (path, message)

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

# now that we have the client and the server connected, we can then send and receive messages

while 1:
    data = clientBsocket.recv(1024) # recieve the bytes from the server
    print("Router L: Message received from Router L.")

    path, message = getPathAndMessage(data)
    print("path = ", path)
    print("message = ", message)

    data, port = getNextData(path, message)       # get next path for which the message should go

    #prepare server socket
    serverSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
    serverSocket.bind((serverName, port))  # bind the socket to the local address
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.listen(5)
    connectionSocket, addr = serverSocket.accept()

    # send data to next client/server
    print("message sent on port", port, "from Router F")
    connectionSocket.send(data.encode())
    time.sleep(2)

    # recieve data and send it to next port
    data = connectionSocket.recv(1024)      # new incoming message
    path, message = getPathAndMessage(data) # send data for processing to get path and message
    print("path = ", path)
    print("message = ", message)  

    data, nextPort = getNextData(path, message)       # get next path for which the message should go
    print("message sent on port", port, "from Router F")
    connectionSocket.send(data.encode())
    time.sleep(2)
    

#clientSocket.close()  # close the socket since we are done using it
