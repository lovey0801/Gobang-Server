import json


class Player:

    def __init__(self, name):
        self.name = name
        self.role = None
        self.readyState = False
        self.playHistory = []

    def setRole(self, role):
        self.role = role

    def ready(self):
        self.readyState = True

    def start(self):
        self.playHistory = []

    def play(self, position):
        self.playHistory.append(position)

    def toDict(self):
        return {
            "name": self.name,
            "role": self.role,
            "readyState": self.readyState
        }

