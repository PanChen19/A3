#  Step 1: Initialize empty project structure
#  Import basic modules and build the most basic TCP server

import socket      # For network communication
import threading   # For handling multiple clients later
import time        #  For timing (to be used later)
# Step 2: Use threads to handle multiple clients
#  Each client gets its own thread so the server can continue accepting others

def handle_client(client_socket, address):
    print(f"[THREAD] Handling client {address}")
    client_socket.sendall("Hello from server!\n".encode())  #  Send welcome message
    client_socket.close()  #  Close connection after handling

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    server_socket.bind(("", port))  #  Bind to a port
    server_socket.listen()  #  Start listening for connections
    print(f"[STARTED] Server is running on port {port}")

    while True:
        client_socket, address = server_socket.accept()  #  Wait and accept a client connection
        print(f"[CONNECTED] Client connected from: {address}")

        # Start a new thread for each client
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")  # Show active client threads

#  Main entry point
if __name__ == "__main__":
    default_port = 51234  #  Default port
    start_server(default_port)