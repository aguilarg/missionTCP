# import modules
from socket import *   # used for socket configurations 
import sys             # used to get arguments on command line 
import time
import pickle


def getPathAndMessage(data):
    # extract path from data
    #data = data.decode()               # decode message because the data is coming as a bytes            
    data = data.split('/')
    path = data[0]
    message = data[1]
    
    return (path, message)


    
annToChan = [] 


annToJan = []

for i in range(9):
    annToJan.append("g")
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
serverSocket.listen(5)

print("Communication setup successfully.")
print ("Ann: Ready to serve on port " + str(serverPort) + "...\n")  
connectionSocket, addr = serverSocket.accept()   

janID = 100
chanID = 1
annID = 111
destination = [annID, janID, chanID]
source = [annID, janID, chanID]

DRP = 0
TER = 0
URG = 0
ACK = 0
RST = 0
SYN = 0
FIN = 0
check_num = 0
seq_num = 0
flags = [DRP, TER, URG, ACK, RST, SYN, FIN, check_num, seq_num]

while True:
    try:
        choice = input("Press 0 for Jan or 1 for Chan: ")
        print("")
        choice = int(choice)

        var = input("Ann's message: ")
        message = str(var)
        
        # go to the path for chan
        if(choice):
            path = "8086 8087/"   
            pathMessage = path + message
            sendDataList = [source[0], destination[2], pathMessage, flags]
        # go to Jan path 
        else:
            path = "8081 8082 8083 8085/"
            pathMessage = path + message
            destination[1] = janID
            sendDataList = [source[0], destination[1], pathMessage, flags]
        
        print("path = ", path)
        print("")
        
        print("DRP:",DRP)
        print("TER:",TER)
        print("URG:",URG)
        print("ACK:",ACK)
        print("RST:",RST)
        print("SYN:",SYN)
        print("FIN:",FIN)
        print("Check number:", check_num)
        print("Sequence number:", seq_num)
        print("")
                  
        #**************************************************
        # data to be sent
        sendData = pickle.dumps(sendDataList)      # convert rawData in string format and store into data
        connectionSocket.send(sendData)
        print("Data:", message)
        print("Message sent.")
        #**************************************************


        #**************************************************
        # receive message from sender
        receivedData =  connectionSocket.recv(1024) # recieve message from sender
        receivedDataList = pickle.loads(receivedData)  # convert data in list format: [destination[0], pathMessage, flags]
        path, message = getPathAndMessage(receivedDataList[2]) # sends data for processing
        time.sleep(1)
        print("\nMessage received.")
        print("Jan:", message)
        #*************************************************
        
    except IOError:
        # Send response message for file not found
        connectionSocket.send(b"Error found")  
        # Close client socket
        connectionSocket.close()  

