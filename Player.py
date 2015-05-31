
class Player:

    def __init__(self):
        self.k = 0
        self.symbol = ""

    def init(self, board, k, symbol):
        self.k = k
        self.symbol = symbol

    def move(self, board):
        return (0, 0), ""