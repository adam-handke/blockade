# Blockade
Python remake of [a 1976 multiplayer snake-like game](https://en.wikipedia.org/wiki/Blockade_(video_game)) created in [Python Arcade](https://api.arcade.academy/en/latest/).

The game currently supports only 2 players. Humans can use arrows or WSAD. There are 4 types of AI bots:
- **Random** - randomly selects one of the possible move directions (avoids immediate death until it's inevitable).
- **Heuristic** - always chases the opponent while dodging death (moves scored by Manhattan distance to the opponent and available area, move is randomly selected in case of a tie).
- **Optimized** - the best bot achieved in an evolutionary optimization process.
- **Reinforcement learning** - bot trained from many games as a policy.

The player which survives wins!

![Blockade screenshot](https://github.com/adam-handke/blockade/blob/main/screenshot.jpg?raw=true)

## Requirements
- Arcade
- NumPy

Details in `requirements.txt`.

## Running

```
python blockade.py [-h] 
                   [-p1 {arrows,wsad,random,heuristic,optimized,rl}]
                   [-p2 {arrows,wsad,random,heuristic,optimized,rl}]
                   [-a {10,11,12,13,14,15,16,17,18,19,20}]
                   [-t {15,20,25,30,35,40,45,50,55,60,65,70,75}]
                   [-s GAME_SPEED]
                   [-r RANDOM_SEED]
                   [-m]
                   [-w]
                   [-v]
```

Arguments:
  - `-h`, `--help` - show help message and exit;
  - `-p1`, `--player1` - type of the first player, green color (`arrows`, `wsad`, `random`, `heuristic`, `optimized`, `rl`), default: `arrows`;
  - `-p2`, `--player2` - type of the second player, red color (`arrows`, `wsad`, `random`, `heuristic`, `optimized`, `rl`), default: `random`;
  - `-a`, `--arena-size` - size of the square game arena (in tiles, `10`-`20`), default: `10`;
  - `-t`, `--tile-size` - size of a square game tile (in pixels, `15`-`75`), default: `50`;
  - `-s`, `--game-speed` - game speed, number of moves per second (positive float), default: `2.0`;
  - `-r`, `--random-seed` - RNG initialization seed (integer), default: `42`;
  - `-m`, `--mute-sound` - mutes game sound effects, default: `False`;
  - `-w`, `--window-hidden` - hides game window, default: `False`;
  - `-v`, `--verbose` - verbose switch, prints game info to the terminal, default: `False`.

Note: two human players can't use the same input method at the same time.

## Bot performance comparison

#TODO
