from socket import *    # used for socket configurations 
import sys              # used to get arguments on command line
import time             # used to find current time


port = 8080          
serverName = "localhost"

clientSocket = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
clientSocket.connect((serverName, port)) # connects the client and the server together

# now that we have the client and the server connected, we can then send and receive messages
while 1:
    data = clientSocket.recv(1024) # recieve the bytes from the server
    print("Router A: Message received from Ann.")

    # extract path from data
    data = data.decode()               # decode message because the data is coming as a bytes            
    data = data.split('/')
    path = data[0]
    message = data[1]
    
    print("path = ", path)
    print("message = ", message)

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

    #prepare server socket
    serverSocket = socket(AF_INET,SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
    serverSocket.bind((serverName, port))  # bind the socket to the local address
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.listen(5)

    #establish connection
    connectionSocket, addr = serverSocket.accept()
    print("message sent on port", port, "from Router A")
    connectionSocket.send(data.encode())
    time.sleep(2)

#clientSocket.close()  # close the socket since we are done using it


