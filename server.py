#  Step 1: Initialize empty project structure
#  Import basic modules and build the most basic TCP server

import socket      # For network communication
import threading   # For handling multiple clients later
import time        #  For timing (to be used later)
#  Step 3:  Define shared tuple space and lock
#  Stores key-value pairs safely during multithreaded access

tuple_space = {}               #  Shared dictionary for client data
space_lock = threading.Lock()  #  Lock to prevent data conflict between threads
# Step 4: Handle and process client requests
#  Process PUT, GET, READ operations from clients

def process_request(request):
    try:
        parts = request.strip().split(" ", 2)  #  Split request into parts
        if len(parts) < 2:
            return "000 ERR Invalid request format"

        cmd = parts[1]  #  Get command type

        if cmd == 'P':  # PUT
            if len(parts) < 3:
                return "000 ERR Missing key or value"
            key_value = parts[2].split(" ", 1)
            if len(key_value) < 2:
                return "000 ERR Incomplete key-value"
            key, value = key_value
            with space_lock:
                if key in tuple_space:
                    msg = f"ERR {key} already exists"
                else:
                    tuple_space[key] = value
                    msg = f"OK ({key}, {value}) added"

        elif cmd == 'G':  # GET
            key = parts[2]
            with space_lock:
                if key in tuple_space:
                    value = tuple_space.pop(key)
                    msg = f"OK ({key}, {value}) removed"
                else:
                    msg = f"ERR {key} not found"

        elif cmd == 'R':  # READ
            key = parts[2]
            with space_lock:
                if key in tuple_space:
                    value = tuple_space[key]
                    msg = f"OK ({key}, {value}) exists"
                else:
                    msg = f"ERR {key} not found"

        else:
            msg = "ERR Unknown command"

    except Exception as e:
        msg = f"ERR Exception: {str(e)}"

    return f"{len(msg):03d} {msg}"
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