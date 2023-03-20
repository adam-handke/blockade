import random
import numpy as np

from players.BasePlayer import BasePlayer


class HeuristicBot(BasePlayer):
    def evaluate_move(self, move_offset, my_coords, opponent_coords):
        # Manhattan distance
        return np.sum([np.abs(my_coords[i] + move_offset[i] - opponent_coords[i]) for i in (0, 1)])

    def get_move(self, game_matrix, possible_moves, my_coords, opponent_coords):
        # select the move with the shortest distance to the opponent; in case of a tie: choose randomly
        best_move = list(possible_moves.keys())[0]
        best_score = self.evaluate_move(possible_moves[best_move], my_coords, opponent_coords)

        for move in list(possible_moves.keys())[1:]:
            score = self.evaluate_move(possible_moves[move], my_coords, opponent_coords)
            if score < best_score:
                best_move = move
            elif score == best_score:
                best_move = random.choice([best_move, move])

        if self.verbose:
            print(f'{self} selects: {best_move} based on score: {np.round(best_score, 2)}')
        return best_move
