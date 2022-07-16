# generate random integer values
from random import seed
from random import randint
import random
# seed random number generator
seed(1)


number_bombs = randint(0, 10)
class Game:
    def __init__(self):
        self.board = None
        self.row = 16
        self.column = 16
        self.winner = -1
        self.bombs_positions = set()
        # List of ids of the players that have been connected to the game
        self.ids = []
        self. colors = set()


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
        while not generated:
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            rgb_v = r, g, b

            if rgb_v in self.colors:
                continue
            self.colors.add(rgb_v)
            generated = True

        


            

    def rgb_to_hex(rgb):
        return '#%02x%02x%02x'  # rgb



    def get_player_move(self, p):
        pass

    
    # Whoes turn is to play
    def play(self, player, move):
        pass

    def connected(self):
        return self.ready

    def game_mechanic(self):
        pass

        

    def resetWent(self):
       pass