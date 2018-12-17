import socket
import threading

LOGIC = {
    "STOP": False
}

HOST = "127.0.0.1"
PORT =  5555

print_lock = threading.Lock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def send_data():
    """
    Sends data to server contionusly.
    """
    while True:
        msq = input("Say: ")
        if msq.lower() == "quit" or msq.lower() == "q":
            LOGIC["STOP"] = True
            break
        b_msq = str.encode(msq)
        s.sendall(b_msq)
        with print_lock:
            print(msq)

def receive_data():
    """
    Receive data from server. The data is  sent by another users.
    """
    while True:
        b_msq = s.recv(4096)
        msq = b_msq.decode()
        if LOGIC["STOP"]:
            break
        with print_lock:
            print(msq)


t1 = threading.Thread(target=send_data)
t2 = threading.Thread(target=receive_data)
t1.daemon = True
t2.daemon = True
t1.start()
t2.start()
