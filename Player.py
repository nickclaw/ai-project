
class Player:

    def __init__(self):
        self.k = 0
        self.symbol = ""
        self.h = 0
        self.w = 0
        self.players = []

    def init(self, board, k, symbol, players):
        self.h = len(board)
        self.w = len(board[0])
        self.k = k
        self.symbol = symbol
        self.players = players

    def move(self, board):
        return (0, 0), ""