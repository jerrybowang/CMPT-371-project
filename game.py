class Game:
    def __init__(self, id):
        # self.p1Went = False
        # self.p2Went = False
        # self.ready = False
        # self.id = id
        # self.moves = [None, None]
        # self.wins = [0, 0]
        # self.ties = 0

    
    def bombs(self):
        pass

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    # Whoes turn is to play
    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def game_mechanic(self):

        

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
