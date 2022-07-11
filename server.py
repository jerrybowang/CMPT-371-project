# Imports
from audioop import add
import socket
from _thread import *
import sys

server = "192.168.1.96"
port = 5555 # unused port number

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP connection

try:
    s.bind((server, port)) # Binds server to port
except socket.error as e:
    str(e)

s.listen(2) 
print("Waiting for a connection, server started")

# Threaded function
def threaded_client(conn):
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)
            
            conn.sendall(str.encode(reply))
        except:
            break

# Continously look for connections
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    # starts new thread
    start_new_thread(threaded_client, (conn,))