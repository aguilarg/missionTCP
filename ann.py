# import modules
from socket import *   # used for socket configurations 
import sys             # used to get arguments on command line 
import time
import pickle

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
    
def getPathAndMessage(data):           
    data = data.split('/')
    path = data[0]
    message = data[1]
    
    return (path, message)

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
firstChan = True
firstJan = True 
firstChanVisited = False
firstJanVisited = False
TermChan = 5

annToChanLog = open("AnnToChanLog.txt","w") 
annToJanLog = open("AnnToJanLog.txt","w") 

pendingExit = False
chanClose = True
while True:
    try:
        if(TermChan == 1 and pendingExit == False):
            flags[2] = 1
            print("Notifying Jan something is fishy..." )
            time.sleep(2)
            choice = 0
            pendingExit = True
            chanClose = False    

        elif(TermChan == 1 and pendingExit == True):
            flags[2] = 0      #URG
            flags[4] = 1      #RST - Download communication
            flags[1] = 1      #TER - Terminate client (Chan)
            choice = 1
            chanClose = False

        elif(TermChan == 0):
            print("Downloading Chan transcript and terminating connection...")
            time.sleep(3)
            print("Download and termination complete\n")
            time.sleep(1)
            TermChan = -1
            flags[4] = 0      #RST - reset
            flags[1] = 0      #TER - reset
            flags[2] = 0      #SYN - reset
            chanClose = True
        
        if(chanClose):
            # error check
            while True:
                choice = input("Press 0 for Jan or 1 for Chan: ")
                try:
                    choice = int(choice) 
                except ValueError:
                    print(end = "")
                if (choice == 1):
                    choice = 1
                    break
                elif (choice == 0):
                    choice = 0
                    break
                elif(choice != 1 or choice != 0):
                    print("Sorry,", choice, "is not accepted. Try again.\n")
        print("")
        if(choice):
            if(firstChan):
                print("Establishing 3 handshake...")
                firstChanVisited = True
                flags[5] = 1
                message = "No data"
            else:
                if(TermChan != 0 and TermChan != 1):
                    var = input("Ann's message: ")
                    message = str(var)
                    flags[5] = 0
            
            # send Chan last message
            if(pendingExit == True):
                message = "You've been compromise. I have to close your connection"
                pendingExit = False
                
            path = "8086 8087/"   
            pathMessage = path + message
            flags[8] = len(message)
            sendDataList = [source[0], destination[2], pathMessage, flags]
        # go to Jan path 
        else:
            if(firstJan):
                print("Establishing 3 handshake...")
                firstJanVisited = True
                flags[5] = 1
                message = "No Data"
            else:
                if(chanClose):
                    var = input("Ann's message: ")
                    message = str(var)
                    flags[5] = 0
            path = "8081 8082 8083 8085/"
            flags[8] = len(message)

            # notify Jan with message
            if(TermChan == 1):
                message = "Chan has been compromise!"
            """
            if(TermChan == 0):
                TermChan = -1
                flags[4] = 0      #RST - reset
                flags[1] = 0      #TER - reset
                flags[2] = 0      #SYN - reset
            """
            pathMessage = path + message
            destination[1] = janID
            sendDataList = [source[0], destination[1], pathMessage, flags]
        print("")

        #**************************************************
        # data to be sent
        sendData = pickle.dumps(sendDataList)      # convert rawData in string format and store into data
        connectionSocket.send(sendData)
        print("Data:", message)
        print("Message sent.")
        if (sendDataList[1] == chanID):
            print("Sent: Writing to chan file")
            annToChanLog = open("AnnToChanLog.txt","a") 
            annToChanLog.write("Ann: " + message + "\n")
            annToChanLog.close()

        if(sendDataList[1] == janID):
            print("Sent: Writing to Jan file")
            annToJanLog = open("AnnToJanLog.txt","a")
            annToJanLog.write("Ann: " + message + '\n')
            annToJanLog.close()
        #**************************************************
        # receive message from sender
        receivedData =  connectionSocket.recv(1024) # recieve message from sender
        receivedDataList = pickle.loads(receivedData)  # convert data in list format: [destination[0], pathMessage, flags]
        seq_num1 = receivedDataList[3]
        flags[8] += seq_num1[8]
        path, message = getPathAndMessage(receivedDataList[2]) # sends data for processing
        time.sleep(1)
        print("\nMessage received.")
        if (receivedDataList[0] == chanID):
            annToChanLog = open("AnnToChanLog.txt","a")
            print("Received: Writing to Chan file")
            annToChanLog.write("Chan: " + message + '\n')
            annToChanLog.close()
        
        if(receivedDataList[0] == janID):
            print("Received: Writing to Jan file")
            annToJanLog = open("AnnToJanLog.txt","a")
            annToJanLog.write("Jan:" + message + '\n')
            annToJanLog.close()

        if(firstChanVisited):
            firstChan = False
            firstChanVisited = False
            displayDataFlags(flags)
            print("Handshake has been completed with Chan...\n")

        elif(receivedDataList[0] == chanID):
            print("Chan:", message)
            TermChan -=1
            displayDataFlags(flags)
            flags[2] = seq_num1[2]

        if (firstJanVisited):
            firstJan = False
            displayDataFlags(flags)
            flags[8] = 328
            firstJanVisited = False
            print("Handshake has been completed with Jan...\n")
        
        if (firstJanVisited != True and receivedDataList[0] == janID):
            print("Jan:", message)
            displayDataFlags(flags)

    except IOError:
        # Send response message for file not found
        connectionSocket.send(b"Error found")  
        # Close client socket
        connectionSocket.close()  
