import numpy as np

from players.HumanPlayer import HumanPlayer
from players.RandomBot import RandomBot
from players.HeuristicBot import HeuristicBot
from players.OptimizedBot import OptimizedBot
from players.ReinforcementLearningBot import ReinforcementLearningBot
import argparse
import arcade
import random


class Blockade(arcade.Window):
    def __init__(self, player1, player2, arena_size, tile_size, game_speed, window_hidden, verbose):
        # arcade init
        # size of the window depends on the arena and tile size but is limited by the screen resolution
        max_width = min(arena_size * tile_size, int(arcade.window_commands.get_display_size()[0]))
        max_height = min(arena_size * tile_size, int(arcade.window_commands.get_display_size()[1]))
        self.actual_window_size = min(max_width, max_height)
        self.actual_tile_size = self.actual_window_size / arena_size
        super().__init__(width=self.actual_window_size, height=self.actual_window_size, title='Blockade',
                         visible=not window_hidden)
        self.background_color = arcade.color.ARSENIC

        # command line arguments init
        self.player1 = player1
        self.player2 = player2
        self.arena_size = arena_size
        self.tile_size = tile_size
        self.game_speed = game_speed
        self.verbose = verbose

        # game init
        self.game_matrix = None
        # game matrix internal encoding:
        #  0 - empty
        #  1 - player1 head
        # -1 - player1 tail
        #  2 - player2 head
        # -2 - player2 tail
        self.tile_colors = {1: (0, 153, 51), -1: (0, 204, 68), 2: (204, 0, 0), -2: (255, 51, 51)}  # RGB colors

    def setup(self):
        # game preparation
        self.game_matrix = np.zeros((self.arena_size, self.arena_size), dtype=int)
        starting_position = int(self.arena_size / 4)
        # player1 starts in the bottom-right corner
        self.game_matrix[self.arena_size - starting_position - 1, self.arena_size - starting_position - 1] = 1
        # player2 starts in the upper-left corner
        self.game_matrix[starting_position, starting_position] = 2

    def on_draw(self):
        # main game loop
        self.clear()

        # drawing tester
        # for y in range(self.game_matrix.shape[0]):
        #     for x in range(self.game_matrix.shape[1]):
        #         self.game_matrix[y, x] = random.choice([0, 1, -1, 2, -2])

        # game matrix drawing
        # y-axis is adjusted for different coordinate systems of np.array and Python Arcade (matrix vs Cartesian)
        for y in range(self.game_matrix.shape[0]):
            for x in range(self.game_matrix.shape[1]):
                if self.game_matrix[y, x] != 0:
                    arcade.draw_rectangle_filled(center_x=(x + 0.5) * self.actual_tile_size,
                                                 center_y=(self.arena_size - y - 0.5) * self.actual_tile_size,
                                                 width=self.actual_tile_size, height=self.actual_tile_size,
                                                 color=self.tile_colors[self.game_matrix[y, x]])


if __name__ == '__main__':
    player_types = {'arrows': HumanPlayer, 'wsad': HumanPlayer, 'random': RandomBot,
                    'heuristic': HeuristicBot, 'optimized': OptimizedBot, 'rl': ReinforcementLearningBot}

    parser = argparse.ArgumentParser()
    parser.add_argument('-p1', '--player1', help='type of the first player',
                        choices=player_types.keys(), default='arrows')
    parser.add_argument('-p2', '--player2', help='type of the second player',
                        choices=player_types.keys(), default='random')
    parser.add_argument('-a', '--arena-size', help='size of the square game arena (in tiles)', type=int,
                        choices=range(10, 21), default=10)
    parser.add_argument('-t', '--tile-size', help='size of a square game tile (in pixels)', type=int,
                        choices=range(25, 80, 5), default=50)
    parser.add_argument('-s', '--game-speed', help='game speed, number of moves per second (positive float)',
                        type=float, default=2.0)
    parser.add_argument('-w', '--window-hidden', help='hides game window', action='store_true')
    parser.add_argument('-v', '--verbose', help='verbose switch, prints game info to the terminal', action='store_true')
    args = parser.parse_args()

    # human players can't use the same input method
    if player_types[args.player1] == HumanPlayer and player_types[args.player2] == HumanPlayer \
            and args.player1 == args.player2:
        raise ValueError(f'two human players use the same input method: {args.player1}')

    # assert that game speed is larger than zero
    if args.game_speed <= 0:
        raise ValueError(f'game speed is not positive: {args.game_speed}')

    # create player1
    if player_types[args.player1] == HumanPlayer:
        init_player1 = HumanPlayer(keyboard_input=args.player1, verbose=args.verbose)
    else:
        init_player1 = player_types[args.player1](verbose=args.verbose)

    # create player2
    if player_types[args.player2] == HumanPlayer:
        init_player2 = HumanPlayer(keyboard_input=args.player2, verbose=args.verbose)
    else:
        init_player2 = player_types[args.player2](verbose=args.verbose)

    if args.verbose:
        print(f'Starting a game of Blockade with parameters:', flush=True)
        for i, (key, value) in enumerate(vars(args).items()):
            print(f'\t{key} = {value}' + (',\n' if i < len(vars(args)) - 1 else ''), end='', flush=True)

    game = Blockade(player1=init_player1,
                    player2=init_player2,
                    arena_size=args.arena_size,
                    tile_size=args.tile_size,
                    game_speed=args.game_speed,
                    window_hidden=args.window_hidden,
                    verbose=args.verbose)

    game.setup()
    arcade.run()
