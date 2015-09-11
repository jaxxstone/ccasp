'''This module is used by the Receiver application to get the status (on/off)
of an end node. It is currently incomplete. It is meant to establish a TCP 
socket connection with the host machine to transmit a command.'''

from django.core.management.base import BaseCommand
from socket import socket, AF_INET, SOCK_STREAM
from server import server_port
from utils import sendMsg, recvMsg, abnormalShutdown

class Command(BaseCommand):
    '''Default class for Django's management commands'''
    help = "creates TCP socket connection to master controller host"

    def add_arguments(self, parser):
        parser.add_argument('args')

    def handle(self, *args, **options):
        # Get node ID
        node_id = int(args[0])

        # Create socket
        client_socket = socket(AF_INET, SOCK_STREAM)
        # Connect to host on specified port
        client_socket.connect(('127.0.0.1', server_port()))

        # Try to contact server
        try:
            sendMsg(client_socket, str(node_id))
        except:
            abnormalShutdown(client_socket, "Error")

        # Shut down write side of socket
        client_socket.shutdown(1)

        # Receive incoming message from server
        try:
            response = recvMsg(client_socket)
        except:
            print "Could not receive message from server"

        # Close socket
        client_socket.close()
        return response
