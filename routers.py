#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 11:18:13 2018

@author: gracielaaguilar & Devony Powell 
"""
from threading import Thread
from socket import*          # used for socket configurations 
import sys                    # used to get arguments on command line
import time                   # used to find current time

Ann = 111
Chan = 1
Jan = 100
A = 8080
B = 8081
C = 8082
D = 8083
E = 8084
F = 8085
G = 8086
H = 8087
L = 8088
localHost = "127.0.0.1"
sockets = []
routers = []

##############################main starts here#################################
def router_thread(soc, port, max_buffer_size = 5120):
    soc.connect((localHost, port ))
    connection, address = soc.accept()
    ip, port = str(address[0]), str(address[1])
    print("Connected with :" + port)
    
# =============================================================================
#     is_active = True
# 
#     while is_active:
#         client_input = receive_input(connection, max_buffer_size)
# 
#         if "--QUIT--" in client_input:
#             print("Client is requesting to quit")
#             connection.close()
#             print("Connection " + ip + ":" + port + " closed")
#             is_active = False
#         else:
#             print("Processed result: {}".format(client_input))
#             connection.sendall("-".encode("utf8"))
# 
# 
# def receive_input(connection, max_buffer_size):
#     client_input = connection.recv(max_buffer_size)
#     client_input_size = sys.getsizeof(client_input)
# 
#     if client_input_size > max_buffer_size:
#         print("The input size is greater than expected {}".format(client_input_size))
# 
#     decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
#     result = process_input(decoded_input)
# 
#     return result
# 
# 
# def process_input(input_str):
#     print("Processing the input received from client")
# 
#     return "Hello " + str(input_str).upper()
# =============================================================================



if __name__ == '__main__':
    
    routerA = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
# =============================================================================
#     routerA.connect((localHost, A)) # connects the client and the server together
# =============================================================================
    #routerA.listen(1)       # queue up to 5 requests 
    print("Socket A on port:",  A, "now listening")
    sockets.append(routerA)
    routers.append(A)
    
    routerB = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
# =============================================================================
#     routerB.connect((A, B)) # connects the client and the server together
# =============================================================================
    #routerB.listen(1)       # queue up to 5 requests 
    print("Socket B on port:",  B,  "now listening")
    sockets.append(routerB)
    routers.append(B)
    
    routerC = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
# =============================================================================
#     routerC.connect((B, C)) # connects the client and the server together
# =============================================================================
    #routerC.listen(1)       # queue up to 5 requests 
    print("Socket C on port:",  C,  "now listening")
    sockets.append(routerC)
    routers.append(C)
    
    routerD = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
# =============================================================================
#     routerD.connect((localHost, D)) # connects the client and the server together
# =============================================================================
    #routerD.listen(1)       # queue up to 5 requests 
    print("Socket D on port:",  D, "now listening")
    sockets.append(routerD)
    routers.append(D)
    
    routerE = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
# =============================================================================
#     routerE.connect((localHost, E)) # connects the client and the server together
# =============================================================================
    #routerE.listen(1)       # queue up to 5 requests 
    print("Socket E on port:",  E,  "now listening")
    sockets.append(routerE)
    routers.append(E)
    
    routerF = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
# =============================================================================
#     routerF.connect((localHost, F)) # connects the client and the server together
# =============================================================================
    #routerF.listen(1)       # queue up to 5 requests 
    print("Socket F on port:",  F,  "now listening")
    sockets.append(routerF)
    routers.append(F)
    
    routerL = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
# =============================================================================
#     routerL.connect((localHost, L)) # connects the client and the server together
# =============================================================================
    #soc.listen(1)       # queue up to 5 requests 
    print("Socket L on port:",  L,  "now listening")
    sockets.append(routerL)
    routers.append(L)
    
    routerH = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
# =============================================================================
#     routerH.connect((localHost, H)) # connects the client and the server together
# =============================================================================
    #routerH.listen(1)       # queue up to 5 requests 
    print("Socket H on port:",  H,  "now listening")
    sockets.append(routerH)
    routers.append(H)
    
    routerG = socket(AF_INET, SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP socket
# =============================================================================
#     routerG.connect((localHost, G)) # connects the client and the server together
# =============================================================================
    #routerG.listen(1)       # queue up to 5 requests 
    print("Socket G on port:",  G,  "now listening")
    sockets.append(routerG)
    routers.append(G)
          
    


    # infinite loop- do not reset for every requests
    #while True:
    r = 0
    while r < len(sockets):
# =============================================================================
#             connection, address = sockets[r].accept()
#             ip, port = str(address[0]), str(address[1])
#             print("Connected with " + ip + ":" + port)
# =============================================================================

        try:
            Thread(target=router_thread, args=(sockets[r], routers[r])).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
        r+=1

        #sockets[r].close()

    