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

AnnVisited = True
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

# This program is licensed under the GPL; see LICENSE for details.

# This procedure can be used to calculate the Internet checksum of
# some data.  It is adapted from RFC 1071:
#
# ftp://ftp.isi.edu/in-notes/rfc1071.txt
#
# See also:
#
# http://www.netfor2.com/ipsum.htm
# http://www.netfor2.com/checksum.html

def ichecksum(data, sum=0):
    """ Compute the Internet Checksum of the supplied data.  The checksum is
    initialized to zero.  Place the return value in the checksum field of a
    packet.  When the packet is received, check the checksum, by passing
    in the checksum field of the packet and the data.  If the result is zero,
    then the checksum has not detected an error.
    """
    # make 16 bit words out of every two adjacent 8 bit words in the packet
    # and add them up
    for i in range(0,len(data),2):
        if i + 1 >= len(data):
            sum += ord(data[i]) & 0xFF
        else:
            w = ((ord(data[i]) << 8) & 0xFF00) + (ord(data[i+1]) & 0xFF)
            sum += w

    # take only 16 bits out of the 32 bit sum and add up the carries
    while (sum >> 16) > 0:
        sum = (sum & 0xFFFF) + (sum >> 16)

    # one's complement the result
    sum = ~sum

    return sum & 0xFFFF

chanToAnnLog = open("ChanToAnnLog.txt","w") 
chanToJanLog = open("ChanToJanLog.txt","w") 
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
    # saving the communication log for Ann and Jan
    if (receivedDataList[0] == annID):
        chanToAnnLog = open("ChanToAnnLog.txt","a")
        print("Received: Writing to Chan-Ann log file")
        chanToAnnLog.write("Ann: " + message + '\n')
        chanToAnnLog.close()
    if(receivedDataList[0] == janID):
        chanToJanLog = open("ChanToJanLog.txt","a")
        print("Received: Writing to Chan-Jan log file")
        chanToJanLog.write("Jan: " + message + '\n')
        chanToJanLog.close()
    
    DataFlags = receivedDataList[3]
    
    #displayDataFlags(receivedDataList[2])
    #*************************************************

    print("")
    
    print("DRP:",DataFlags[0])
    print("TER:",DataFlags[1])
    print("URG:",DataFlags[2])
    print("ACK:",DataFlags[3])
    print("RST:",DataFlags[4])
    print("SYN:",DataFlags[5])
    print("FIN:",DataFlags[6])
    print("Checksum:", DataFlags[7])
    print("Sequence number:", DataFlags[8])
                  

    # Ann is the source
    if (receivedDataList[0] == annID):
        receivedDataList[1] = annID
        path = "8086 8081 8080/"
    else:
        receivedDataList[1] = janID
        path = "8086 8089 9090 8083 8085/"
    receivedDataList[0] = chanID   # set source agentID

    if(AnnVisited):
        message = "No data"
        AnnVisited = False
    else:
        var = input("Chan's message: ")
        message = str(var)
    
    receivedDataList[2] = path + message
    receivedDataList[3][7] = ichecksum(message)
    # Send data with message and path
    print("\nChan Source ",  receivedDataList[0])
    print("Chan Destination ",  receivedDataList[1])
    
    if (receivedDataList[1] == annID):
        print("Sent: Writing to Chan-Ann log file")
        chanToAnnLog = open("ChanToAnnLog.txt","a") 
        chanToAnnLog.write("Chan: " + message + "\n")
        chanToAnnLog.close()
    
    if (receivedDataList[1] == janID):
        chanToJanLog = open("ChanToJanLog.txt","a")
        print("Sent: Writing to Chan-Jan log file")
        chanToJanLog.write("Chan: " + message + '\n')
        chanToJanLog.close()

    receivedDataList = pickle.dumps(receivedDataList)      # convert rawData in string format and store into data
    clientSocket.send(receivedDataList)
    
    if (DataFlags[1] == 1):
        print("Terminating...")
        clientSocket.close()
        sys.exit()

    print("")
    print("Data:", message)
    print("Message sent.")




#clientSocket.close()  # close the socket since we are done using it