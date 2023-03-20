import random

from players.BasePlayer import BasePlayer


class RandomBot(BasePlayer):
    def get_move(self, game_matrix, possible_moves, my_coords, opponent_coords):
        return random.choice(list(possible_moves.keys()))
