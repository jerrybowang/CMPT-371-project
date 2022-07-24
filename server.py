from tkinter import Button
from game import Game
import socket
import threading
import time
import sys
import pygame
import random

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

# Global variable
my_game = Game()
my_game.init_board_game()

threads = []

bomb_list = []
for i in range(1,16): # choose 16 random numbers to be bombs
    n = random.randint(1, 256)
    bomb_list.append(n)

def process_client(conn, addr, player_number):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    my_game.handle_messages("player#", conn, addr, player_number)
    my_game.generate_color_player()
    my_game.handle_messages("player_colour", conn, addr, player_number)
    print("Player turn: " + str(my_game.player_id_turn))

    while connected:
        # msg_len = conn.recv(HEADER).decode(FORMAT)

        # if msg_len:
        #     msg_len = int(msg_len)
        #     msg = conn.recv(msg_len).decode(FORMAT)
        #     command = msg.split()
        #     print("msg is",  msg)
        #     if command[0] == END:
        #         # if player wants to end the game
        #         connected = False
        #     if command[0] == Pressed:
        #         player_id = command[1]
        #         button_id = command[2]
        #         # for testing
        #         # two_ids = player_id + " " + button_id
        #         # print("two_ids is ", two_ids)
        #         # conn.send(two_ids.encode((FORMAT)))
        #     if command[0] == player_num:
        #         player_number = str(player_number)
        #         player_number = "player# " + player_number
        #         conn.send(player_number.encode((FORMAT)))
        #     if command[0] == IP_and_Port:
        #         address = (str(addr))
        #         address = "IP and port is: " + address
        #         print(f"[{addr}] {msg}")
        #         conn.send(address.encode((FORMAT)))

        if my_game.player_id_turn == player_number:

            data = conn.recv(HEADER)
            msg = data.decode(FORMAT)

            if data:
                msg = msg.split(" ")
                button_number = int(msg[2])
                if msg[0] == Pressed:
                    msg[0] = "remote_press"
                    my_game.handle_messages(msg, conn, addr, player_number)
            

                    # CASE: when the player has died
                    if check_player_died(button_number):
                    #   my_game.handle_messages("end", conn, addr, player_number)
                        connected = False

                    # CASE: when the player has won
                    if check_player_won():
                    #   my_game.handle_messages("display", conn, addr, player_number)
                        connected = False

                # if check_player_won():
                #   connected = False

            # Give chance to the next player
            my_game.player_turn()
            my_game.handle_messages("player_turn", conn, addr, player_number)

        else:
            continue

    conn.close()

def check_player_died(button_number):
    if button_number in bomb_list:
        print("PLAYER DIED")
        player_num -= 1
        return True
    else:
        return False

def check_player_won():
    if player_num <= 1:
        return True
    else:
        return False

def wait_clients_finish():
    for index in range(len(threads)):
        threads[index].join()

def start():
    player_number = 0

    max_connections = int(input("Enter a number: "))
    my_game.set_max_connections(max_connections)
    # Determine whose turn is it
    my_game.player_turn()
    server.listen()
    run = True

    print(f"[LISTENING] Server is listing on {SERVER}")
    while run:
        conn, addr = server.accept()
        # the maximum player
        if len(my_game.connections) >= max_connections:
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
        threads.append(thread)
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}")
        if len(my_game.connections) == max_connections:
            my_game.handle_messages("player_turn", conn, addr, player_number)
            wait_clients_finish()
            run = False

    

print("Please enter maximum player number for current game")
start()


        



