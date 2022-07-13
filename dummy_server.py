# This dummy server is used to test client.py only

import socket
import threading

# local host
HOST = 'localhost'
# Port to listen on (non-privileged ports are > 1023)
PORT = 5555

END = False


def receive(conn):
    global END
    while not END:
        try:
            data = conn.recv(1024)
            command = data.decode('utf-8')
            print(command)
        except:
            pass


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

