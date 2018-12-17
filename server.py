"""
This module is made for server, which sends data from user to another user.
Users can send data contionusly, and server uses threading to contionusly
receive data from multiple users.
"""
import socket
from _thread import start_new_thread

HOST = "127.0.0.1"
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

def handle_client(conn):
    """
    Function, which every thread runs.
    """
    while True:
        data = conn.recv(4096)
        message = data.decode()
        print("Client said: ", message)
        if message.lower() == "quit" or message.lower() == "q":
            print("Client has left the chat")
        msq = message.swapcase()
        b_msq = str.encode(msq)
        conn.sendall(b_msq)

while True:
    connection, addr = s.accept()
    print("Connecte by:", addr)
    start_new_thread(handle_client, (connection,))
