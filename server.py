#  Step 1: Initialize empty project structure
#  Import basic modules and build the most basic TCP server

import socket      # For network communication
import threading   # For handling multiple clients later
import time        #  For timing (to be used later)

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 TCP 套接字 / Create a TCP socket
    server_socket.bind(("", port))  #  Bind to a port
    server_socket.listen()  #  Start listening for connections
    print(f"[STARTED] Server is running on port {port}")

    #  Wait for one client connection and respond
    client_socket, address = server_socket.accept()
    print(f"[CONNECTED] Client connected from: {address}")
    client_socket.sendall("Hello from server!\n".encode())  #  Send welcome message
    client_socket.close()  # Close connection

# 主程序入口 / Main entry point
if __name__ == "__main__":
    default_port = 51234  # Default port
    start_server(default_port)