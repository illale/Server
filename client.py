import socket
import threading
from time import sleep

HOST = "192.168.1.85"
PORT =  2222

print_lock = threading.Lock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def send_data():
    """
    Sends data to server contionusly.
    """
    name = input("Give your name: ")
    s.sendall(str.encode(name))
    while True:
        msq = input("Say: ")
        b_msq = str.encode(msq)
        s.sendall(b_msq)
        sleep(0.2)
        continue

def receive_data():
    """
    Receive data from server. The data is sent by another users.
    """
    while True:
        b_msq = s.recv(1024)
        msq = b_msq.decode()
        with print_lock:
            print("Server said:", msq)

t1 = threading.Thread(target=send_data)
t2 = threading.Thread(target=receive_data)
t1.start()
t2.start()
