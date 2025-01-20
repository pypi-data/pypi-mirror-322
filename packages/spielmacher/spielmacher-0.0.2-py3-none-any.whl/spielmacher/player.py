import random
from enum import Enum
from abc import ABC, abstractmethod

import joblib
import numpy as np
from sklearn.calibration import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

type MoveHistory = list[list[Move]]
type ScoreHistory = list[list[Move]]


class Move(Enum):
    COOPERATE = "C"
    DEFECT = "D"
    EMPTY = "E"


class Player(ABC):
    round_score: int
    total_score: int
    num_games: int
    move_history: MoveHistory
    score_history: ScoreHistory
    name: str = "GenericPlayer"

    @property
    def current_move_history(self) -> list[Move]:
        return self.move_history[self.num_games]

    @property
    def last_move(self) -> Move:
        return self.current_move_history[-1]

    def __init__(self):
        self.reset()

    def reset(self):
        self.round_score = 0
        self.total_score = 0
        self.num_games = 0
        self.move_history = [[]]
        self.score_history = [[]]

    def update_move_history(self, move: Move) -> None:
        self.move_history[self.num_games].append(move)

    def update_round_score(self, points: int) -> None:
        self.round_score += points
        self.score_history[self.num_games].append(self.round_score)

    def prepare_for_next_game(self) -> None:
        self.total_score += self.round_score
        self.round_score = 0
        self.num_games += 1
        self.score_history[self.num_games] = []
        self.move_history[self.num_games] = []

    def print_moves(self) -> None:
        styled_history = [
            (
                f"\033[92m{move.value}\033[0m"
                if move == Move.COOPERATE
                else f"\033[91m{move.value}\033[0m"
            )
            for move in self.move_history[self.num_games]
        ]
        print(f"{self.name:<25} {' '.join(styled_history)}")

    @abstractmethod
    def select_move(self, opponent_history: list[Move]) -> Move:
        pass


class CooperativePlayer(Player):
    """
    Always cooperates.
    """

    name: str = "CooperativePlayer"

    def select_move(self, opponent_history: list[Move]) -> Move:
        return Move.COOPERATE


class EgoisticPlayer(Player):
    """
    Always defects
    """

    name: str = "EgoisticPlayer"

    def select_move(self, opponent_history: list[Move]) -> Move:
        return Move.DEFECT


class RandomPlayer(Player):
    """
    Chooses moves randomly between cooperate and egoistic.
    """

    name: str = "RandomPlayer"

    def select_move(self, opponent_history: list[Move]) -> Move:
        return random.choice([Move.COOPERATE, Move.DEFECT])


class GrudgerPlayer(Player):
    """
    Cooperates until the opponent defects, then always defects.
    """

    name: str = "GrudgerPlayer"

    def select_move(self, opponent_history: list[Move]) -> Move:
        return Move.DEFECT if Move.DEFECT in opponent_history else Move.COOPERATE


class DetectivePlayer(Player):
    """
    Cooperates until the opponent defects twice in a row, then always defects.
    """

    name: str = "DetectivePlayer"
    defect: bool = False

    def reset(self):
        super().reset()
        self.defect = False

    def select_move(self, opponent_history: list[Move]) -> Move:
        move = Move.COOPERATE

        if self.defect:
            move = Move.DEFECT
        elif (
            len(opponent_history) >= 2
            and opponent_history[-1] == Move.DEFECT
            and opponent_history[-2] == Move.DEFECT
        ):
            self.defect = True
            move = Move.DEFECT

        return move


class TitForTatPlayer(Player):
    """
    Cooperates at first, then plays the opponent's last move.
    """

    name: str = "TitForTatPlayer"

    def select_move(self, opponent_history: list[Move]) -> Move:
        return Move.COOPERATE if not opponent_history else opponent_history[-1]


class ForgivingTitForTatPlayer(Player):
    """
    Cooperates until the opponent defects, then a 10% chance to forgive a defect
    """

    name: str = "ForgivingTitForTatPlayer"
    FORGIVE_PROBABILITY: int = 0.1  # 10% chance to forgive

    def select_move(self, opponent_history: list[Move]) -> Move:
        if not opponent_history:
            return Move.COOPERATE
        elif (
            opponent_history[-1] == Move.DEFECT
            and random.random() < self.FORGIVE_PROBABILITY
        ):
            return Move.COOPERATE

        return opponent_history[-1]


class SimpletonPlayer(Player):
    """
    Cooperates on the first round. If opponent cooperates, the player repeats its last move. If the opponent defects, the player switches its last move.
    """

    name: str = "SimpletonPlayer"
    last_move: Move = Move.COOPERATE

    def reset(self):
        super().reset()
        self.last_move = Move.COOPERATE

    def select_move(self, opponent_history: list[Move]) -> Move:
        move = Move.COOPERATE

        if not opponent_history:
            move = Move.COOPERATE
        elif opponent_history[-1] == Move.COOPERATE:
            move = self.last_move
        else:
            move = Move.DEFECT if self.last_move == Move.COOPERATE else Move.COOPERATE

        self.last_move = move
        return move


class EveryNthDefectorPlayer(Player):
    """
    Defects every nth turn.
    """

    name: str = "EveryNthDefectorPlayer"
    n: int

    def __init__(self, n: int):
        self.n = n
        self.name = f"EveryNthDefectorPlayer_{n}"
        super().__init__()

    def select_move(self, opponent_history: list[Move]) -> Move:
        return (
            Move.DEFECT
            if len(self.current_move_history) % self.n == 0
            else Move.COOPERATE
        )


class HumanPlayer(Player):
    """
    Human player that selects moves manually.
    """

    name: str = "HumanPlayer"

    def select_move(self, opponent_history: list[Move]) -> Move:
        while True:
            move = (
                input("Enter your move (C for Cooperate, D for Defect): ")
                .strip()
                .upper()
            )
            if move == "C":
                return Move.COOPERATE
            elif move == "D":
                return Move.DEFECT
            else:
                print("Invalid input. Please enter 'C' or 'D'.")


class SimulatedPlayer(Player):
    """
    Simulated player that selects moves based on a pre-trained model.
    """

    name: str = "SimulatedPlayer"
    model: RandomForestClassifier
    encoder: LabelEncoder

    def __init__(self, model_path: str):
        super().__init__()
        self.model = joblib.load(model_path)
        self.encoder = LabelEncoder().fit([move.value for move in Move])

    def select_move(self, opponent_history: list[Move]) -> Move:
        player_history = self.__transform_history(self.current_move_history)
        opponent_history = self.__transform_history(opponent_history)

        model_input = np.concat([player_history, opponent_history])

        prediction = self.model.predict([model_input])[0]
        predicted_move = self.encoder.inverse_transform([prediction])[0]
        return Move(predicted_move)

    def __transform_history(self, history: list[Move]) -> list[int]:
        transformed = [move.value for move in history]
        # TODO: remove magic number 10
        transformed += [Move.EMPTY.value] * (
            10 - len(transformed)
        )  # Pad the list to the required length
        return self.encoder.transform(transformed)
