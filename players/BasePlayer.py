import numpy as np


class BasePlayer:
    def __init__(self, verbose):
        self.verbose = verbose

    def __str__(self):
        return self.__class__.__name__

    def calculate_available_area(self, game_matrix, position):
        # recursive function
        # tile has 0 area if it is outside the game matrix or has non-zero value
        if not (game_matrix.shape[0]-1 >= position[0] >= 0 and game_matrix.shape[1]-1 >= position[1] >= 0) \
                or game_matrix[position[0], position[1]] != 0:
            return 0
        else:
            game_matrix[position[0], position[1]] = 1234
            return 1 + sum([self.calculate_available_area(game_matrix, (position[0] + move[0], position[1] + move[1]))
                            for move in [(-1, 0), (1, 0), (0, -1), (0, 1)]])

    def calculate_manhattan_distance(self, move_offset, my_coords, opponent_coords):
        return np.sum([np.abs(my_coords[i] + move_offset[i] - opponent_coords[i]) for i in (0, 1)])

    def get_move(self, game_matrix, possible_moves, my_coords, opponent_coords):
        pass
