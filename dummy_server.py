# This dummy server is used to test client.py only

import socket
import threading

import random

# local host
HOST = 'localhost'
# Port to listen on (non-privileged ports are > 1023)
PORT = 5555

END = False



def receive(conn):
    bomb_list = bombs()
    global END
    while not END:
        try:
            data = conn.recv(1024)
            button = data.decode('utf-8')
            print(bomb_list)
            button_number = int(button)
            print(button_number)
            if (button_number in bomb_list):
                print("player died")
        except:
            pass

def bombs():
    bomb_list = []
    for i in range(1,16): # choose 16 random numbers to be bombs
        n = random.randint(1,256) # total of 256 numbers
        bomb_list.append(n)
    return bomb_list



# This server can only handle on connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Waiting for a connection")
    conn, addr = s.accept()
    print("Start to type token messages to test")
    print("Type 'end' to exit this dummy server")

    with conn:
        receive_thread = threading.Thread(target=receive, args=[conn])
        receive_thread.start()
        while True:
            msg = input()
            if msg == "end":
                END = True
                conn.sendall(bytes(msg, encoding='utf8'))
                break
            conn.sendall(bytes(msg, encoding='utf8'))

    receive_thread.join()

