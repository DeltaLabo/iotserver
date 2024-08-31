import socket

# Set the port number and host to connect to
PORT = 1883
HOST = "200.119.184.91"

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set a timeout in seconds
TIMEOUT = 5  # 5 seconds

# Set the timeout on the socket
client_socket.settimeout(TIMEOUT)

try:
    # Connect to the server
    client_socket.connect((HOST, PORT))

    # Send some data
    message = b"Hello, world"
    print(f"Sending: {message.decode()}")
    client_socket.sendall(message)

    # Receive the response
    data = client_socket.recv(1024)
    print(f"Received: {data.decode()}")

    # Check if the response matches the sent data
    if data == message:
        print("Test passed! The server responded correctly.")
    else:
        print("Test failed. The server did not respond correctly.")

except socket.timeout:
    print(f"Timeout occurred after {TIMEOUT} seconds.")
except socket.error as e:
    print(f"Socket error: {e}")
finally:
    # Close the connection
    client_socket.close()
