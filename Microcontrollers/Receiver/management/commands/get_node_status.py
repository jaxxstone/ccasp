from django.core.management.base import BaseCommand
from socket import socket, AF_INET, SOCK_STREAM
from server import server_port
from utils import sendMsg, recvMsg, abnormalShutdown


class Command(BaseCommand):
    help = "creates TCP socket connection to master controller host"

    def add_arguments(self, parser):
        parser.add_argument('args')

    def handle(self, *args, **options):

        # Get node ID
        nodeID = int(args[0])
        
        # Create socket
        clientSocket = socket(AF_INET, SOCK_STREAM)
        # Connect to host on specified port
        clientSocket.connect(('127.0.0.1', server_port()))
        
        # Try to contact server
        try:
            sendMsg(clientSocket, str(nodeID))
        except:
            abnormalShutdown(clientSocket, "Error")
                        
        # Shut down write side of socket
        clientSocket.shutdown(1)
        
        # Receive incoming message from server
        try:
            response = recvMsg(clientSocket)
        except:
            print "Could not receive message from server"

        #print("Client returning response")
        # Close socket
        clientSocket.close()
        return response
