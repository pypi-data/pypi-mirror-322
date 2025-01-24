from typing import Callable, Optional
from spielmacher.game import Game, GameConfig
from spielmacher.player import Player


class Tournament:
    __players: list[Player]
    __rounds_per_game: int

    def __init__(self, players: list[Player], rounds_per_game: int) -> None:
        self.__players = players
        self.__rounds_per_game = rounds_per_game

    def run(self, callback: Optional[Callable[[Player, Player], None]] = None) -> None:
        for i in range(len(self.__players)):
            for j in range(i + 1, len(self.__players)):
                p1 = self.__players[i]
                p2 = self.__players[j]

                config = GameConfig(p1, p2, self.__rounds_per_game)
                game = Game(config)
                game.run()

                if callback is not None:
                    callback(p1, p2)

                p1.prepare_for_next_game()
                p2.prepare_for_next_game()
