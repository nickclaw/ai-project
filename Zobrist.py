__author__ = 'danielnakamura'

from random import randint
from Player import Player


class ZobristPlayer(Player):
    def __init__(self):
        Player.__init__(self)
        self.zobrist = {}
        self.board_size = 0
        self.zobristnum = None

    def init(self, board, k, symbol, players):
        Player.init(self, board, k, symbol, players)
        self.board_size = self.h * self.k
        self.zobristnum = [[0]*len(self.players)]*self.board_size
        self.myinit()


    def myinit(self):
        for i in range(self.board_size):
            for j in range(len(self.players)):
                self.zobristnum[i][j] = randint(0, 4294967296)

    # Hash the board to an int.
    def zhash(self, board):
        val = 0
        for i in range(self.h):
            for j in range(self.w):
                piece = None
                for player in range(len(self.players)):
                    if (board[i][j] == self.players[player].symbol): piece = player
                if(piece != None): val ^= self.zobristnum[i][piece]
        return val

    def move(self, board, turn):
        (move, _) = self.minimax(board, turn)
        return (move, "")


    def minimax(self, board, turn):
        hash_val = self.zhash(board)
        if hash_val in self.zobrist: return self.zobrist[hash_val]
        moves = get_moves(board)
        index = turn % len(self.players)
        (player, s) = self.players[index]

        # if tie 0
        # if we lose -1
        # if we win +1
        if is_tie(board): return None, 0
        winner = get_winner(board, self.k)
        if winner == self.symbol: return None, 1
        elif winner is not None: return None, -1

        best_move = None
        best_score = 0
        sum = 0

        # otherwise try each move for current player
        for (y, x) in moves:
            state = deep_copy(board)
            state[y][x] = s

            (_, score) = self.minimax(state, turn + 1)
            sum += score
            if best_move is None or score > best_score:
                best_move = (y, x)
                best_score = score

        return best_move, sum



'''
Deep copy the two dimensional board state
'''
def deep_copy(state):
    return [s[:] for s in state]

'''
Returns an array of all possible moves
'''
def get_moves(state):
    h = len(state)
    w = len(state[0])
    moves = []
    for y in range(0, h):
        for x in range(0, w):
            if state[y][x] == " ":
                moves.append((y, x))
    return moves


'''
Gets the symbol of the winner if there is one
Otherwise return None
'''
def get_winner(board, k):
    h = len(board)
    w = len(board[0])

    # for every coordinate
    for y in range(0, h):
        for x in range(0, w):

            # check symbol and make sure it's start of streak
            symbol = board[y][x]
            if symbol == " " or symbol == "-": break

            # try a streak going 'up and right'
            for z in range(1, k):
                if x + z >= w: break
                if y - z < 0: break
                if board[y - z][x + z] != symbol: break
                if z + 1 == k: return symbol # WINNER

            # try a streak going 'right'
            for z in range(1, k):
                if x + z >= w: break
                if board[y][x + z] != symbol: break
                if z + 1 == k: return symbol # WINNER

            # try a streak going 'down and right'
            for z in range(1, k):
                if x + z >= w: break
                if y + z >= h: break
                if board[y + z][x + z] != symbol: break
                if z + 1 == k: return symbol # WINNER

            # try a streak going 'down'
            for z in range(1, k):
                if y + z >= h: break
                if board[y + z][x] != symbol: break
                if z + 1 == k: return symbol # WINNER
    return None


'''
Returns true if the game is tied
'''
def is_tie(state):
    for row in state:
        for move in row:
            if move == " ":
                return False

    return True