"""
This module is made for server, which sends data from user to another user.
Users can send data contionusly, and server uses threading to contionusly
receive data from multiple users.
"""
import socket
from _thread import start_new_thread
import threading

USERS = {

}

HOST = "192.168.1.69"
PORT = 2222

print_lock = threading.Lock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
print("Waiting for a connection...")

def handle_client(conn):
    """
    Function, which every thread runs.
    """
    name = conn.recv(4096)
    str_name = name.decode()
    USERS[str_name] = conn
    while True:
        if len(USERS) <= 1:
            print("Waiting for more clients to connect")
        else:
            break
    for name in USERS:
        conn.sendall(name)
    pair = conn.recv(4096)
    str_pair = pair.decode()
    s_conn = USERS[str_pair]
    while True:
        data = conn.recv(4096)
        s_conn.sendall(data)

while True:
    connection, addr = s.accept()
    print("Connected by:", addr)
    start_new_thread(handle_client, (connection,))
