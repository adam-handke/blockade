# Blockade

Python remake of [the 1976 multiplayer snake-like game](https://en.wikipedia.org/wiki/Blockade_(video_game)) created in [Python Arcade](https://github.com/pythonarcade/arcade).

The game currently supports only 2 players. There are 5 types of players (1 human and 4 AI bots):
- **Human** - controlling with arrows or WSAD.
- **Random** - a bot that randomly selects one of the possible move directions (moves erratically but avoids immediate death until it's inevitable).
- **Heuristic** - a bot with moves heuristically scored by the difference of available area (calculated with [flood fill](https://en.wikipedia.org/wiki/Flood_fill) algorithm) and [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry) to the opponent (the bot always chases the opponent while dodging death). The move with the highest score is selected unless there is a tie, then it's chosen randomly out of the top-scored moves.
- **Optimized** - the best bot achieved in a custom competitive coevolution process, it's similar to the Heuristic bot but the behavior is modified by 4 weights (agoraphillic/agoraphobic, aggressive/elusive, evasive/ballsy, preferring straight lines/turns).
- **Reinforcement learning** - a bot trained on many games while receiving rewards after every step. The training environment is a custom [`ParallelEnv`](https://pettingzoo.farama.org/api/parallel/) created using [Gymnasium](https://github.com/Farama-Foundation/Gymnasium), [PettingZoo](https://github.com/Farama-Foundation/PettingZoo) and [SuperSuit](https://github.com/Farama-Foundation/SuperSuit). The model is a tuned [`A2C`](https://stable-baselines3.readthedocs.io/en/master/modules/a2c.html) from [Stable Baselines 3](https://github.com/DLR-RM/stable-baselines3) trained on 20 million steps.

The player which survives wins!

![Blockade gameplay](https://github.com/adam-handke/blockade/blob/main/gameplay.gif)

## Controls

| Action              | Key (`arrows` / `wsad` player) |
|---------------------|--------------------------------|
| Move UP             | 🡅       / W                   |
| Move DOWN           | 🡇       / S                   |
| Move LEFT           | 🡄       / A                   |
| Move RIGHT          | 🡆       / D                   |
| Increase game speed | +                              |
| Decrease game speed | -                              |
| Mute/unmute sound   | M                              |
| Exit                | Escape                         |              

## Requirements

For playing the game you only need:
- Python Arcade
- NumPy
- Stable-Baselines3 (**at least 2.0.0**)

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

### Arguments:

| Long name         | Short name | Description                                                                 | Options                                                    | Default value |
|-------------------|------------|-----------------------------------------------------------------------------|------------------------------------------------------------|---------------|
| `--help`          | `-h`       | Shows help message and exits the game.                                      | [flag]                                                     | `False`       |
| `--player1`       | `-p1`      | Type of the first player (green color).                                     | `arrows`, `wsad`, `random`, `heuristic`, `optimized`, `rl` | `arrows`      |
| `--player2`       | `-p2`      | Type of the second player (red color).                                      | `arrows`, `wsad`, `random`, `heuristic`, `optimized`, `rl` | `random`      |
| `--arena-size`    | `-a`       | Size of the square game arena (in tiles).                                   | Integers between `10`-`20`                                 | `10`          |
| `--tile-size`     | `-t`       | Size of a square game tile (in pixels).                                     | Integers between `15`-`75`                                 | `50`          |
| `--game-speed`    | `-s`       | Game speed, number of moves per second.                                     | Floats between `1.0`-`60.0`                                 | `2.0`         |
| `--random-seed`   | `-r`       | RNG initialization seed, controls random behaviors of bots.                 | Integer                                                    | `42`          |
| `--mute-sound`    | `-m`       | Mutes game sound effects.                                                   | [flag]                                                     | `False`       |
| `--window-hidden` | `-w`       | Hides game window (sound and human players are not available in this mode). | [flag]                                                     | `False`       |
| `--verbose`       | `-v`       | Verbosity switch, prints game info to the terminal.                         | [flag]                                                     | `False`       |

Note: two human players can't use the same input method at the same time.

## Bot training

### Optimized bot
![Evolution plot](https://github.com/adam-handke/blockade/blob/main/training/avg-weight-evolution2.png?raw=true)

### Reinforcement learning bot
![RL training plot](https://github.com/adam-handke/blockade/blob/main/training/A2C15v2_training_log_plot.png?raw=true)


## Bot performance comparison

### Base results 

Wins/draws/loses from the perspective of Player 1.

| Player 2 \ Player 1      | RandomBot   | HeuristicBot | OptimizedBot | ReinforcementLearningBot |
|--------------------------|-------------|--------------|--------------|--------------------------|
| RandomBot                | 480/66/454  | 834/129/37   | 849/128/23   | 560/94/346               |
| HeuristicBot             | 43/85/872   | 344/166/490  | 512/88/400   | 24/516/460               |
| OptimizedBot             | 55/137/808  | 272/354/374  | 385/221/394  | 1/931/68                 |
| ReinforcementLearningBot | 329/126/545 | 829/100/71   | 0/1000/0     | 386/371/243              |

### Aggregated results

| Bot type    | RandomBot | HeuristicBot | OptimizedBot | ReinforcementLearningBot |
|-------------|-----------|--------------|--------------|--------------------------|
| Total wins  | 1767      | 4501         | 3390         | 1830                     |
| Total draws | 831       | 1604         | 3080         | 3509                     |
| Total loses | 5402      | 1895         | 1530         | 2661                     |
