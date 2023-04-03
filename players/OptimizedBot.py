import numpy as np
import random
from copy import deepcopy

from players.BasePlayer import BasePlayer


class OptimizedBot(BasePlayer):
    def __init__(self, verbose, weights=(0.25648373, -0.31488939, -0.12317508, 0.48541348)):
        super().__init__(verbose)

        # weights of heuristic score components, values <-1.0, 1.0>
        # weights[0] - available area (positive = agoraphillic bot; negative = agoraphobic bot)
        # weights[1] - manhattan distance (positive = aggressive bot; negative = elusive bot)
        # weights[2] - head-on collision eagerness (positive = evasive; negative = ballsy)
        # weights[3] - preference to continue movement (positive = likes straight lines; negative = likes turns)
        # RandomBot is equivalent to OptimizedBot(weights=[0.0, 0.0, 0.0, 0.0])
        # HeuristicBot is equivalent to OptimizedBot(weights=[1.0, 1.0, 1.0, 0.0])
        self.previous_move = None
        expected_num_weights = 4
        if len(weights) == expected_num_weights:
            self.weights = weights
        else:
            raise ValueError(f'Wrong number of weights: {len(weights)} (should be {expected_num_weights}).')

    def __str__(self):
        return super().__str__() + f' {self.weights}'

    def evaluate_move(self, game_matrix, move_offset, my_coords, opponent_coords, continued_move):
        available_area = self.calculate_available_area(deepcopy(game_matrix),
                                                       (my_coords[0] + move_offset[0], my_coords[1] + move_offset[1]))
        manhattan_distance = self.calculate_manhattan_distance(move_offset, my_coords, opponent_coords)
        continued_movement_factor = (1.0 + self.weights[3]) if continued_move else (1.0 - self.weights[3])
        if manhattan_distance == 1:
            # 'enemy too close'-case: decrease score if the enemy is 1 tile away from the target tile
            return (available_area * self.weights[0] - 5.0 * self.weights[2]) * continued_movement_factor
        else:
            return (available_area * self.weights[0] - manhattan_distance * self.weights[1]) * continued_movement_factor

    def get_move(self, game_matrix, possible_moves, my_coords, opponent_coords):
        # similar to HeuristicBot but the heuristic score is weighted (and the weights can be optimized separately)
        # in case of a tie: choose randomly
        best_move = list(possible_moves.keys())[0]
        best_score = self.evaluate_move(game_matrix, possible_moves[best_move], my_coords, opponent_coords,
                                        continued_move=(self.previous_move == best_move))

        for move in list(possible_moves.keys())[1:]:
            score = self.evaluate_move(game_matrix, possible_moves[move], my_coords, opponent_coords,
                                       continued_move=(self.previous_move == move))
            if score > best_score:
                best_move = move
            elif score == best_score:
                best_move = random.choice([best_move, move])

        if self.verbose:
            print(f'{self} selects move "{best_move}" based on score: {np.round(best_score, 2)}', flush=True)
        self.previous_move = best_move
        return best_move
