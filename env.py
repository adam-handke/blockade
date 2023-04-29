import numpy as np
import functools
import gymnasium
import pettingzoo


class BlockadeEnv(pettingzoo.ParallelEnv):
    # Blockade environment only for training RL bots
    # based on: https://pettingzoo.farama.org/content/environment_creation/#example-custom-parallel-environment

    def __init__(self, arena_size, verbose):
        self.arena_size = arena_size
        self.verbose = verbose
        self.game_matrix = np.zeros((self.arena_size, self.arena_size), dtype=int)
        self.starting_position = int(self.arena_size / 4)
        self.game_matrix[self.arena_size - self.starting_position - 1, self.arena_size - self.starting_position - 1] = 1
        self.game_matrix[self.starting_position, self.starting_position] = 2
        self.move_dict = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        self.move_counter = 0
        self.max_number_of_moves = int(np.ceil(self.arena_size ** 2 / 2.0) - 2)

        self.action_map = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}
        self.possible_agents = ["player" + str(r) for r in [1, 2]]
        self.agent_name_mapping = dict(zip(self.possible_agents, list(range(len(self.possible_agents)))))

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return gymnasium.spaces.Box(low=0, high=3, shape=(self.arena_size, self.arena_size), dtype=np.integer)

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return gymnasium.spaces.Discrete(4)

    def reset(self, seed=None, return_info=False, options=None):
        self.game_matrix = np.zeros((self.arena_size, self.arena_size), dtype=int)
        self.game_matrix[self.arena_size - self.starting_position - 1, self.arena_size - self.starting_position - 1] = 1
        self.game_matrix[self.starting_position, self.starting_position] = 2
        self.move_counter = 0

        self.agents = self.possible_agents[:]
        observations = {agent: self.next_observation(i+1) for i, agent in enumerate(self.agents)}
        return observations

    def next_observation(self, player_number):
        matrix_map = {0: 0, 1: 1, 2: 1,
                      -1: 2 if player_number == 1 else 3,
                      -2: 2 if player_number == 2 else 3}
        # translate game_matrix values to player_number-irrelevant generalisation
        # 0: empty, 1: any tail, 2: player head, 3: enemy head
        return np.vectorize(matrix_map.get)(self.game_matrix)

    def step(self, actions):
        # TODO
        pass

