# generate random integer values
from random import seed
from random import randint
import random
import re
# seed random number generator
seed(1)

# Will be changed
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

number_bombs = randint(0, 16)


# We have a players dictionary in the following format

# {1: True, 2: False}
# True: means player is still alive
# False: means player is died

# Connections

# {1: conn, 2: conn }

class Game:
    def __init__(self):
        self.board = None
        self.row = 16
        self.column = 16
        self.bomb_list = []
        self.bombs_positions = set()
        self.connections = []
        # List of ids of the players that have been connected to the game
        self.player_ids = dict()
        self.colors = set()
        self.hex_colors = []
        self.max_connections = None
        self.player_id_turn = None
        #self.connections = dict() If we need it

    def init_board_game(self):
        self.board = [[0 for _ in range(self.column)] for _ in range(self.row)]

        while len(self.bombs_positions) < number_bombs:
            # Implementation details

            # random_row = random.randrange(0,self.row)
            # random_column = random.randrange(0,cols)
            # pos = random_row, random_column

            # if pos in self.bombs_positions:
            #     continue
            # self.bombs_positions.add(pos)
            # self.board[random_row][random_column] = 1

            return 1

    def set_max_connections(self, max_connection):
        self.max_connections = max_connection

    def generate_random_rgb(self):
        generated = False
        generated_rgb = None
        while not generated:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            rgb_v = r, g, b

            if rgb_v in self.colors:
                continue

            self.colors.add(rgb_v)
            generated_rgb = rgb_v
            self.hex_colors.append(self.rgb_to_hex(r,g,b))
            generated = True

        

    def rgb_to_hex(self, r, g, b):
        return ('#{:X}{:X}{:X}').format(r, g, b)

    def add_player(self, id):
        self.player_ids[id] = True

    def generate_color_player(self):
        self.generate_random_rgb()

    def send_player_died(self, id, conn):
        # Make sure player is dead
        if self.player_ids[id] == False:
            end_message = "end"
            conn.send(end_message.encode((FORMAT)))

        return False  # Failure

    def send_player_won(self, id, conn):
        # number_of_trues = 0
        # for key, value in self.player_ids.items():
        #if value == true
        #number_of_trues+=1

        if self.player_ids[id] == True:
            winning_message = 'display "You Won"'
            conn.send(winning_message.encode((FORMAT)))

    def add_connections(self, conn, add):
        self.connections.append((conn, add))

    def player_turn(self):
        # Generate a random number from 1 to how many players we have in dictionary
        player_id = random.randint(1, self.max_connections)
        self.player_id_turn = player_id

    def read_message(msg):
        msg = msg.split(",")
        return msg

    # def bombs(self):
    #     for i in range(1,number_bombs): # choose number_bombs random numbers to be bombs
    #         n = random.randint(1,256) # total of 256 numbers
    #         self.bomb_list.append(number_bombs)

    # Pressed Button needs to be added

    def handle_messages(self, msg, conn, addr, player_number):
        if msg == END:
            self.send_player_died(player_number, conn)

        if msg[0] == remote:
            message = "remote_press " + \
                msg[2] + " " + self.hex_colors[player_number-1]

            for index in range(len(self.connections)):
                self.connections[index][0].send(message.encode((FORMAT)))

        if msg == display:
            self.send_player_won(player_number, conn)

        if msg == player_color:
            message_color = "player_color " + \
                self.hex_colors[player_number-1]
            print(self.hex_colors[player_number-1])
            conn.sendall(message_color.encode((FORMAT)))

        if msg == player_turn:
            message_turn = "player_turn " + str(self.player_id_turn)
            conn.sendall(message_turn.encode((FORMAT)))

        if msg == player_num:
            player_number = str(player_number)
            player_number = "player# " + player_number
            conn.sendall(player_number.encode((FORMAT)))

        if msg == IP_and_Port:
            address = (str(addr))
            address = "IP and port is: " + address
            print(f"[{addr}] {msg}")
            conn.send(address.encode((FORMAT)))

    def game_won(self):
        pass

    def game_lost(self):
        pass
