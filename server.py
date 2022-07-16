

import socket
import threading
import time
import sys
import pygame
from game import Game



HEADER = 2048
PORT = 5555  # port number
SERVER = socket.gethostbyname(socket.gethostname())  # get local host IP
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
END = "end"
Pressed = "pressed"
player_num = "player#"
IP_and_Port = "IPandPort"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP connection
server.bind(ADDR)  # Binds server to port


connections = []
# Global variable
my_game = Game()
my_game.init_board_game()


def process_client(conn, addr, player_number):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:

        my_game.handle_messages("player#", conn, addr, player_number)
        my_game.generate_color_player()
        my_game.handle_messages("player_colour", conn, addr, player_number)
        
        data = conn.recv(HEADER)
        msg = data.decode(FORMAT)

        if data:
            msg = msg.split(" ")
            if msg[0] == Pressed:
                msg[0] = "remote_press"
                my_game.handle_messages(msg, conn, addr, player_number)

            # CASE: when the player has died
            # if check_player_died():
            #   my_game.handle_messages("end", conn, addr, player_number)
            #   connected = False
            
            # CASE: when the player has won
            # if check_player_won():
            #   my_game.handle_messages("display", conn, addr, player_number)
            #   connected = False


    conn.close()


def start():
    player_number = 0
    
    

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
        my_game.add_connections(conn, addr)

        player_number += 1
        my_game.add_player(player_number)
        # Threaded function
        thread = threading.Thread(
            target=process_client, args=(conn, addr, player_number))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}")


print("Please enter maximum player number for current game")
start()








































