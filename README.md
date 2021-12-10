# Client-Server-Trivia

## Overview
This program is a shell based text game where a client plays trivia with a server using Python sockets. The following website was used for free trivia API:

https://opentdb.com/api_config.php

The server program pulls 1 question per round using "easy" settings.

## Instructions
To run the program, download the files into a Mac or Linux machine directory. For best results open two terminal shells.

In terminal one, enter the following command to fire up the server-side program:

  ```
  python3 server.py
  ```
  
  ![image](https://user-images.githubusercontent.com/54946106/145160438-c2719ef0-7e72-4407-8c3f-c8a8940b5c16.png)

  
In terminal two, enter the following command to fire up the client-side program:

  ```
  python3 client.py 50489
  ``` 
  *NOTE: 50489 is the randomly generated port number created by the server, copy this from terminal one.*
  
  ![image](https://user-images.githubusercontent.com/54946106/145160546-a882a51a-9c83-4151-a68b-dcbb78683b61.png)
  
  Once the client program is running, follow the directions to play the trivia game. A example screenshot is included below.
  
  ## Sample Output
  ![image](https://user-images.githubusercontent.com/54946106/145160640-7a849bce-51fa-4c6a-af5f-538e8eabd987.png)


  
  
