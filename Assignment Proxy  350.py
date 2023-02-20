import socket
import datetime

PROXY_ADDRESS = '127.0.0.1'  # Change this to the IP address of your proxy server
PROXY_PORT = 12345

# Create a TCP/IP socket
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
proxy_socket.bind((PROXY_ADDRESS, PROXY_PORT))

# Listen for incoming connections
proxy_socket.listen(1)

print('Proxy server listening on', PROXY_ADDRESS, 'port', PROXY_PORT)

while True:
    # Wait for a client connection
    client_socket, client_address = proxy_socket.accept()

    # Receive the request from the client
    request = b''
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        request += data

    # Parse the request to get the destination server IP address
    destination_address = request.split(b'\r\n')[1].split(b' ')[1].split(b':')[0].decode()

    # Print a message describing this request with the IP and exact time of the request
    print('Received request for', destination_address, 'from', client_address, 'at', datetime.datetime.now())

    # Send the client's request to the destination server
    try:
        destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination_socket.connect((destination_address, 80))
        destination_socket.sendall(request)

        # Print a message with exact time of the actual request
        print('Sent request to', destination_address, 'at', datetime.datetime.now())

        # Receive the response from the destination server
        response = b''
        while True:
            data = destination_socket.recv(4096)
            if not data:
                break
            response += data

        # Print a message that the response was received with the exact time
        print('Received response from', destination_address, 'at', datetime.datetime.now())

        # Send the response back to the client
        client_socket.sendall(response)

        # Print a message that the response was sent with the exact time
        print('Sent response to', client_address, 'at', datetime.datetime.now())

        # Close the connection to the destination server
        destination_socket.close()

    except Exception as e:
        # If there was any error from the client side or from the server side, the proxy server should display a message and return an error message to the client
        print('Error:', e)
        client_socket.sendall(b'HTTP/1.1 500 Internal Server Error\r\n\r\n')

    # Close the connection to the client
    client_socket.close()

