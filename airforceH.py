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

# connect to port with incomming messages 
port = 8088              # this router, F, gets connected to port 8084 as a client        
serverName = "localhost"

clientSocket = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
clientSocket.connect((serverName, port)) # connects the client and the server together
print("sucessfully connected. Ready to send message on port " + str(port) + "...")

airforceToJan = open("AirforceToJanLog.txt","w") 
while True:
    # receive message from sender
    message = clientSocket.recv(1024) 
    message = message.decode()
    
    print("\nMessage received.")
    print("Jan:", message)
    print("")

    if (message == "PEPPER THE PEPPER"):
        flags[2] = 1
        displayDataFlags(flags)
        flags[2] = 0          # URG set to zero
        message  = "mission successful"
    else:
        displayDataFlags(flags)

    # close connection if Jan sends that command
    if(message == "close"):
        clientSocket.close()
        print("Terminating...")
        time.sleep(1)
        sys.exit()
    
    # log communication
    airforceToJan = open("AirforceToJanLog.txt","a")
    print("Received: Writing to Airforce-Jan log file")
    airforceToJan.write("Jan: " + message + '\n')
    airforceToJan.close()
    
    if (message != "mission successful"):
        var = input("H's message: ")
        message = str(var)

    # Send data with message and path
    clientSocket.send(message.encode())
    print("airforceH:", message)
    print("Message sent.")

    airforceToJan = open("AirforceToJanLog.txt","a")
    print("Sent: Writing to Airforce-Jan log file")
    airforceToJan.write("AirforceH: " + message + '\n')
    airforceToJan.close()

#clientSocket.close()  # close the socket since we are done using it