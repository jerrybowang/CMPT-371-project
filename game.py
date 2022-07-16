# generate random integer values
from random import seed
from random import randint
import random
# seed random number generator
seed(1)

# Will be changed
HEADER = 2048
PORT = 5555
FORMAT = 'utf-8'
END = "end"
Pressed = "Pressed"

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
        # List of ids of the players that have been connected to the game
        self.player_ids = dict()
        self.colors = set()
        
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

            
    def generate_random_rgb(self):
        generated = False
        generated_rgb = None
        while not generated:
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            rgb_v = r, g, b

            if rgb_v in self.colors:
                continue

            self.colors.add(rgb_v)
            generated_rgb = rgb_v
            generated = True

        return generated_rgb

    def rgb_to_hex(rgb):
        return '#%02x%02x%02x'  # hex

    def add_player(self, id):
        self.player_ids[id] = True 

    def generate_color_player(self):
        rgb_color = self.generate_random_rgb()
        hex = self.rgb_to_hex(rgb_color)
        return hex

    def send_player_died(self, id, conn):
        # Make sure player is dead
        if self.player_ids[id] == False:
            end_message = "end"
            conn.send(end_message.encode((FORMAT)))

        return False # Failure

    def send_player_won(self, id, conn):
        # number_of_trues = 0
        # for key, value in self.player_ids.items():
            #if value == true
                #number_of_trues+=1

         if self.player_ids[id] == True:
            winning_message = "you_won"
            conn.send(winning_message.encode((FORMAT)))



    def player_turn(self):
        player_id = random.randint(1, len(self.player_ids)) # Generate a random number from 1 to how many players we have in dictionary
        return player_id


    # def bombs(self):
    #     for i in range(1,number_bombs): # choose number_bombs random numbers to be bombs
    #         n = random.randint(1,256) # total of 256 numbers
    #         self.bomb_list.append(number_bombs)
      

    def handle_different_messages():


    def game_won(self):
        pass

    def game_lost(self):
        pass