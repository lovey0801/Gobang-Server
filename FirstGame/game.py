from .player import Player
from .table import Table
import time


class Game:
    stateIdle = 0
    stateGaming = 1
    stateGameOver = 2

    def __init__(self):
        self.table = None
        self.state = Game.stateIdle
        self.winner = None
        self.curPlayer = None
        self.timestamp = time.time()

    def toDict(self):
        return {
            "table": self.table.toDict(),
            "state": self.state,
            "winner": self.winner,
            "curPlayer": self.curPlayer,
            "timestamp": str(self.timestamp)
        }

    def updateTimestamp(self):
        self.timestamp = time.time()

    def enterPlayer(self, player):
        if self.table.addPlayer(player) == 0:
            self.updateTimestamp()
            return 0
        return -1

    def ready(self, role):
        if self.table.ready(role) == 0:
            if self.table.isAllPlayerReady():
                self.table.start()
                self.state = Game.stateGaming
                self.curPlayer = "X"
                self.winner = None
            self.updateTimestamp()
            return 0
        return -1

    def play(self, role, position):
        ret = 0
        if role == self.curPlayer:
            ret = self.table.play(role, position)
            if ret >= 1:
                self.curPlayer = "X" if role == "O" else "O"
                if ret == 2:
                    self.state = Game.stateGameOver
                    self.winner = role
                    self.table.game_over()
                self.updateTimestamp()
        return ret
