

import socket
import threading
import time
import sys
import pygame


HEADER = 2048
PORT = 5555  # port number
SERVER = socket.gethostbyname(socket.gethostname())  # get local host IP
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
END = "end"
Pressed = "Pressed"
player_num = "player#"
IP_and_Port = "IPandPort"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP connection
server.bind(ADDR)  # Binds server to port








def process_client(conn, addr, player_number):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)

        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)
            if msg == END:
                connected = False
            if msg == Pressed:
                press_player = conn.recv(HEADER).decode(FORMAT)
            if msg == player_num:
                player_number = str(player_number)
                player_number = "player# " + player_number
                conn.send(player_number.encode((FORMAT)))
            if msg == IP_and_Port:
                address = (str(addr))
                address = "IP and port is: " + address
                print(f"[{addr}] {msg}")
                conn.send(address.encode((FORMAT)))

    conn.close()


def start():
    player_number = 0
    connections = []
    max_connections = int(input("Enter a number: "))
    server.listen()
    print(f"[LISTENING] Server is listing on {SERVER}")
    while True:
        conn, addr = server.accept()
        # the maximum player
        if len(connections) >= max_connections:
            conn.sendall(
                f"Connection overflow. Max amount is {max_connections}".encode())
            continue
        connections.append((conn, addr))
        player_number += 1
        # Threaded function
        thread = threading.Thread(
            target=process_client, args=(conn, addr, player_number))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}")


print("Please enter maximum player number for current game")
start()








































# # Imports
# from audioop import add
# import socket
# from _thread import *
# import sys

# server = "192.168.1.96"
# port = 5555 # unused port number

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP connection

# try:
#     s.bind((server, port)) # Binds server to port
# except socket.error as e:
#     str(e)

# s.listen(2) 
# print("Waiting for a connection, server started")

# # Threaded function
# def threaded_client(conn):
#     reply = ""
#     while True:
#         try:
#             data = conn.recv(2048)
#             reply = data.decode("utf-8")

#             if not data:
#                 print("Disconnected")
#                 break
#             else:
#                 print("Received: ", reply)
#                 print("Sending: ", reply)
            
#             conn.sendall(str.encode(reply))
#         except:
#             break

# # Continously look for connections
# while True:
#     conn, addr = s.accept()
#     print("Connected to: ", addr)

#     # starts new thread
#     start_new_thread(threaded_client, (conn,))