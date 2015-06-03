from Player import Player
from re import *

class UserPlayer(Player):

    def __init__(self, name):
        Player.__init__(self, name)
        self.intro = ""

    def init(self, board, k, symbol, players):
        self.intro = raw_input("Introduce yourself: ")

    def name(self):
        return self.nm

    def introduce(self):
        return self.intro

    def move(self, board, turn, remarks):
        result = raw_input("Enter your move:    ")
        m = match("(\d+).*(\d+).*", result)
        while m is None:
            result = raw_input("Invalid, try again: ")
            m = match("(\d+).*(\d+).*", result)

        remark = raw_input("Enter your remark:  ")

        return (int(m.group(1)), int(m.group(2))), remark