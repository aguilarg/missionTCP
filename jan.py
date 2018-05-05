# import modules
from socket import *   # used for socket configurations 
import sys             # used to get arguments on command line 
import time
    
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
    data = data.decode()               # decode message because the data is coming as a bytes            
    data = data.split('/')
    path = data[0]
    message = data[1]
    
    return (path, message)

connectedFlag = False       # use to check is server is already in use
done = False
first_time = True
while True:
    # receive message from sender
    data = clientSocket.recv(1024) 
    path, message = getPathAndMessage(data)
    time.sleep(1)   # wait 1 second the print message
    print("\nMessage received.")
    print("Ann:", message)
    print("")
    
    
    if(message == "execute"):
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
            if (message == "mission successful"):
                close = "close"
                
                connectionSocket.send(close.encode())
                message = "mission has been accomplished!!!!"
                done = True
                break

            if(first_time):
                # send data to next client/server
                print("message sent on port", port, "from Jan")
                #message = message.decode()
                connectionSocket.send(message.encode())
                print("Jan:", message)
                print("Message sent.")
                first_time = False

            message = connectionSocket.recv(1024)      # new incoming message (server end)
            message = message.decode()
            print("\nMessage received.")
            print("AirforceH:", message)
            print("")

            var = input("Jan's message: ")
            message = str(var)
            #message = message.decode()
            connectionSocket.send(message.encode())
            print("Jan:", message)
            print("Message sent.")


            # recieve data and send it to next port
            

    path = "8083 8082 8081 8080/"

    if(done != True):
        var = input("Jan's message: ")
        message = str(var)
     

    data = path + message
    # Send data with message and path
    clientSocket.send(data.encode())
    print("Jan:", message)
    print("Message sent.")
    time.sleep(1)

#clientSocket.close()  # close the socket since we are done using it