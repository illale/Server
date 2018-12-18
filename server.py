"""
This module is made for server, which sends data from user to another user.
Users can send data contionusly, and server uses threading to contionusly
receive data from multiple users.
"""
import socket
from _thread import start_new_thread
import threading

HOST = "192.168.1.85"
PORT = 2222

print_lock = threading.Lock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

def handle_client(conn):
    """
    Function, which every thread runs.
    """
    name = conn.recv(4096)
    str_name = name.decode()
    while True:
        data = conn.recv(4096)
        message = data.decode()
        with print_lock:
            print(str_name, "said: ", message)
        if message.lower() == "quit" or message.lower() == "q":
            print(str_name, "has left the chat")
        msq = message.swapcase()
        conn.sendall(str.encode(msq))

while True:
    connection, addr = s.accept()
    print("Connected by:", addr)
    start_new_thread(handle_client, (connection,))
