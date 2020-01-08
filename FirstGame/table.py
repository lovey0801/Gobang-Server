from . import utils
from .player import Player
import json


class Table:
    tableCode = 0

    rows = 20
    cols = 20

    def __init__(self):
        self.squares = []
        self.playerX = None
        self.playerO = None
        Table.tableCode += 1
        self.code = Table.tableCode
        self.initSquares()

    def addPlayer(self, player):
        if self.playerX is None:
            if self.playerO is not None and self.playerO.name == player.name:
                return -1
            self.playerX = player
            player.setRole("X")
        elif self.playerO is None:
            if self.playerX is not None and self.playerX.name == player.name:
                return -1
            self.playerO = player
            player.setRole("O")
        return 0

    def hasEmptyPlayer(self):
        return self.playerX is None or self.playerO is None

    def initSquares(self):
        for _ in range(0, Table.rows):
            for _ in range(0, Table.cols):
                self.squares.append("")

    def calcSquares(self):
        for i in self.playerX.playHistory:
            self.squares[i] = "X"
        for j in self.playerO.playHistory:
            self.squares[j] = "O"
        return self.squares

    def toDict(self):
        return {
            "code": self.code,
            "playerX": "" if self.playerX is None else self.playerX.toDict(),
            "playerO": "" if self.playerO is None else self.playerO.toDict(),
            "rows": Table.rows,
            "cols": Table.cols,
            "squares": self.squares
        }

    def ready(self, role):
        self.get_player(role).ready()
        return 0

    def start(self):
        self.playerO.start()
        self.playerX.start()
        self.squares = []
        self.initSquares()

    def isAllPlayerReady(self):
        return self.playerX is not None and self.playerX.readyState \
               and self.playerO is not None and self.playerO.readyState

    def play(self, role, position):
        if 0 <= position < Table.rows * Table.cols:
            if len(self.squares[position]) <= 0:
                self.get_player(role).play(position)
                self.squares[position] = role
                ret = self.calc_win(role, position)
                return ret
        return 0

    def get_player(self, role):
        if role == "X":
            return self.playerX
        else:
            return self.playerO

    def calc_win(self, role, position):
        start = -4
        end = 5

        play_history = self.get_player(role).playHistory

        counts = [0, 0, 0, 0]
        for i in range(start, end):
            for j in range(start, end):
                if i == 0:
                    counts[0] = utils.five(play_history, position + j, counts[0])
                if j == 0:
                    counts[1] = utils.five(play_history, position + i * Table.cols, counts[1])
                if i == j:
                    counts[2] = utils.five(play_history, position + j + i * Table.cols, counts[2])
                if i == -j:
                    counts[3] = utils.five(play_history, position + j + i * Table.cols, counts[3])
                for item in counts:
                    if item >= 5:
                        return 2
        return 1

    def game_over(self):
        self.playerX.readyState = False
        self.playerO.readyState = False

