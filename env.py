import numpy as np
import functools
from gymnasium.spaces import Box, Discrete
from pettingzoo import ParallelEnv


class BlockadeEnv(ParallelEnv):
    # Blockade environment only for training RL bots
    # based on: https://pettingzoo.farama.org/content/environment_creation/#example-custom-parallel-environment
    metadata = {'render_mode': None, 'name': 'blockade'}

    def __init__(self, arena_size):
        self.arena_size = arena_size
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
        return Box(low=0, high=3, shape=(self.arena_size, self.arena_size), dtype=np.int32)

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return Discrete(4)

    def reset(self, seed=None, return_info=False, options=None):
        self.game_matrix = np.zeros((self.arena_size, self.arena_size), dtype=int)
        self.game_matrix[self.arena_size - self.starting_position - 1, self.arena_size - self.starting_position - 1] = 1
        self.game_matrix[self.starting_position, self.starting_position] = 2
        self.move_counter = 0

        self.agents = self.possible_agents[:]
        observations = {agent: self.next_observation(i+1) for i, agent in enumerate(self.agents)}
        return observations

    def next_observation(self, player_number):
        matrix_map = {0: 0, -1: 1, -2: 1,
                      1: 2 if player_number == 1 else 3,
                      2: 2 if player_number == 2 else 3}
        # translate game_matrix values to player_number-irrelevant generalisation
        # 0: empty, 1: any tail, 2: player head, 3: enemy head
        return np.vectorize(matrix_map.get)(self.game_matrix)

    def check_possible_move(self, head, move):
        if len(head[0]) == 0 or len(head[1]) == 0:
            return False
        elif self.game_matrix.shape[0] - 1 >= head[0] + self.move_dict[move][0] >= 0 \
                and self.game_matrix.shape[1] - 1 >= head[1] + self.move_dict[move][1] >= 0 \
                and self.game_matrix[head[0] + self.move_dict[move][0], head[1] + self.move_dict[move][1]] == 0:
            return True
        else:
            return False

    def step(self, actions):
        # takes actions and returns observations, rewards, terminations, truncations and infos for each agent

        if not actions:
            self.agents = []
            return {}, {}, {}, {}, {}

        # update player1
        p1_state = None
        p1_head = np.where(self.game_matrix == 1)
        self.game_matrix[p1_head[0], p1_head[1]] = -1
        if self.check_possible_move(p1_head, self.action_map[actions[self.agents[0]]]):
            self.game_matrix[p1_head[0] + self.move_dict[self.action_map[actions[self.agents[0]]]][0],
                             p1_head[1] + self.move_dict[self.action_map[actions[self.agents[0]]]][1]] = 1
        else:
            p1_state = 'lost'

        # update player2
        p2_state = None
        p2_head = np.where(self.game_matrix == 2)
        self.game_matrix[p2_head[0], p2_head[1]] = -2
        if self.check_possible_move(p2_head, self.action_map[actions[self.agents[1]]]):
            self.game_matrix[p2_head[0] + self.move_dict[self.action_map[actions[self.agents[1]]]][0],
                             p2_head[1] + self.move_dict[self.action_map[actions[self.agents[1]]]][1]] = 2
        else:
            p2_state = 'lost'

        # reward calculation
        rewards = {}
        if p1_state == 'lost' and p2_state is None:
            # p1 lost
            rewards[self.agents[0]], rewards[self.agents[1]] = (-100, 100)
        elif p1_state is None and p2_state == 'lost':
            # p2 lost
            rewards[self.agents[0]], rewards[self.agents[1]] = (100, -100)
        elif p1_state == 'lost' and p2_state == 'lost':
            # tie
            rewards[self.agents[0]], rewards[self.agents[1]] = (-10, -10)
        else:
            # game continues
            rewards[self.agents[0]], rewards[self.agents[1]] = (1, 1)

        # terminations
        if p1_state == 'lost' or p2_state == 'lost':
            terminations = {agent: True for agent in self.agents}
        else:
            terminations = {agent: False for agent in self.agents}

        # truncations
        self.move_counter += 1
        if self.move_counter > self.max_number_of_moves:
            truncations = {agent: True for agent in self.agents}
        else:
            truncations = {agent: False for agent in self.agents}

        # observations
        observations = {agent: self.next_observation(i+1) for i, agent in enumerate(self.agents)}

        # infos
        infos = {agent: {} for agent in self.agents}

        return observations, rewards, terminations, truncations, infos
