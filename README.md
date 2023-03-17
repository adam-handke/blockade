# Blockade
Python remake of [a 1976 multiplayer snake-like game](https://en.wikipedia.org/wiki/Blockade_(video_game)) created in [Python Arcade](https://api.arcade.academy/en/latest/).

The game currently supports only 2 players. Humans can use arrows or WSAD. There are 4 types of AI bots:
- **Random** - randomly selects one of the possible move directions (avoids immediate death until it's inevitable).
- **Heuristic** - always chases the opponent while dodging immediate death.
- **Optimized** - the best bot achieved in an evolutionary optimization process.
- **Reinforcement learning** - bot trained from many games as a policy.

The player which survives wins!

## Requirements

#TODO

## Running

```
python blockade.py [-h] 
                   [-p1 {arrows,wsad,random,heuristic,optimized,rl}]
                   [-p2 {arrows,wsad,random,heuristic,optimized,rl}]
                   [-a {10,11,12,13,14,15,16,17,18,19,20}]
                   [-t {25,30,35,40,45,50,55,60,65,70,75}]
                   [-s GAME_SPEED] 
                   [-w]
                   [-v]
```

Arguments:
  - `-h`, `--help` - show help message and exit;
  - `-p1` `--player1` - type of the first player (`arrows`, `wsad`, `random`, `heuristic`, `optimized`, `rl`), default: `arrows`;
  - `-p2`, `--player2` - type of the second player (`arrows`, `wsad`, `random`, `heuristic`, `optimized`, `rl`), default: `random`;
  - `-a`, `--arena-size` - size of the square game arena (in tiles, `10`-`20`), default: `10`;
  - `-t`, `--tile-size` - size of a square game tile (in pixels, `25`-`75`), default: `50`;
  - `-s`, `--game-speed` - game speed, number of moves per second (positive float), default: `2.0`;
  - `-w`, `--window-hidden` - hides game window, default: `False`;
  - `-v`, `--verbose` - verbose switch, prints game info to the terminal, default: `False`.

Note: two human players can't use the same input method at the same time.

## Bot performance comparison

#TODO
