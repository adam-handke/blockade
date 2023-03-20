class BasePlayer:
    def __init__(self, verbose):
        self.verbose = verbose

    def __str__(self):
        return self.__class__.__name__

    def get_move(self, game_matrix, possible_moves, my_coords, opponent_coords):
        pass
