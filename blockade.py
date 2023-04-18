import argparse
import arcade
import numpy as np
import random
import time

from players.HumanPlayer import HumanPlayer
from players.RandomBot import RandomBot
from players.HeuristicBot import HeuristicBot
from players.OptimizedBot import OptimizedBot
from players.ReinforcementLearningBot import ReinforcementLearningBot


class Blockade:
    def __init__(self, player1, player2, arena_size, verbose):
        # command line arguments init
        self.player1 = player1
        self.player2 = player2
        self.arena_size = arena_size
        self.verbose = verbose

        # game init
        self.game_matrix = np.zeros((self.arena_size, self.arena_size), dtype=int)
        # game matrix internal encoding:
        #  0 - empty
        #  1 - player1 head
        # -1 - player1 tail
        #  2 - player2 head
        # -2 - player2 tail
        # 999 - player collision
        starting_position = int(self.arena_size / 4)
        # player1 starts in the bottom-right corner
        self.game_matrix[self.arena_size - starting_position - 1, self.arena_size - starting_position - 1] = 1
        # player2 starts in the upper-left corner
        self.game_matrix[starting_position, starting_position] = 2

        self.move_dict = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}  # (y, x) offset tuples
        self.move_counter = 0
        self.max_number_of_moves = int(np.ceil(self.arena_size**2 / 2.0) - 2)

    def find_possible_moves(self, head):
        possible_moves = dict()
        # no head found - no possible moves
        if len(head[0]) == 0 or len(head[1]) == 0:
            return possible_moves

        for move in self.move_dict.keys():
            # check y borders and x borders and free tile
            if self.game_matrix.shape[0]-1 >= head[0] + self.move_dict[move][0] >= 0 \
                    and self.game_matrix.shape[1]-1 >= head[1] + self.move_dict[move][1] >= 0 \
                    and self.game_matrix[head[0] + self.move_dict[move][0], head[1] + self.move_dict[move][1]] == 0:
                possible_moves[move] = self.move_dict[move]
        return possible_moves

    def check_human_trying_impossible_move(self, player, possible_moves):
        return isinstance(player, HumanPlayer) \
            and player.current_direction is not None \
            and player.current_direction not in possible_moves.keys()

    def process_move(self):
        # returns game outcome:
        # None - unfinished
        # 0 - draw
        # 1 - player1 won
        # 2 - player2 won

        # gather possible moves
        p1_head = np.where(self.game_matrix == 1)
        p1_possible_moves = self.find_possible_moves(p1_head)
        p2_head = np.where(self.game_matrix == 2)
        p2_possible_moves = self.find_possible_moves(p2_head)

        # if no possible moves: player loses; if both don't have possible moves: draw; else: continue game
        if (len(p1_possible_moves) == 0 or self.check_human_trying_impossible_move(self.player1, p1_possible_moves)) \
                and (len(p2_possible_moves) == 0 or self.check_human_trying_impossible_move(self.player2,
                                                                                            p2_possible_moves)):
            if self.verbose:
                print('Draw!')
            return 0
        elif len(p1_possible_moves) == 0 or self.check_human_trying_impossible_move(self.player1, p1_possible_moves):
            if self.verbose:
                print('Player 2 wins!')
            return 2
        elif len(p2_possible_moves) == 0 or self.check_human_trying_impossible_move(self.player2, p2_possible_moves):
            if self.verbose:
                print('Player 1 wins!')
            return 1
        elif (isinstance(self.player1, HumanPlayer) and self.player1.current_direction is None) \
                or (isinstance(self.player2, HumanPlayer) and self.player2.current_direction is None):
            # at least one of the players is human and didn't make the first move yet
            if self.verbose:
                print('Waiting for human input!', flush=True)
        else:
            # both players have possible moves - ask the players to select their moves
            self.move_counter += 1
            p1_move = self.player1.get_move(self.game_matrix, p1_possible_moves, p1_head, p2_head)
            p2_move = self.player2.get_move(self.game_matrix, p2_possible_moves, p2_head, p1_head)
            if self.move_counter > self.max_number_of_moves:
                raise RuntimeError(f'counted moves than should be possible: {self.move_counter} '
                                   f'(should be less than {self.max_number_of_moves})')
            if self.verbose:
                print(f'Move {self.move_counter}: '.ljust(10) + f'Player1 goes {p1_move}\tPlayer2 goes {p2_move}',
                      flush=True)
            # update player1
            self.game_matrix[p1_head[0], p1_head[1]] = -1
            self.game_matrix[p1_head[0] + self.move_dict[p1_move][0], p1_head[1] + self.move_dict[p1_move][1]] = 1
            # update player2
            self.game_matrix[p2_head[0], p2_head[1]] = -2
            self.game_matrix[p2_head[0] + self.move_dict[p2_move][0], p2_head[1] + self.move_dict[p2_move][1]] = 2
            # edge case: players tried to move to the same tile (head collision)
            if p1_head[0] + self.move_dict[p1_move][0] == p2_head[0] + self.move_dict[p2_move][0] \
                    and p1_head[1] + self.move_dict[p1_move][1] == p2_head[1] + self.move_dict[p2_move][1]:
                self.game_matrix[p1_head[0] + self.move_dict[p1_move][0], p1_head[1] + self.move_dict[p1_move][1]] = 999
            return None

    def run_windowless(self):
        # mainly for fast bot testing, uses no Arcade backend

        # humans can't play when the window is not visible
        if isinstance(self.player1, HumanPlayer) or isinstance(self.player2, HumanPlayer):
            raise ValueError(f'human player can`t participate in a windowless game')

        while True:
            outcome = self.process_move()
            if outcome is not None:
                break
        return outcome


