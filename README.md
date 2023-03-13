# Blockade
Python remake of [a 1976 multiplayer snake-like game](https://en.wikipedia.org/wiki/Blockade_(video_game)). Includes 4 types of AI bots:
- **Random** - randomly selects one of the possible move directions (avoids immediate death until it's inevitable).
- **Heuristic** - always chases the opponent while dodging immediate death.
- **Optimized** - the best bot achieved in an evolutionary optimization process.
- **Reinforcement learning** - bot trained from many games as a policy.

## Requirements

#TODO

## Running

```
python blockade.py [-h] 
                   [-p1 {arrows,wsad,random,heuristic,optimized,rl}]
                   [-p2 {arrows,wsad,random,heuristic,optimized,rl}]
                   [-a {10,11,12,13,14,15,16,17,18,19,20}]
                   [-s {1,2,3,4,5,6,7,8,9}] 
                   [-v]
```

Arguments:
  - `-h`, `--help` - show help message and exit;
  - `-p1` `--player1` - type of the first player (arrows, wsad, random, heuristic, optimized, rl};
  - `-p2`, `--player2` - type of the second player (arrows, wsad, random, heuristic, optimized, rl};
  - `-a`, `--arena-size` - size of the square game arena (10-20);
  - `-s`, `--game-speed` - game speed, number of moves per second (1-9);
  - `-v`, `--verbose` - verbose switch, prints game info to the terminal.

Note: human players can't use the same input method (arrows, wsad).

## Bot performance comparison

#TODO
