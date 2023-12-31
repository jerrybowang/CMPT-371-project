# imports 
from game import Game
import socket
import threading
import time
import sys
import random

HEADER = 2048
PORT = 5555  # port number

# host_name = socket.gethostname()
# SERVER = socket.gethostbyname(host_name) # get local host IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
SERVER = s.getsockname()[0]  # get local host IP
s.close()

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
Pressed = "pressed"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP connection
server.bind(ADDR)  # Binds server to port

# Global variable
my_game = Game()

threads = []

mutex = threading.Lock()
# critical recourse
ready_client = 0


def update_ready():
    global ready_client
    global mutex
    mutex.acquire()
    ready_client += 1
    mutex.release()


# receives messaging from client and determines if player (client) dies (then closes the connection)
def process_client(conn, addr, player_number):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    my_game.handle_messages("player#", conn, addr, player_number)
    # time.sleep(0.1)
    my_game.generate_color_player()
    my_game.handle_messages("player_colour", conn, addr, player_number)
    print("Player turn: " + str(my_game.player_id_turn))
    # finished set up, update ready number
    update_ready()

    while connected:
        if my_game.game_done == True:
            break
        if my_game.player_id_turn == player_number and len(my_game.connections) == my_game.max_connections:

            data = conn.recv(HEADER)
            msg = data.decode(FORMAT)

            if data:
                msg = msg.split(" ")
                button_number = int(msg[2])
                if msg[0] == Pressed:
                    msg[0] = "remote_press"
                    my_game.handle_messages(msg, conn, addr, player_number)

                    # CASE: when the player has died
                    if my_game.check_player_died(button_number, player_number):
                        my_game.handle_messages("end", conn, addr, player_number)
                        print("Died message sent!")
                        connected = False

                    # CASE: when the player has won
                    if my_game.check_player_won():
                        my_game.handle_messages("display", conn, addr, player_number)
                        # print(f"Player {msg[1]} is winner")
                        connected = False

            # Give chance to the next player
            if my_game.check_player_won() == False:
                my_game.player_turn()
                my_game.handle_messages("player_turn", conn, addr, player_number)

        else:
            continue

    conn.close()


# assigns each client to seperate thread
def wait_clients_finish():
    for index in range(len(threads)):
        threads[index].join()


# prompts user to enter number of players and displays address and port info
def start():
    player_number = 0

    max_connections = int(input("Enter a number: "))
    my_game.set_max_connections(max_connections)
    my_game.init_board_game()

    # Determine whose turn is it
    my_game.player_turn()
    server.listen()
    run = True

    print(f"[LISTENING] Server is listing on {SERVER} and port {PORT}")
    while run:
        conn, addr = server.accept()
        # the maximum player
        if len(my_game.connections) >= max_connections:
            conn.sendall(
                f"Connection overflow. Max amount is {max_connections}".encode())
            continue

        my_game.add_connections(conn, addr)

        player_number += 1

        # Threaded function

        thread = threading.Thread(
            target=process_client, args=(conn, addr, player_number))
        thread.start()
        threads.append(thread)
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}")
        if len(my_game.connections) == max_connections:
            # spinlock, wait until ALL clients are ready
            while ready_client != max_connections:
                time.sleep(1)

            time.sleep(0.1)
            my_game.handle_messages("player_turn", conn, addr, player_number)
            wait_clients_finish()
            run = False


print("Please enter maximum player number for current game")
start()
