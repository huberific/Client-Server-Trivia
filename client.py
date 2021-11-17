################################################################################
# Due Date:    10-17-2021
# Author:      Aaron Huber
# Title:       Project 1 - Sockets and HTTP (Client File 1) 
# Description: This program creates the client-side socket for sending
#              messages and receiving responses.
#
# References:
#   Overall client structure:
#   [1> Computer Networking, A Top-Down Approach, 7th Edition (pg 202/856) 
################################################################################

# [1> throughout
# socket module forms basis for network communication in python:
from socket import *
import sys

if len(sys.argv) != 2:
    print ("----------------------------------------------------------------")
    print ("Incorrect usage. Note, you must be logged onto the flip1 server.")
    print ("Please include the known port number on the flip1 server.")
    print ("example: python3 client.py 58932")
    print ("----------------------------------------------------------------")
    exit()

server     = 'flip1.engr.oregonstate.edu'
path       = '/'
serverPort = int(sys.argv[1])

# client socket created. AF_INET indicates IPv4, SOCK_STREAM indicates TCP.
# the server socket is the welcoming socket (handshake):
clientSocket = socket(AF_INET, SOCK_STREAM)

# note: operating system determines port for the client side

# initiate TCP connection between the client and server
# three-way handshake is performed after this method:
clientSocket.connect((server, serverPort))

# message sent to server:
# msg = method + ' ' + path + ' ' + version + '\r\nHost:' + server + '\r\n\r\n'

msg = "init"

count = 0

while True:
    if msg == "no":
        clientSocket.close()
        break

    # send bytes to server, then wait for response:
    clientSocket.send(msg.encode())

    # size of buffer to receive message in bytes:
    BUFSIZE = 4096
    
    # place characters from server in variable:
    msgBack = clientSocket.recv(BUFSIZE)
    
    # print message length and message received from server:
    print('server: ' + msgBack.decode())
    
    msg = input ("client: ")
    msg = msg.rstrip('\n')
