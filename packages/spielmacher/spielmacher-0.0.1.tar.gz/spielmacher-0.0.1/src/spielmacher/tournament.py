from game import Game
from player import Player


class Tournament:
    __players: list[Player]
    __rounds_per_game: int

    def __init__(self, players: list[Player], rounds_per_game: int) -> None:
        self.__players = players
        self.__rounds_per_game = rounds_per_game

    def run(self) -> None:
        for i in range(len(self.__players)):
            for j in range(i + 1, len(self.__players)):
                p1 = self.__players[i]
                p2 = self.__players[j]

                game = Game(p1, p2, self.__rounds_per_game)
                winner = game.run()
                scores = game.get_scores()

                print(f"{p1.name} vs {p2.name}: {scores}")
                p1.print_moves()
                p2.print_moves()
                print(f"Winner: {winner.name}")

                game.plot_scores()
