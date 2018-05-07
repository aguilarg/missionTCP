#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  4 13:40:09 2018

@author: gracielaaguilar
"""

# import modules
from socket import *   # used for socket configurations 
import sys             # used to get arguments on command line 
import time
import pickle

janToAnn = []
janToChan = []

fp = open('Chan-_Ann.txt') 
chanToAnn = fp.read().split("\n") 
fp.close() 
fp = open('Chan-_Jan.txt') 
chanToJan = fp.read().split("\n") 
fp.close() 

port = 8087             # this router, F, gets connected to port 8084 as a client        
serverName = "localhost"

clientSocket = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
clientSocket.connect((serverName, port)) # connects the client and the server together
print("sucessfully connected. Ready to send message on port " + str(port) + "...")

def getPathAndMessage(data):
    # extract path from data
    #data = data.decode()               # decode message because the data is coming as a bytes            
    data = data.split('/')
    path = data[0]
    message = data[1]
    
    return (path, message)

annID = 111
janID = 100
chanID = 1

while True:
    # receive message from sender
    #**************************************************
    receivedData = clientSocket.recv(1024) # recieve message from sender
    receivedDataList = pickle.loads(receivedData)  # convert data in list format: [destination[0], pathMessage, flags]
    path, message = getPathAndMessage(receivedDataList[2]) # sends data for processing
    time.sleep(1)
    print("\nMessage received.")
    print("Ann:", message)
    print("")
    #displayDataFlags(receivedDataList[2])
    #*************************************************
    DataFlags = receivedDataList[3]
    
    print("")
    
    print("DRP:",DataFlags[0])
    print("TER:",DataFlags[1])
    print("URG:",DataFlags[2])
    print("ACK:",DataFlags[3])
    print("RST:",DataFlags[4])
    print("SYN:",DataFlags[5])
    print("FIN:",DataFlags[6])
    print("Check number:", DataFlags[7])
                  
    
    

    # Ann is the source
    if (receivedDataList[0] == annID):
        receivedDataList[1] = annID
        print("in if s tatement", receivedDataList[1])
 
        path = "8086 8081 8080/"
    else:
        receivedDataList[1] = janID
        path = "8086 8089 9090 8083 8085/"
    print("CHAN is DES")
    receivedDataList[0] = chanID   # set source agentID
    print(receivedDataList[0])

    var = input("Chan's message: ")
    message = str(var)

    receivedDataList[2] = path + message
    # Send data with message and path
    receivedDataList = pickle.dumps(receivedDataList)      # convert rawData in string format and store into data
    clientSocket.send(receivedDataList)
    print("")
    print("Data:", message)
    print("Message sent.")

#clientSocket.close()  # close the socket since we are done using it