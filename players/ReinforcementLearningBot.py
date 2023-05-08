import numpy as np
import random
from stable_baselines3 import PPO, A2C, DQN

from players.BasePlayer import BasePlayer


class ReinforcementLearningBot(BasePlayer):
    def __init__(self, verbose, model_name='players/A2C15v2', model_type='a2c', model_size=15):
        super().__init__(verbose)
        self.model_name = model_name
        if model_type == 'ppo':
            self.model = PPO.load(model_name)
        elif model_type == 'a2c':
            self.model = A2C.load(model_name)
        elif model_type == 'dqn':
            self.model = DQN.load(model_name)
        else:
            raise ValueError(f'{self}: unknown model_type: {model_type}')
        self.action_map = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}
        self.model_size = model_size
        
    def __str__(self):
        return super().__str__() + f' ({self.model_name[-7:]})'

    def get_move(self, game_matrix, possible_moves, my_coords, opponent_coords):
        player_number = int(abs(game_matrix[my_coords]))
        matrix_map = {0: 0, -1: 1, -2: 1,
                      1: 2 if player_number == 1 else 3,
                      2: 2 if player_number == 2 else 3}
        # translate game_matrix values to player_number-irrelevant generalisation
        # 0: empty, 1: any tail, 2: player head, 3: enemy head
        translated_game_matrix = np.vectorize(matrix_map.get)(game_matrix)

        # enable game arenas different than self.model_size
        if game_matrix.shape[0] < self.model_size:
            diff = self.model_size - game_matrix.shape[0]
            padding1 = diff // 2
            padding2 = (diff // 2) if (diff % 2 == 0) else (diff // 2 + 1)
            observation = np.pad(translated_game_matrix, ((padding1, padding2), (padding1, padding2)), 
                                 'constant', constant_values=1)
        elif game_matrix.shape[0] > self.model_size:
            upper_border = min(max(0, int(my_coords[0])-self.model_size//2), game_matrix.shape[0]-self.model_size)
            left_border = min(max(0, int(my_coords[1])-self.model_size//2), game_matrix.shape[1]-self.model_size)
            observation = translated_game_matrix[upper_border:(upper_border+self.model_size), left_border:(left_border+self.model_size)]
        else:
            observation = translated_game_matrix

        action, _states = self.model.predict(observation)
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
