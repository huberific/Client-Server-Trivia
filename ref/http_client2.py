################################################################################
# Due Date:    10-17-2021
# Author:      Aaron Huber
# Title:       Project 1 - Sockets and HTTP (Client File 2) 
# Description: This program creates the client-side socket for sending
#              messages and receiving responses.
#
# References:
#   Overall client structure:
#   [1> Computer Networking, A Top-Down Approach, 7th Edition (pg 202/856) 
#
#   Looping .recv method till full message received:
#   [2> https://pythonprogramming.net/sockets-tutorial-python-3/
################################################################################

# [1> throughout
# socket module forms basis for network communication in python:
from socket import *

server     = 'gaia.cs.umass.edu'
path       = '/wireshark-labs/HTTP-wireshark-file3.html'
serverPort = 80
version    = 'HTTP/1.1'
method     = 'GET'

# client socket created. AF_INET indicates IPv4, SOCK_STREAM indicates TCP.
# the server socket is the welcoming socket (handshake):
clientSocket = socket(AF_INET, SOCK_STREAM)

# note: operating system determines port for the client side

# initiate TCP connection between the client and server
# three-way handshake is performed after this method:
clientSocket.connect((server, serverPort))

# message sent to server:
msg = method + ' ' + path + ' ' + version + '\r\nHost:' + server + '\r\n\r\n'

print('Request: ' + method + ' ' + path + ' ' + version)
print('Host: ' + server)

# send bytes to server, then wait for response:
clientSocket.send(msg.encode())

# [2> place characters from server in variable. loop until full data received:
BUFSIZE = 4096
msgBack = ''
while True:
    msgPortion = clientSocket.recv(BUFSIZE)
    if len(msgPortion) <= 0:
        break
    msgBack += msgPortion.decode()

# print message length and message received from server:
print ('\n\n[RECV] - length:', len(msgBack))
print(msgBack)

clientSocket.close()
