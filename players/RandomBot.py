import random

from players.BasePlayer import BasePlayer


class RandomBot(BasePlayer):

    def get_move(self, game_matrix, possible_moves):
        super().get_move(game_matrix, possible_moves)

        return random.choice(possible_moves)
