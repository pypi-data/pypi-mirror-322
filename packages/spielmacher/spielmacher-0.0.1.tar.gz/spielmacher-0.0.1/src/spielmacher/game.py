import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from enum import Enum
from player import Player, Move
from typing import Callable, Optional


SCORE_MAP = {
    (Move.COOPERATE, Move.COOPERATE): (3, 3),
    (Move.DEFECT, Move.DEFECT): (1, 1),
    (Move.DEFECT, Move.COOPERATE): (5, 0),
    (Move.COOPERATE, Move.DEFECT): (0, 5),
}


class GameConfig(object):
    player1: Player
    player2: Player
    num_rounds: int = 10
    mistake_probability: float = 0.0

    def __init__(
        self,
        player1: Player,
        player2: Player,
        num_rounds: int,
        mistake_probability: float,
    ) -> None:
        self.player1 = player1
        self.player2 = player2
        self.num_rounds = num_rounds
        self.mistake_probability = mistake_probability


class GameState(Enum):
    INITIALIZED = "INIT"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"


class Game:
    __p1: Player
    __p2: Player
    __num_rounds: int
    __mistake_probability: float
    __state: GameState

    def __init__(self, config: GameConfig) -> None:
        self.__p1 = config.player1
        self.__p2 = config.player2
        self.__num_rounds = config.num_rounds or 10
        self.__mistake_probability = config.mistake_probability or 0.0
        self.__state = GameState.INITIALIZED

    def get_scores(self) -> tuple[int, int]:
        return self.__p1.round_score, self.__p2.round_score

    def plot_scores(self) -> None:
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        self.__current_round = 0

        def plot_round(round_index):
            p1_scores = self.__p1.score_history
            p2_scores = self.__p2.score_history

            ax.clear()
            ax.set_ylim(0, max(p1_scores + p2_scores) + 5)

            p1_score = p1_scores[round_index]
            p2_score = p2_scores[round_index]

            rects = ax.bar(
                [self.__p1.name, self.__p2.name],
                [p1_score, p2_score],
            )
            ax.bar_label(rects, padding=3)
            ax.set_title(f"Scores after round {round_index}")
            plt.draw()

        def next(event):
            if self.__current_round < self.__num_rounds:
                self.__current_round += 1
                plot_round(self.__current_round)

        def prev(event):
            if self.__current_round > 0:
                self.__current_round -= 1
                plot_round(self.__current_round)

        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, "Next")
        bnext.on_clicked(next)
        bprev = Button(axprev, "Previous")
        bprev.on_clicked(prev)

        plot_round(self.__current_round)
        plt.show()

    def run(self, callback: Optional[Callable[[Player, Player], None]] = None) -> None:
        self.__state = GameState.RUNNING

        for _ in range(self.__num_rounds):
            self.__play_round()
            if callback:
                callback(self.__p1, self.__p2)

        self.__state = GameState.FINISHED

    def __play_round(self) -> None:
        # Step 1: Get moves from players
        move1 = self.__p1.select_move(self.__p2.current_move_history)
        move2 = self.__p2.select_move(self.__p1.current_move_history)

        # Step 2: Apply potential mistakes in communication
        self.__apply_mistake(move1)
        self.__apply_mistake(move2)

        # Step 3: Update move history
        self.__p1.update_move_history(move1)
        self.__p2.update_move_history(move2)

        # Step 4: Calculate and update round scores
        self.__update_scores(move1, move2)

    def __apply_mistake(self, move: Move) -> None:
        if random.random() < self.__mistake_probability:
            move = Move.COOPERATE if move == Move.DEFECT else Move.DEFECT
        return move

    def __update_scores(self, move1: Move, move2: Move) -> None:
        score1, score2 = SCORE_MAP[(move1, move2)]
        self.__p1.update_round_score(score1)
        self.__p2.update_round_score(score2)
