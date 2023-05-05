import numpy as np
import random
from stable_baselines3 import PPO

from players.BasePlayer import BasePlayer


class ReinforcementLearningBot(BasePlayer):
    def __init__(self, verbose, model_name='players/PPO15v1'):
        super().__init__(verbose)
        self.model = PPO.load(model_name)
        self.action_map = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}

    def get_move(self, game_matrix, possible_moves, my_coords, opponent_coords):
        player_number = abs(game_matrix[my_coords])
        matrix_map = {0: 0, 1: 1, 2: 1,
                      -1: 2 if player_number == 1 else 3,
                      -2: 2 if player_number == 2 else 3}
        # translate game_matrix values to player_number-irrelevant generalisation
        # 0: empty, 1: any tail, 2: player head, 3: enemy head
        translated_game_matrix = np.vectorize(matrix_map.get)(game_matrix)

        action, _states = self.model.predict(translated_game_matrix)
        move = self.action_map[int(action)]
        if move in possible_moves.keys():
            if self.verbose:
                print(f'{self} selects possible move "{move}"', flush=True)
            return move
        else:
            # handle impossible moves by selecting random possible move
            random_move = random.choice(list(possible_moves.keys()))
            if self.verbose:
                print(f'{self} selected impossible move "{move}", so "{random_move}" was selected randomly instead', flush=True)
            return random_move
