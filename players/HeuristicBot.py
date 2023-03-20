import random
import numpy as np
from copy import deepcopy

from players.BasePlayer import BasePlayer


class HeuristicBot(BasePlayer):
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

    def evaluate_move(self, game_matrix, move_offset, my_coords, opponent_coords):
        available_area = self.calculate_available_area(deepcopy(game_matrix),
                                                       (my_coords[0] + move_offset[0], my_coords[1] + move_offset[1]))
        manhattan_distance = np.sum([np.abs(my_coords[i] + move_offset[i] - opponent_coords[i]) for i in (0, 1)])
        # 'enemy too close'-case: decrease score if the enemy is 1 tile away from the target tile
        if manhattan_distance == 1:
            return available_area - 5
        else:
            return available_area - manhattan_distance

    def get_move(self, game_matrix, possible_moves, my_coords, opponent_coords):
        # select the move with the largest available area and the shortest distance to the opponent
        # in case of a tie: choose randomly
        best_move = list(possible_moves.keys())[0]
        best_score = self.evaluate_move(game_matrix, possible_moves[best_move], my_coords, opponent_coords)

        for move in list(possible_moves.keys())[1:]:
            score = self.evaluate_move(game_matrix, possible_moves[move], my_coords, opponent_coords)
            if score > best_score:
                best_move = move
            elif score == best_score:
                best_move = random.choice([best_move, move])

        if self.verbose:
            print(f'{self} selects move "{best_move}" based on score: {best_score}')
        return best_move
