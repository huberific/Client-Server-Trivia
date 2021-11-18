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

def printOptions(options):
    for o in options:
        print(o)

def fixHTMLFormatStr(str):
    str = str.replace("&quot;", '"')
    str = str.replace("&#039;", "'")
    str = str.replace("&amp;", '&')
    return str

def fixHTMLFormat(options):
    fixedOptions = []
    for o in options:
        newStr = fixHTMLFormatStr(o)
        fixedOptions.append(newStr)
    return fixedOptions

def format(question, options, answer):
    optionNum = 1
    payload = question + '\n'
    for o in options:
        payload += ('\t' + str(optionNum) + ". " + o + '\n')
        optionNum += 1
    payload += "\tChoose correct numbered option.\n"
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

# function to get trivia json info:
def loadQuestion():
    with urllib.request.urlopen("https://opentdb.com/api.php?amount=1") as url:
        jsonData = json.loads(url.read().decode()) # returns json data
        question = jsonData["results"][0]["question"]
        options  = jsonData["results"][0]["incorrect_answers"]
        answer   = jsonData["results"][0]["correct_answer"]
        question = fixHTMLFormatStr(question)
        answer   = fixHTMLFormatStr(answer)
        options  = fixHTMLFormat(options)
        options.append(answer)
        random.shuffle(options)
        fullQuestion = [question, options, answer]
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

welcome  = 'Welcome to Client-Server-Trivia! Would you like to play? (yes or no)'
newRound = 'Wanna play again? (yes or no)'
thanks   = 'Thanks for playing, bye!\n'
oopsMsg  = 'Oops. That is incorrect. The correct answer was '
correct  = "That's correct, well done!"

# buffer size in bytes accepted by connection socket:
BUFSIZE = 2048

# for holding the question options and correct answer:
options = []
answer = ''

# new socket connection is created with client after handshake:
while True:
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
        try:
            if int(msgRcv) == getCorrectAnswer(answer, options):
                payload = correct
                print('\nSending>>>>>>>>')
                connectionSocket.send(payload.encode())
                print(payload)
                continue
        except ValueError:
            try:
                if int(msgRcv) != getCorrectAnswer(answer, options):
                    payload = getIncorrectMsg(answer, options)
                    print('\nSending>>>>>>>>')
                    connectionSocket.send(payload.encode())
                    print(payload)
                    continue
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
                question = fullQuestion[0]
                options = fullQuestion[1]
                answer = fullQuestion[2]
                payload = format(question, options, answer)
                print('\nSending>>>>>>>>')
                connectionSocket.send(payload.encode())
                print(payload)
            elif msgRcv == "no":
                payload = thanks
                connectionSocket.send(payload.encode())
                break
            elif msgRcv != "yes" and msgRcv != "no":
                payload = getIncorrectMsg(answer, options)
                print('\nSending>>>>>>>>')
                print(payload)
                connectionSocket.send(payload.encode())
        continue

connectionSocket.close()
# note, serverSocket remains open to welcome new handshakes from clients