class BlockadeWindowed(Blockade, arcade.Window):
    # visual mode for humans playing against bots or observing bots fighting against each other
    def __init__(self, player1, player2, arena_size, tile_size, game_speed, mute_sound, verbose):
        # arcade init
        # size of the window depends on the arena and tile size but is limited by the screen resolution
        max_width = min(arena_size * tile_size, int(arcade.window_commands.get_display_size()[0]))
        max_height = min(arena_size * tile_size, int(arcade.window_commands.get_display_size()[1]))
        self.actual_window_size = min(max_width, max_height)
        self.actual_tile_size = self.actual_window_size / arena_size
        arcade.Window.__init__(self, width=self.actual_window_size, height=self.actual_window_size, title='Blockade')
        self.background_color = arcade.color.ARSENIC

        # blockade init
        Blockade.__init__(self, player1, player2, arena_size, verbose)
        self.game_over = False
        self.tile_size = tile_size
        self.game_speed = game_speed
        self.speed_change_step = 1.0
        self.max_speed = 60.0
        self.frame_mod = int(np.round(self.max_speed / self.game_speed))
        self.frame_counter = 0
        self.mute_sound = mute_sound
        self.tile_colors = {1: (0, 153, 51), -1: (0, 204, 68), 2: (204, 0, 0), -2: (255, 51, 51),
                            999: (204, 153, 51)}  # RGB colors
        self.keys = {arcade.key.UP: 'up', arcade.key.DOWN: 'down', arcade.key.LEFT: 'left', arcade.key.RIGHT: 'right',
                     arcade.key.W: 'up', arcade.key.S: 'down', arcade.key.A: 'left', arcade.key.D: 'right'}
        self.sounds = {'move': arcade.load_sound(':resources:sounds/phaseJump1.wav'),
                       'game_over': arcade.load_sound(':resources:sounds/gameover4.wav')}

    def update_game_speed(self, new_speed):
        self.game_speed = new_speed
        self.frame_mod = int(np.round(self.max_speed / new_speed))

    def on_key_press(self, symbol: int, modifiers: int):
        # handling user input
        # arrows
        if symbol in [arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT]:
            if isinstance(self.player1, HumanPlayer) and self.player1.keyboard_input == 'arrows':
                self.player1.current_direction = self.keys[symbol]
            elif isinstance(self.player2, HumanPlayer) and self.player2.keyboard_input == 'arrows':
                self.player2.current_direction = self.keys[symbol]
            elif self.verbose:
                print(f'No player uses arrows!', flush=True)
        # WSAD
        elif symbol in [arcade.key.W, arcade.key.S, arcade.key.A, arcade.key.D]:
            if isinstance(self.player1, HumanPlayer) and self.player1.keyboard_input == 'wsad':
                self.player1.current_direction = self.keys[symbol]
            elif isinstance(self.player2, HumanPlayer) and self.player2.keyboard_input == 'wsad':
                self.player2.current_direction = self.keys[symbol]
            elif self.verbose:
                print(f'No player uses WSAD!', flush=True)
        # other keys
        elif symbol == arcade.key.ESCAPE:
            if self.verbose:
                print('Premature exit on Escape.', flush=True)
            self.exit_game()
        elif symbol == arcade.key.EQUAL or symbol == arcade.key.NUM_ADD:
            if self.game_speed <= self.max_speed - self.speed_change_step:
                self.update_game_speed(self.game_speed + self.speed_change_step)
                if self.verbose:
                    print(f'Increased speed to {self.game_speed}.', flush=True)
            else:
                self.update_game_speed(self.max_speed)
                if self.verbose:
                    print(f'Speed too high to increase further: {self.game_speed}.', flush=True)
        elif symbol == arcade.key.MINUS or symbol == arcade.key.NUM_SUBTRACT:
            if self.game_speed > self.speed_change_step * 2:
                self.update_game_speed(self.game_speed - self.speed_change_step)
                if self.verbose:
                    print(f'Decreased speed to {self.game_speed}.', flush=True)
            else:
                self.update_game_speed(self.speed_change_step)
                if self.verbose:
                    print(f'Speed too low to decrease further: {self.game_speed}.', flush=True)
        elif symbol == arcade.key.M:
            self.mute_sound = not self.mute_sound
            if self.verbose:
                if self.mute_sound:
                    print(f'Sound muted.', flush=True)
                else:
                    print(f'Sound unmuted.', flush=True)
        elif self.verbose:
            print(f'Unknown keyboard input: {symbol}', flush=True)

    def on_draw(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_mod == 0 and not self.game_over:
            outcome = self.process_move()
            if outcome is not None:
                # game finished - exit
                self.exit_game(sound=True)
            else:
                # play move sound
                if not ((isinstance(self.player1, HumanPlayer) and self.player1.current_direction is None)
                        or (isinstance(self.player2, HumanPlayer) and self.player2.current_direction is None)) \
                        and not self.mute_sound:
                    arcade.sound.play_sound(self.sounds['move'], volume=0.3, speed=self.game_speed ** 0.05)

        # game matrix drawing
        self.clear()
        # y-axis is adjusted for different coordinate systems of np.array and Python Arcade (matrix vs Cartesian)
        for y in range(self.game_matrix.shape[0]):
            for x in range(self.game_matrix.shape[1]):
                if self.game_matrix[y, x] != 0:
                    arcade.draw_rectangle_filled(center_x=(x + 0.5) * self.actual_tile_size,
                                                 center_y=(self.arena_size - y - 0.5) * self.actual_tile_size,
                                                 width=self.actual_tile_size, height=self.actual_tile_size,
                                                 color=self.tile_colors[self.game_matrix[y, x]])

    def exit_game(self, sound=False):
        self.game_over = True
        if sound and not self.mute_sound:
            arcade.sound.play_sound(self.sounds['game_over'], volume=0.2)
        time.sleep(2.0 / self.game_speed)
        arcade.exit()


if __name__ == '__main__':
    player_types = {'arrows': HumanPlayer, 'wsad': HumanPlayer, 'random': RandomBot,
                    'heuristic': HeuristicBot, 'optimized': OptimizedBot, 'rl': ReinforcementLearningBot}

    parser = argparse.ArgumentParser()
    parser.add_argument('-p1', '--player1', help='type of the first player (green color)',
                        choices=player_types.keys(), default='arrows')
    parser.add_argument('-p2', '--player2', help='type of the second player (red color)',
                        choices=player_types.keys(), default='random')
    parser.add_argument('-a', '--arena-size', help='size of the square game arena (in tiles)', type=int,
                        choices=range(10, 21), default=10)
    parser.add_argument('-t', '--tile-size', help='size of a square game tile (in pixels)', type=int,
                        choices=range(15, 80, 5), default=50)
    parser.add_argument('-s', '--game-speed', help='game speed, number of moves per second (floats between 1.0-60.0)',
                        type=float, default=2.0)
    parser.add_argument('-r', '--random-seed', help='RNG initialization seed, controls random behaviors of bots',
                        type=int, default=42)
    parser.add_argument('-m', '--mute-sound', action='store_true', help='mutes game sound effects')
    parser.add_argument('-w', '--window-hidden', action='store_true',
                        help='hides game window (sound and human players are not available in this mode)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='verbosity switch, prints game info to the terminal')
    args = parser.parse_args()

    # human players can't use the same input method
    if player_types[args.player1] == HumanPlayer and player_types[args.player2] == HumanPlayer \
            and args.player1 == args.player2:
        raise ValueError(f'two human players can`t use the same input method: {args.player1}')

    # humans can't play when the window is not visible
    if (player_types[args.player1] == HumanPlayer or player_types[args.player2] == HumanPlayer) \
            and args.window_hidden:
        raise ValueError(f'human player can`t play when the window is hidden: --window_hidden / -w')

    # assert that game speed is in <1.0, 60.0>
    if args.game_speed < 1.0 or args.game_speed > 60.0:
        raise ValueError(f'game speed is not in interval <1.0, 60.0>: {args.game_speed}')

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
            print(f'\t{key} = {value}' + (',' if i < len(vars(args)) - 1 else ''), flush=True)

    random.seed(args.random_seed)
    if args.window_hidden:
        game = Blockade(player1=init_player1,
                        player2=init_player2,
                        arena_size=args.arena_size,
                        verbose=args.verbose)
        game.run_windowless()
    else:
        game = BlockadeWindowed(player1=init_player1,
                                player2=init_player2,
                                arena_size=args.arena_size,
                                tile_size=args.tile_size,
                                game_speed=args.game_speed,
                                mute_sound=args.mute_sound,
                                verbose=args.verbose)
        game.run()
