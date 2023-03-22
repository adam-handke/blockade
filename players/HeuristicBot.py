import random
from copy import deepcopy

from players.BasePlayer import BasePlayer


class HeuristicBot(BasePlayer):
    def evaluate_move(self, game_matrix, move_offset, my_coords, opponent_coords):
        available_area = self.calculate_available_area(deepcopy(game_matrix),
                                                       (my_coords[0] + move_offset[0], my_coords[1] + move_offset[1]))
        manhattan_distance = self.calculate_manhattan_distance(move_offset, my_coords, opponent_coords)
        if manhattan_distance == 1:
            # 'enemy too close'-case: decrease score if the enemy is 1 tile away from the target tile
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
            print(f'{self} selects move "{best_move}" based on score: {best_score}', flush=True)
        return best_move
