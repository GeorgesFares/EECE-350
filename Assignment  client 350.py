# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 11:06:30 2023

@author: Lenovo
"""

import socket
import datetime

SERVER_ADDRESS = '127.0.0.1'  # Change this to the IP address of your server
SERVER_PORT = 12345

# Take the text to be sent as input
text = input('Enter the text to send: ')

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

# Send the text to the server
request = text.encode()
client_socket.sendall(request)
print('Sent request to', SERVER_ADDRESS, 'at', datetime.datetime.now())

# Receive the reply back from the server
response = b''
while True:
    data = client_socket.recv(4096)
    if not data:
        break
    response += data
print('Received response from', SERVER_ADDRESS, 'at', datetime.datetime.now())

# Print the response
print(response.decode())

# Close the connection
client_socket.close()
