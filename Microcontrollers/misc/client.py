#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM
from server import server_port
from utils import sendMsg, recvMsg, abnormalShutdown

def get_node_status(node_id):
    # Create socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # Connect to localhost on specified port
    clientSocket.connect(('127.0.0.1', server_port()))
    # Print connection information to console
    #print("Connected to " + str(clientSocket.getpeername()[0]) + " on port " + str(server_port()))

    try:
        sendMsg(clientSocket, str(node_id))
    except:
        abnormalShutdown(clientSocket, "Error")
                    
    # Shut down write side of socket
    clientSocket.shutdown(1)
    
    # Receive incoming message from server
    return recvMsg(clientSocket)
    #print("Received from server " + str(incomingMsg))
    # Close socket
    clientSocket.close()
    
    #print("Connection closed")
