#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:03:33 2018

@author: gracielaaguilar
"""

from socket import *    # used for socket configurations 
import sys              # used to get arguments on command line
import time             # used to find current time
import networkx as nx
import numpy as np
import pickle

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

dijAlg (routers, 4)

"""
port = 8086             # this router, F, gets connected to port 8083 as a client        
serverName = "localhost"

clientSocket = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
clientSocket.connect((serverName, port)) # connects the client and the server together


def getPathAndMessage(data):
    # extract path from data
    #data = data.decode()               # decode message because the data is coming as a bytes            
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

# send and receive data
connectedFlag = False       # use to check is server is already in use
while 1:
    #**************************************************
    receivedData = clientSocket.recv(1024) # recieve message from sender
    
    receivedDataList = pickle.loads(receivedData)  # convert data in list format: [destination[0], pathMessage, flags]
    path, message = getPathAndMessage(receivedDataList[2]) # sends data for processing
    time.sleep(1)
    print ("Source: ", receivedDataList[0])
    print ("Destination: ", receivedDataList[1])
    print("path = ", path)
    print("message = ", message)
    #displayDataFlags(receivedDataList[2])
    #*************************************************

    data, port = getNextData(path, message)       # get next path for which the message should go

    if (connectedFlag != True):
        #prepare server socket
        serverSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
        serverSocket.bind((serverName, port))  # bind the socket to the local address
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSocket.listen(5)
        connectionSocket, addr = serverSocket.accept()
        connectedFlag = True

    # send data to next client/server
    receivedDataList = pickle.dumps(receivedDataList)
    connectionSocket.send(receivedDataList)

    # recieve data and send it to next port
    #**************************************************
    receivedData = connectionSocket.recv(1024) # recieve message from sender
    receivedDataList = pickle.loads(receivedData)  # convert data in list format: [destination[0], pathMessage, flags]
    path, message = getPathAndMessage(receivedDataList[2]) # sends data for processing
    time.sleep(1)
    print ("Source: ", receivedDataList[0])
    print ("Destination: ", receivedDataList[1])
    print("path = ", path)
    print("message = ", message)
    #displayDataFlags(receivedDataList[2])
    #*************************************************  

    # since we got the data using the server, we send it using the client
    receivedDataList[1], port = getNextData(path, message)       # get next path for which the message should go
    receivedDataList = pickle.dumps(receivedDataList)
    clientSocket.send(receivedDataList) 
    

#clientSocket.close()  # close the socket since we are done using it
"""


#**************************************************************************   A's code below

port = 8086                      
serverName = "localhost"
clientSocket = socket(AF_INET, SOCK_STREAM)     # AF_INET = IPv4, SOCK_STREAM = TCP socket
clientSocket.connect((serverName, port))        # connects the client and the server together

# extract path from data
def getPathAndMessage(data):
    #data = data.decode()               # decode message because the data is coming as a bytes            
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
def sendRecv(connectionSocket, dataList, port):
    # send data to next client/server
    sendData = pickle.dumps(dataList)      # convert rawData in string format and store into data
    connectionSocket.send(sendData)

    # recieve data and send it to next port
    #**************************************************
    dataList = connectionSocket.recv(1024) # recieve message from sender
    dataList = pickle.loads(dataList)  # convert data in list format: [destination[0], pathMessage, flags]
    path, message = getPathAndMessage(dataList[2]) # sends data for processing
    time.sleep(1)
    print ("Source: ", receivedDataList[0])
    print ("Destination: ", receivedDataList[1])
    print("path = ", path)
    print("message = ", message)
    #displayDataFlags(dataList[2])
    #************************************************* 

    # since we got the data using the server, we send it using the client
    dataList[2], port = getNextData(path, message)       # get next path for which the message should go
    dataList = pickle.dumps(dataList) 
    clientSocket.send(dataList)

# send and receive data
connectedFlagA = False       # use to check is server is already in use
connectedFlagG = False       # use to check is server is already in use
connectedFlagChan = False

annID = 111
janID = 100

while 1:
    #**************************************************
    receivedData = clientSocket.recv(1024) # recieve message from sender
    receivedDataList = pickle.loads(receivedData)  # convert data in list format: [destination[0], pathMessage, flags]
    path, message = getPathAndMessage(receivedDataList[2]) # sends data for processing
    time.sleep(1)
    print ("Source: ", receivedDataList[0])
    print ("Destination: ", receivedDataList[1])
    print("path = ", path)
    print("message = ", message)
    #displayDataFlags(receivedDataList[2])
    #*************************************************
    
    data, port = getNextData(path, message)       # get next path for which the message should go

    # go to chan
    if (connectedFlagChan != True):
        #prepare server socket
        serverSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
        serverSocket.bind((serverName, port))  # bind the socket to the local address
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSocket.listen(5)
        chanConnectionSocket, addr = serverSocket.accept()
        connectedFlagChan = True

    if (connectedFlagG != True and port == 8089):
        #prepare server socket
        gServerSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
        gServerSocket.bind((serverName, port))  # bind the socket to the local address
        gServerSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        gServerSocket.listen(5)
        gConnectionSocket, addr = gServerSocket.accept()
        connectedFlagG = True

    if (connectedFlagA != True and port == 8081):
        #prepare server socket
        aServerSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
        aServerSocket.bind((serverName, port))  # bind the socket to the local address
        aServerSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        aServerSocket.listen(5)
        aConnectionSocket, addr = aServerSocket.accept()
        connectedFlagA = True

    # send message to Jan
    if(port == 8086 and receivedDataList[1] == janID):
        sendRecv(gConnectionSocket, data, port)

    # send data to Ann
    if(port == 8086 and receivedDataList[1] == annID):
        sendRecv(aConnectionSocket, receivedDataList, port) 
    
    # send data to Chan
    if(port == 8087):
        sendRecv(chanConnectionSocket, receivedDataList, port) 