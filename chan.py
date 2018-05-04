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
    data = data.decode()               # decode message because the data is coming as a bytes            
    data = data.split('/')
    path = data[0]
    message = data[1]
    
    return (path, message)


while True:
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

    path = "8086 8081 8080/"
    var = input("Chan's message: ")
        #print("You entered " + str(var))
    message = str(var)
    data = path + message
    # Send data with message and path
    clientSocket.send(data.encode())
    print("Jan:", message)
    print("Message sent.")
    time.sleep(1)

#clientSocket.close()  # close the socket since we are done using it