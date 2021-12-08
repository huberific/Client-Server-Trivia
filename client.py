###################################################################################
# Date:        12-05-2021
# Author:      Aaron Huber
# Title:       Client-Server-Trivia
# Description: This program creates the client-side socket component of the
#              Client-Server-Chat interface. It receives trivia questions from
#              the server and sends answers.
#
# References:
#   Overall client structure:
#   [1> Computer Networking, A Top-Down Approach, 7th Edition (pg 202/856) 
###################################################################################

# [1> overall client structure throughout
# socket module forms basis for network communication in python:
from socket import *
import sys

# exit program if incorrect arguments received:
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

msg = "init"         # first msg sent to server to initiate
msgBack = ''         # holds msg received

# strings used for checking server response:
correctMsg = "That's correct"
incorrectMsg = "That's incorrect"
invalidMsg = "That's an invalid answer"
finalMsg = "Thanks for playing, bye"

# size of buffer to receive message in bytes:
BUFSIZE = 4096
    
while True:
    # exit if user wants to quit:
    if msg == "\q":
        clientSocket.close()
        break

    # if-statement used to wait for server to ask to play again:
    if correctMsg not in msgBack and incorrectMsg not in msgBack:
        # send bytes to server, then wait for response:
        clientSocket.send(msg.encode())

    # place characters from server in variable:
    msgBack = clientSocket.recv(BUFSIZE).decode()
    
    # print message length and message received from server:
    print('\nserver: ' + msgBack)
    
    if finalMsg in msgBack:
        print("Good-bye!")
        break
    
    if (correctMsg not in msgBack and incorrectMsg not in msgBack and 
       invalidMsg not in msgBack):
        msg = input ("client: ")
        if msg == "":               # catch if user hits enter only and change
            msg = "invalid"
        msg = msg.rstrip('\n')
