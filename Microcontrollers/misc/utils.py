#!/usr/bin/env python3
import time
import re
import sys

def sendMsg(socket, outgoingData):

    if outgoingData == None:
        raise ValueError("Outgoing data cannot be null")
    if socket == None:
        raise ValueError("Socket cannot be null")
    
    try:
        # Send message to server
        socket.sendall(outgoingData.encode())
    except:
        raise Exception("Could not send message")
    return None
    
def recvMsg(socket):
   
    try:
        # resultString holds received message
        resultString = ""
        # Try to receive bytes from socket
        receivedBytes = socket.recv(2048)
        
        while len(receivedBytes) > 0:            
            # Decode receivedBytes
            bytes_str = receivedBytes.decode()
                        
            # Append to result string
            resultString += bytes_str
            
            # Read receivedBytes
            receivedBytes = socket.recv(2048)
                        
        return resultString
    except:
        raise Exception("Could not receive message")
        
def abnormalShutdown(socket, message):
    print(message)
    socket.shutdown(2)
    socket.close()
    sys.exit(0)