import socket

# Set the port number you want to listen on
PORT = 1883
HOST = "200.119.184.91"

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
HOST = socket.gethostname()

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}")

while True:
    # Wait for a connection
    print('Waiting for a connection...')
    conn, addr = server_socket.accept()
    print(f'Got connection from {addr}')

    # Receive the data in small chunks and retransmit it
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode()}")
        conn.sendall(data)

    # Clean up the connection
    conn.close()
