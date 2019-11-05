import socket
import threading
from time import sleep

LOGIC = {
    "STOP": False
}

HOST = "127.0.0.1"
PORT =  2225


def send_data():
    """
    Sends data to server contionusly.
    """
    name = input("Give your name: ")
    s.sendall(str.encode(name))
    print("Waiting for other users to connect")
    pairs = s.recv(4096)
    print(pairs.decode())
    pair = input("Give the person you want to connect to: ")
    s.sendall(str.encode(pair))
    while True:
        msq = input("Say: ")
        if msq.lower() == "quit" or msq.lower() == "q":
            LOGIC["STOP"] = True
            break
        b_msq = str.encode(msq)
        s.sendall(b_msq)
        sleep(0.2)
        continue

def receive_data():
    """
    Receive data from server. The data is sent by another users.
    """
    while True:
        b_msq = s.recv(4096)
        msq = b_msq.decode()
        with print_lock:
            print("Server:", msq)
        if LOGIC["STOP"]:
            break

if __name__ == "__main__":
    print_lock = threading.Lock()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    t1 = threading.Thread(target=send_data)
    t2 = threading.Thread(target=receive_data)
    t1.start()
    t2.start()
