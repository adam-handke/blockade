from players.HumanPlayer import HumanPlayer
from players.RandomBot import RandomBot
from players.HeuristicBot import HeuristicBot
from players.OptimizedBot import OptimizedBot
from players.ReinforcementLearningBot import ReinforcementLearningBot
import argparse


class Blockade:
    def __init__(self, player1, player2, arena_size, game_speed, verbose):
        self.player1 = player1
        self.player2 = player2
        self.arena_size = arena_size
        self.game_speed = game_speed
        self.verbose = verbose

    def __str__(self):
        description = f'Game of Blockade with parameters:\n'
        for i, (key, value) in enumerate(self.__dict__.items()):
            description += f'\t{key} = {value}' + (',\n' if i < len(self.__dict__)-1 else '')
        return description


if __name__ == '__main__':
    player_types = {'arrows': HumanPlayer, 'wsad': HumanPlayer, 'random': RandomBot,
                    'heuristic': HeuristicBot, 'optimized': OptimizedBot, 'rl': ReinforcementLearningBot}

    parser = argparse.ArgumentParser()
    parser.add_argument('-p1', '--player1', help='type of the first player',
                        choices=player_types.keys(), default='random')
    parser.add_argument('-p2', '--player2', help='type of the second player',
                        choices=player_types.keys(), default='random')
    parser.add_argument('-a', '--arena-size', help='size of the square game arena', type=int,
                        choices=range(10, 21), default=10)
    parser.add_argument('-s', '--game-speed', help='game speed, number of moves per second', type=int,
                        choices=range(1, 10), default=2)
    parser.add_argument('-v', '--verbose', help='verbose switch, prints game info to the terminal', action='store_true')
    args = parser.parse_args()

    # human players can't use the same input method
    if player_types[args.player1] == HumanPlayer and player_types[args.player2] == HumanPlayer \
            and args.player1 == args.player2:
        raise ValueError(f'two human players use the same input method: {args.player1}')

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

    game = Blockade(player1=init_player1,
                    player2=init_player2,
                    arena_size=args.arena_size,
                    game_speed=args.game_speed,
                    verbose=args.verbose)

    print(game)
