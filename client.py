import sys
import os
import threading
import string
from socket import *

# Define the listener thread function
def listener():
    # Constantly listen for a message from the server
    while True:
        # Receive the message from the server (chose 1000 randomly + 200 for username)
        message = client.recv(1200)
        # If the server shuts down, the user will recieve this
        if not message:
            print("Disconnected from server.")
            break
        # Print received message
        print("Message received: ", message.decode())


# Create a socket for the client
client=socket(AF_INET, SOCK_STREAM)
# Connect client to the server at the server port; 
client.connect(("127.0.0.1", 20000))

# Make the user send a valid username
unique = False
while not unique:
    # Make the user enter a username
    username = input("Enter a unique username: ")
    # Send the username
    client.send(username.encode())
    # Check if it is valid
    valid = client.recv(200).decode()
    if valid == "True":
        unique = True
    else:
        # If it is not valid alert the user
        print("Username not valid.")

# Create the listener thread 
listenThread = threading.Thread(target=listener)

# Start the thread
listenThread.start()


option = "1" # Give option a value to be able to enter while
# Wait until the user enters a proper option
while (option == "1" or option == "2"):
    option = input("Please enter a 1 for broadcast and a 2 for peer to peer, anything else to cancel: \n")
    if option == "1":
        data = input("Please enter the message you want to broadcast: \n")
        # Add the 1: to indicate to the server we want to broadcast
        data = "1:" + data
        # Send this to the server for it to broadcast to other clients
        client.send(data.encode())
        # print debugging information
        print("Data sent: " + data)
    elif option == "2":
        print("You would like to send to a specific user")

# Close any open sockets
client.close()



