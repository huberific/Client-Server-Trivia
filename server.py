################################################################################
# Due Date:    12-05-2021
# Author:      Aaron Huber
# Title:       Project 4 - Client-Server-Trivia
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
###############################################################################

# [1> throughout
# socket module forms basis for network communication in python:
import socket
import random
import urllib.request, json
import html         # for fixing html special characters
from html.parser import HTMLParser
import time # for pausing momentarily

# free trivia api: https://opentdb.com/api_config.php
triviaAPILink = "https://opentdb.com/api.php?amount=1&difficulty=easy"

def printOptions(options):
    for o in options:
        print(o)

# fix HTML characters
# https://www.geeksforgeeks.org/python-convert-html-characters-to-strings/kkj
def fixHTMLChars(str):
    h = html.parser
    newStr = h.unescape(str)
    return newStr

def fixHTMLFormat(options):
    fixedOptions = []
    for o in options:
        newStr = fixHTMLChars(o)
        fixedOptions.append(newStr)
    return fixedOptions

def format(category, question, options, answer):
    payload = "\n\n\tCatagory - " + category + '\n\t' + question + '\n'
    optionNum = 1
    for o in options:
        payload += ('\t\t' + str(optionNum) + ". " + o + '\n')
        optionNum += 1
    payload += "\tEnter your answer by its number.\n"
    return payload

def getCorrectAnswer(ans, options):
    num = 1
    for o in options:
        if o == ans:
            return num
        num += 1
    return -1

def getIncorrectMsg(ans, options):
    msg = "That's incorrect. The correct answer was "
    num = getCorrectAnswer(ans, options)
    msg += (str(num) + ". " + ans)
    return msg

def getInvalidMsg(ans, options):
    msg = "That's an invalid answer. The correct answer was "
    num = getCorrectAnswer(ans, options)
    msg += (str(num) + ". " + ans)
    return msg

# function to get trivia json info:
def loadQuestion():
    with urllib.request.urlopen(triviaAPILink) as url:
        jsonData = json.loads(url.read().decode()) # returns json data
        question = jsonData["results"][0]["question"]
        options  = jsonData["results"][0]["incorrect_answers"]
        answer   = jsonData["results"][0]["correct_answer"]
        category = jsonData["results"][0]["category"]
        question = fixHTMLChars(question)
        answer   = fixHTMLChars(answer)
        category = fixHTMLChars(category)
        options  = fixHTMLFormat(options)
        options.append(answer)
        random.shuffle(options)
        fullQuestion = [category, question, options, answer]
        return fullQuestion

# [ref> https://www.delftstack.com/howto/python/dict-to-string-in-python/

serverPort = int(random.uniform(49152, 65535))  # arbitrary port number
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

welcome  = "Welcome to Client-Server-Trivia! Would you like to play? ('yes' " +\
           "to continue or '/q' to quit)"
newRound = "Wanna play again? ('yes' to continue or '/q' to quit)"
thanks   = "Thanks for playing, bye!\n"
oopsMsg  = "Oops. That's incorrect. The correct answer was "
correct  = "That's correct, well done!"

# buffer size in bytes accepted by connection socket:
BUFSIZE = 2048

# for holding the question options and correct answer:
options = []
answer = ''
exit = "n"

# new socket connection is created with client after handshake:
while exit is not "y":
    # client knocks on door and a new socket, connectionSocket, is created:
    connectionSocket, addr = serverSocket.accept()      
    # [3> tutorial ref for printing address info:
    print ('------------------------- SERVER  --------------------------------')
    print(f"Connected by {addr}\n")
    # [4> https://www.geeksforgeeks.org/simple-chat-room-using-python/
    count = 0
    while True:
        msgRcv = connectionSocket.recv(BUFSIZE).decode()
        print('from client: ' + msgRcv)
        answered = "n"
        exit = "n"
        if msgRcv == '':
            msgRcv = 'invalid'

        try:
            if int(msgRcv) == getCorrectAnswer(answer, options):
                payload = correct
                print('\nSending>>>>>>>>')
                connectionSocket.send(payload.encode())
                answered = "y"
                print(payload)
        except ValueError:
            try:
                if int(msgRcv) != getCorrectAnswer(answer, options):
                    payload = getIncorrectMsg(answer, options)
                    print('\nSending>>>>>>>>')
                    connectionSocket.send(payload.encode())
                    answered = "y"
                    print(payload)
            except ValueError:
                payload = ''
        finally:
            if msgRcv == "init":
                payload = welcome
                print('\nSending>>>>>>>>')
                connectionSocket.send(payload.encode())
                print(payload)
            elif msgRcv == "yes":
                fullQuestion = loadQuestion()
                category = fullQuestion[0]
                question = fullQuestion[1]
                options = fullQuestion[2]
                answer = fullQuestion[3]
                payload = format(category, question, options, answer)
                print('\nSending>>>>>>>>')
                connectionSocket.send(payload.encode())
                print(payload)
            elif msgRcv == "/q":
                payload = thanks
                connectionSocket.send(payload.encode())
                exit = "y"
                break
            elif answered == "n":
                payload = getIncorrectMsg(answer, options)
                print('\nSending>>>>>>>>')
                print(payload)
                connectionSocket.send(payload.encode())
            if msgRcv != "init" and msgRcv != "yes" and exit == "n":
                payload = newRound
                time.sleep(1)
                connectionSocket.send(payload.encode())
                print(payload)
                payload = 'invalid'
        continue

connectionSocket.close()
