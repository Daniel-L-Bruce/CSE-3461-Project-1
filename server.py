import sys
import os
import threading
import string
from socket import *

# This is the function for the handler thread
def handler(client_soc, client_addr):
    # This will loop until the user gives a unique username
    unique = False
    while not unique:
        username = client_soc.recv(200).decode()
        # If the username returns nothing, terminate the client, as it likely disconnected
        with username_lock:
            if not username:
                clients.remove((client_soc, client_addr))
                client_soc.close()
                return
            # Respond with true or false to the client
            if username not in usernames:
                unique = True
                client_soc.send("True".encode())
                # Add the username to the list
                usernames[username] = client_soc
            else:
                client_soc.send("False".encode())


    # Listen for messages to be handles
    while True:
        message = client_soc.recv(1000).decode()
        # If the message returns nothing, terminate the client, as it likely disconnected
        if not message:
            # Give the username lock to ensure the username list is only being used by the deletes here
            with username_lock:
                clients.remove((client_soc, client_addr))
                usernames.pop(username, None)
                client_soc.close()
            return
        # If the message is a broadcast is a 1, then send message to everyone
        if message[0] == '1':
            message = username + ": " + message[2:]
            # Give the username lock to ensure the username list remains the same during broadcast
            with username_lock:
                for name, client_s in usernames.items():
                    client_s.send(message.encode())


    return


# Create a TCP socket for the server  
server = socket(AF_INET, SOCK_STREAM)

# Bind this socket to the server IP and port
server.bind(("0.0.0.0", 20000))

# Put the server into listening mode
server.listen()

# Initialize a list of threads for the different clients and one for usernames
clients = [] # This may be unneccessary but I wanted to create it in case it is needed
usernames = {} # This will be helpful for peer to peer
# This will be used to ensure the usernames do not enter a race condition
username_lock = threading.Lock()

# Loop until the server is closed
while True:
    # Accept the new client connection
    client_soc, client_addr = server.accept()

    # Store the info about the connection
    clients.append((client_soc, client_addr))

    # Create the thread and start it
    thread = threading.Thread(target=handler,args=(client_soc, client_addr))
    thread.start()
    



# Close any open sockets
server.close()
