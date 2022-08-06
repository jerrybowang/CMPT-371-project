from random import seed
from random import randint
import random
import time

# seed random number generator
seed(1)


HEADER = 2048
PORT = 5555
FORMAT = 'utf-8'
END = "end"
Pressed = "Pressed"
player_num = "player#"
IP_and_Port = "IPandPort"
player_color = "player_colour"
player_turn = "player_turn"
display = "display"
remote = "remote_press"

number_bombs = randint(40, 100)


# We have a players dictionary in the following format

# {1: True, 2: False}
# True: means player is still alive
# False: means player is died

# Connections

# {1: conn, 2: conn }

class Game:
    def __init__(self):
        self.bomb_list = []
        self.connections = []
        # List of ids of the players that have been connected to the game
        self.player_ids = dict()
        self.colors = set()
        self.hex_colors = []
        self.max_connections = None
        self.player_id_turn = -1
        self.number_player_alive = None
        self.game_done = False
        self.bomb_color = '#ff0000'
# initialize the board and populate the bombs
    def init_board_game(self):
        rgb = 255, 0, 0
        self.colors.add(rgb)

        for i in range(self.max_connections):
            self.player_ids[i + 1] = True

        while len(self.bomb_list) < 10:
            n = random.randint(1, 256)
            if n in self.bomb_list:
                continue
            self.bomb_list.append(n)

    # Set the maximum number of connections that is connected to the server
    def set_max_connections(self, max_connection):
        self.max_connections = max_connection
        self.number_player_alive = max_connection

    # Generate a random RGB color
    def generate_random_rgb(self):
        generated = False
        while not generated:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            rgb_v = r, g, b

            if rgb_v in self.colors:
                continue

            self.colors.add(rgb_v)
            self.hex_colors.append(self.rgb_to_hex(r, g, b))
            print("RGB" + str(r) + str(g) + str(b))
            generated = True

    def rgb_to_hex(self, r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    # Generate unique color for each player with the help of generate_random_rgb fucntion
    def generate_color_player(self):
        self.generate_random_rgb()


    def send_player_died(self, conn):
        display_message = 'display "You died"'
        conn.sendall(display_message.encode(FORMAT))
        time.sleep(0.1)
        end_message = "end"
        conn.sendall(end_message.encode((FORMAT)))

    def send_player_won(self):
        for i in range(self.max_connections):
            if self.player_ids[i + 1] == True:
                winning_message = 'display "You Won"'
                self.connections[i][0].sendall(winning_message.encode((FORMAT)))
                time.sleep(0.1)
                self.connections[i][0].sendall("end".encode((FORMAT)))
                self.game_done = True


    def add_connections(self, conn, add):
        self.connections.append((conn, add))

    # Give player turn based on particular order
    def player_turn(self):
        
        if self.player_id_turn == -1:
            self.player_id_turn = 1
        else:
            generated_live_player = False
            player_id = self.player_id_turn
            while not generated_live_player:
                player_id += 1
                if player_id > self.max_connections:
                    player_id = 1
                self.player_id_turn = player_id
                if self.player_ids[self.player_id_turn] == False:
                    continue
                else:
                    generated_live_player = True

    def read_message(msg):
        msg = msg.split(",")
        return msg

    # A handler which can handle different messages sent by the client
    def handle_messages(self, msg, conn, addr, player_number):
        time.sleep(0.1)
        if msg == END:
            print("we will send die message !")
            self.send_player_died(conn)

        #   Broadcase a remote message to clients telling them a player has pressed a button and the color of the button
        if msg[0] == remote:
            button_number = int(msg[2])
            message = "remote_press " + msg[2] + " "
            if button_number in self.bomb_list:
                message += self.bomb_color
            else:
                message += self.hex_colors[player_number - 1]

            for index in range(len(self.connections)):
                if self.player_ids[index + 1] == True:
                    self.connections[index][0].sendall(message.encode((FORMAT)))
                else:
                   continue

        # Send a display message to client 
        if msg == display:
            self.send_player_won()

        # Send a player color to the client 
        if msg == player_color:
            message_color = "player_colour " + \
                            self.hex_colors[player_number - 1]
            print(self.hex_colors[player_number - 1])
            conn.sendall(message_color.encode((FORMAT)))

        # Telling clients which player's turn is it right now
        if msg == player_turn:
            message_turn = "player_turn " + str(self.player_id_turn)
            for index in range(len(self.connections)):
                if self.player_ids[index + 1] == True:
                    self.connections[index][0].sendall(message_turn.encode((FORMAT)))
                else:
                    continue
        
        # Telling client its player number
        if msg == player_num:
            player_number = str(player_number)
            player_number = "player# " + player_number
            conn.sendall(player_number.encode((FORMAT)))
        
        if msg == IP_and_Port:
            address = (str(addr))
            address = "IP and port is: " + address
            print(f"[{addr}] {msg}")
            conn.sendall(address.encode((FORMAT)))

    def check_player_won(self):
        
        if len(self.bomb_list) == 0 or self.number_player_alive <= 1:
            return True
        else:
            return False

    def check_player_died(self, button_number, player_number):
        if button_number in self.bomb_list:
            self.player_ids[player_number] = False
            print("PLAYER DIED")
            self.number_player_alive -= 1
            self.bomb_list.remove(button_number)
            return True
        else:
            return False
