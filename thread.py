#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 13:27:17 2018

@author: gracielaaguilar
"""
import _thread
import pickle
import socket
import time

localhost = "127.0.0.1"

def main():
    """Run a server in a thread and start a client to talk to it."""
    _thread.start_new_thread(run_server, (localhost, 111))
    print("server is ann on port", 111, ":")
    run_client(localhost, 8080)


def run_server(host, port):
    """Handle all incoming connections by spawning worker threads."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    while True:
        _thread.start_new_thread(handle_connection, server.accept())


def handle_connection(client, address):
    """Answer an incoming question from the connected client."""
    print('Incoming connection from', address)
    client.settimeout(0.1)
    data = recvall(client)
    client.shutdown(socket.SHUT_RD)
    question = pickle.loads(data)
    answer = '''len(username) = {}
len(password) = {}
len(message) = {}'''.format(*map(len, question))
    client.sendall(answer.encode())
    client.shutdown(socket.SHUT_WR)
    client.close()
    print('Finished with', address)


def recvall(connection):
    """Receive all data from a socket and return as a bytes object."""
    buffer = bytearray()
    while True:
        try:
            data = connection.recv(1 << 12)
        except socket.timeout:
            pass
        else:
            if data:
                buffer.extend(data)
            else:
                return bytes(buffer)


def run_client(host, port):
    """Collect information from question and display returned answer."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(0.1) # wait for server to start listening for clients
    client.connect((host, port))
    time.sleep(0.1) # wait for handler thread to display connection
    username = input('Username: ')
    password = input('Password: ')
    message = input('Message: ')
    question = pickle.dumps((username, password, message))
    client.sendall(question)
    client.shutdown(socket.SHUT_WR)
    answer = recvall(client)
    client.shutdown(socket.SHUT_RD)
    client.close()
    print(answer.decode())
    time.sleep(0.1) # wait for handler to cleanly terminate execution

if __name__ == '__main__':
    main()