# spielmacher

`spielmacher` is a Python package for simulating the Prisoner's Dilemma game. It supports both 1v1 and tournament-style gameplay, allowing users to create various player strategies and observe their interactions over multiple rounds.

## Installation

```bash
pip install spielmacher
```

## Usage

### 1v1 Gameplay

To simulate a 1v1 game, you need to create instances of `Player` subclasses and configure the game using `GameConfig`. Then, create a `Game` instance and run it.

```python
from spielmacher.player import CooperativePlayer, EgoisticPlayer
from spielmacher.game import Game, GameConfig

# Create player instances
player1 = CooperativePlayer()
player2 = EgoisticPlayer()

# Configure the game
config = GameConfig(player1, player2)

# Create and run the game
game = Game(config)
game.run()
scores = game.get_scores()
print(f"Final Scores: {scores}")
game.plot_scores()
```

### Tournament Gameplay

To simulate a tournament, create a list of `Player` instances and configure the tournament using the `Tournament` class. Then, run the tournament.

```python
from spielmacher.player import CooperativePlayer, EgoisticPlayer, RandomPlayer
from spielmacher.tournament import Tournament

# Create player instances
players = [
    CooperativePlayer(),
    EgoisticPlayer(),
    RandomPlayer()
]

# Configure and run the tournament
tournament = Tournament(players, rounds_per_game=10)
tournament.run()
```

## Configuration Options

### GameConfig

The `GameConfig` class is used to configure a 1v1 game. It has the following options:

- `player1` (Player): The first player.
- `player2` (Player): The second player.
- `num_rounds` (int, optional): The number of rounds to be played. Default is 10.
- `mistake_probability` (float, optional): The probability of a mistake occurring in communication. Default is 0.0.
- `score_map` (ScoreMap, optional): The rewards given after a round based on the players' decisions.

Example:

```python
config = GameConfig(player1, player2, num_rounds=20, mistake_probability=0.05)
```

### Tournament

The `Tournament` class is used to configure and run a tournament. It has the following options:

- `players` (list\[Player\]): A list of player instances participating in the tournament.
- `rounds_per_game` (int): The number of rounds to be played in each game.

Example:

```python
tournament = Tournament(players, rounds_per_game=15)
```

## Player Strategies

The package includes several predefined player strategies:

- `CooperativePlayer`: Always cooperates.
- `EgoisticPlayer`: Always defects.
- `RandomPlayer`: Chooses moves randomly between cooperate and defect.
- `GrudgerPlayer`: Cooperates until the opponent defects, then always defects.
- `DetectivePlayer`: Cooperates until the opponent defects twice in a row, then always defects.
- `TitForTatPlayer`: Cooperates at first, then plays the opponent's last move.
- `ForgivingTitForTatPlayer`: Cooperates until the opponent defects, then has a 10% chance to forgive a defect.
- `SimpletonPlayer`: Cooperates on the first round. If the opponent cooperates, repeats its last move. If the opponent defects, switches its last move.
- `EveryNthDefectorPlayer`: Defects every nth turn.
- `HumanPlayer`: Human player that selects moves manually.
- `SimulatedPlayer`: Simulated player that selects moves based on a pre-trained model.

## Uploading

```bash
python -m build
python -m twine upload dist/*
```

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
