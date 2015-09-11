#!/usr/bin/env python

from socket import socket, AF_INET, SOCK_STREAM
import time
import serial
from django.conf import settings
from utils import sendMsg, recvMsg, abnormalShutdown
def server_port():
    return 12322

if __name__ == "__main__":
    # Create socket object
    socket = socket(AF_INET, SOCK_STREAM)
    # Bind socket to localhost on defined port
    socket.bind(('', server_port()))
    # Start listening
    socket.listen(0)
    
    while True:
        # Accept connections while server is alive
        conn, address = socket.accept()
        
        # Print connection information
        #print("Connection received from client address " + str(address[0]) + " on port " + str(address[1]))
        
        # Try to receive incoming message and starting time
        incomingMsg = recvMsg(conn)
        # Print message from client
        #print("Received from client: " + str(incomingMsg))

        ser = serial.Serial(settings.TTY_PORT, '9600', timeout=5)
        time.sleep(2)

        try:
            ser.write(str(incomingMsg))
        except:
            print("Error during serial write")
        
        time.sleep(2)
        try:
            result = ser.read()
        except:
            print("Error during serial read")

        # Send serial value to client
        sendMsg(conn, result)
        # Try to shut down write side of socket
        # If successful, print server-side messages
        # Otherwise inform server that client abnormally terminated
        try:
            # Shutdown write side of socket
            conn.shutdown(1)
        except:
            print("Abnormal termination from client\n")
            
        # Clock the connection
        conn.close()
        
    
