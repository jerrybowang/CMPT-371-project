import socket
import threading
import time
import sys
import pygame


HEADER = 2048
PORT = 5555 # port number
SERVER = socket.gethostbyname(socket.gethostname()) # get local host IP
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
END = "end"
Pressed = "pressed"
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
            command = msg.split()
            print("msg is",  msg)
            if command[0] == END:
                # if player wants to end the game
                connected = False
            if command[0] == Pressed:
                player_id = command[1]
                button_id = command[2]
                # for testing
                # two_ids = player_id + " " + button_id
                # print("two_ids is ", two_ids)
                # conn.send(two_ids.encode((FORMAT)))
            if command[0] == player_num:
                player_number = str(player_number)
                player_number = "player# " + player_number
                conn.send(player_number.encode((FORMAT)))
            if command[0] == IP_and_Port:
                address = (str(addr))
                address = "IP and port is: " + address
                print(f"[{addr}] {msg}")
                conn.send(address.encode((FORMAT)))

    conn.close()


def start():
    player_number =0
    connections = []
    max_connections = int(input("Enter a number: "))
    server.listen()
    print(f"[LISTENING] Server is listing on {SERVER}")
    while True:
        conn, addr = server.accept()
        # the maximum player
        if len(connections) >= max_connections:
            conn.sendall(f"Connection overflow. Max amount is {max_connections}".encode())
            continue
        connections.append((conn, addr))
        player_number += 1
        # Threaded function
        thread = threading.Thread(target=process_client, args=(conn, addr, player_number))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}")


print("Please enter maximum player number for current game")
start()
