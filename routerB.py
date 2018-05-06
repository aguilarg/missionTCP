from socket import *    # used for socket configurations 
import sys              # used to get arguments on command line
import time             # used to find current time
import pickle
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

dijAlg (routers, 1)


port = 8081             # this router, F, gets connected to port 8083 as a client        
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
    receivedDataList[2], port = getNextData(path, message)       # get next path for which the message should go

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
    receivedDataList[2], port = getNextData(path, message)       # get next path for which the message should go
    receivedDataList = pickle.dumps(receivedDataList)
    clientSocket.send(receivedDataList)    

#clientSocket.close()  # close the socket since we are done using it
