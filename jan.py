# import modules
from socket import *   # used for socket configurations 
import sys             # used to get arguments on command line 
import time
import pickle
    
janToAnn = []
janToChan = []

fp = open('Jan-_Ann.txt') 
janToAnn = fp.read().split("\n") 
fp.close() 
fp = open('Jan-_Chan.txt') 
janToChan = fp.read().split("\n") 
fp.close() 

# connect to port with incomming messages 
port = 8085             # this router, F, gets connected to port 8084 as a client        
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

def displayDataFlags(flags):
    print("DRP = ", flags[0])
    print("TER = ", flags[1])
    print("URG = ", flags[2])
    print("ACK = ", flags[3])
    print("RST = ", flags[4])
    print("SYN = ", flags[5])
    print("FIN = ", flags[6])
    print("Checksum:", flags[7])
    print("Sequence number:", flags[8])
    
    
janID = 100
annID = 111
chanID = 1
destination = [annID, chanID]

DRP = 0
TER = 0
URG = 0
ACK = 0
RST = 0
SYN = 0
FIN = 0
check_sum = 0
flags = [DRP, TER, URG, ACK, RST, SYN, FIN, check_sum]

connectedFlag = False       # use to check is server is already in use
done = False
first_time = True
firstHandshake = False

janToAnnLog = open("JanToAnnLog.txt","w") 
janToChanLog = open("JanToChanLog.txt","w")
janToAirforceH = open("JanToAirforceLog.txt","w") 

while True:
    #**************************************************
    receivedData = clientSocket.recv(1024) # recieve message from sender
    receivedDataList = pickle.loads(receivedData)  # convert data in list format: [destination[0], pathMessage, flags]
    path, message = getPathAndMessage(receivedDataList[2]) # sends data for processing
    time.sleep(1)
    print ("Destination: ", receivedDataList[0])
    print("\nMessage received.")
    print("Ann:", message)
    print("")
    
    # saving the communication log for Ann and Jan
    if (receivedDataList[0] == annID):
        receivedDataList[0] = janID   # set source for packets
        receivedDataList[1] = annID   # set destination for packets
        janToAnnLog = open("JanToAnnLog.txt","a")
        print("Received: Writing to Jan-Ann log file")
        janToAnnLog.write("Ann: " + message + '\n')
        janToAnnLog.close()

    if(receivedDataList[0] == chanID):
        receivedDataList[0] = janID   # set source for packets
        receivedDataList[1] = chanID
        janToChanLog = open("JanToChanLog.txt","a")
        print("Received: Writing to Jan-Chan log file")
        janToChanLog.write("Chan: " + message + '\n')
        janToChanLog.close()

    DataFlags = receivedDataList[3]
    displayDataFlags(DataFlags)
                  
    #*************************************************
    
    if(message == "Execute"):
        time.sleep(1)
        print("Notifying airforce base to execute mission...")
        # connect to airforceH
        if (connectedFlag != True):
            #prepare server socket
            serverSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
            serverSocket.bind((serverName, 8088))  # bind the socket to the local address
            serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            serverSocket.listen(5)
            connectionSocket, addr = serverSocket.accept()
            connectedFlag = True

        while(connectedFlag):
            if(first_time):
                # send data to next client/server
                #message = message.decode()
                connectionSocket.send(message.encode())
                print("Jan:", message)
                print("Message sent.")

                # log communication
                janToAirforceH = open("JanToAirforceLog.txt","a")
                print("Sent: Writing to Jan-Airforce log file")
                janToAirforceH.write("Jan: " + message + '\n')
                janToAirforceH.close()

                first_time = False

            message = connectionSocket.recv(1024)      # new incoming message (server end)
            message = message.decode()
            time.sleep(1)
            print("\nMessage received.")
            print("AirforceH:", message)
            print("")

            if (message == "mission successful"):
                close = "close"
                connectionSocket.send(close.encode())
                #message = "CONGRATULATIONS WE FRIED DRY GREEN LEAVES"
                done = True
                
                # log communication
                janToAirforceH = open("JanToAirforceLog.txt","a")
                print("Received: Writing to Jan-Airforce log file")
                janToAirforceH.write("AirforceH: " + message + '\n')
                janToAirforceH.close()
                break

            # log communication
            janToAirforceH = open("JanToAirforceLog.txt","a")
            print("Received: Writing to Jan-Airforce log file")
            janToAirforceH.write("AirforceH: " + message + '\n')
            janToAirforceH.close()

            var = input("Jan's message: ")
            message = str(var)
            #message = message.decode()
            
            # log communication
            janToAirforceH = open("JanToAirforceLog.txt","a")
            print("Sent: Writing to Jan-Airforce log file")
            janToAirforceH.write("Jan: " + message + '\n')
            janToAirforceH.close()

            connectionSocket.send(message.encode())
            print("Jan:", message)
            print("Message sent.")
            # recieve data and send it to next port
            

    path = "8083 8082 8081 8080/"

    if(done != True and firstHandshake):
        var = input("Jan's message: ")
        message = str(var)
    elif (firstHandshake != True):
        message = "No data"
        firstHandshake = True
    else:
        # mission has been completed
        message = "CONGRATULATIONS WE FRIED DRY GREEN LEAVES"
        done = False

    receivedDataList[2] = path + message

    if (receivedDataList[1] == annID):
        print("Sent: Writing to Jan-Ann log file")
        janToAnnLog = open("JanToAnnLog.txt","a") 
        janToAnnLog.write("Jan: " + message + "\n")
        janToAnnLog.close()
    
    if (receivedDataList[1] == chanID):
        janToChanLog = open("JanToChanLog.txt","a")
        print("Sent: Writing to Jan-Chan log file")
        janToChanLog.write("Jan: " + message + '\n')
        janToChanLog.close()
    
    # Send data with message and path
    receivedDataList = pickle.dumps(receivedDataList)   # convert data to string
    clientSocket.send(receivedDataList)
    print("Jan:", message)
    print("Message sent.")

#clientSocket.close()  # close the socket since we are done using it