################################################################################
# Due Date:    10-17-2021
# Author:      Aaron Huber
# Title:       Project 1 - Sockets and HTTP (Server File) 
# Description: This program creates the server-side socket for accepting
#              incoming messages and sending responses.
#
# References:
#   Overall server structure:
#   [1> Computer Networking, A Top-Down Approach, 7th Edition (pg 205/856) 
#
#   Socket module syntax:
#   [2> https://www.tutorialspoint.com/python3/python_networking.htm
#
#   Socket receiving large files:
#   [3> https://stackoverflow.com/questions/17667903/
#       python-socket-receive-large-amount-of-data
##############################################################################k

# [1> throughout
# socket module forms basis for network communication in python:
import socket

serverPort = 59897                              # arbitrary port number
server     = socket.gethostname()               # get host name of server
hostIP     = socket.gethostbyname(server)       # get IP address of server

# [2> reference used for 'socket.*' syntax
# server socket created. AF_INET indicates IPv4, SOCK_STREAM indicates TCP.
# the server socket is the welcoming socket (handshake):
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# associate the server port number:
serverSocket.bind((hostIP, serverPort))

# server socket listens for TCP connection requests and allows max number of 
# queued connections (at least 1)
serverSocket.listen(1)

print('Server listening on ' + str(hostIP) + ':' + str(serverPort))

# data package to be sent:
data =  "HTTP/1.1 200 OK\r\n"\
        "Content-Type: text/html; charset=UTF-8\r\n\r\n"\
        "<html>Congratulations!  You've downloaded the first Wireshark lab"\
        "file!</html>\r\n"

# buffer size in bytes accepted by connection socket:
BUFSIZE = 2048

# new socket connection is created with client after handshake:
while True:
    # client knocks on door and a new socket, connectionSocket, is created:
    connectionSocket, addr = serverSocket.accept()      
    # [3> tutorial ref for printing address info:
    print(f"Connected by {addr}\n")
    # receive msg back [3>:
    segments = []
    while True:
        portion = connectionSocket.recv(BUFSIZE)
        segments.append(portion)
        if len(portion) <= BUFSIZE:
            break
    msg = b''.join(segments)
    print('Received: ', msg)
    connectionSocket.send(data.encode())
    print('\nSending>>>>>>>>')
    print(data)
    print('<<<<<<<<')
    connectionSocket.close()

# note, serverSocket remains open to welcome new handshakes from clients
