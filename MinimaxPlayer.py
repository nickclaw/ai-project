from Player import Player
from random import randint

INF = float('inf')

class MinimaxPlayer(Player):

    def __init__(self):
        Player.__init__(self)
        self.hashes = []
        self.dict = {}

    def init(self, board, k, symbol, players):
        Player.init(self, board, k, symbol, players)

        for i in range(self.h * self.w):
            self.hashes.append([])
            for j in range(len(players)):
                self.hashes[i].append(randint(0, 4294967296))


    def move(self, board, turn):
        index = turn % len(self.players)
        hash = self.zhash(board, index)
        (move, _) = self.minimax(board, turn, 4, hash)
        return (move, "")


    def minimax(self, board, turn, depth, hash):
        moves = get_moves(board)
        index = turn % len(self.players)
        (player, s) = self.players[index]

        # check for hash
        if hash in self.dict:
            return self.dict[hash]

        # base case
        if is_tie(board) or depth == 1:
            score = score_game(board, self.symbol, self.k)
            self.dict[hash] = None, score
            return None, score

        best_move = None
        best_score = -INF if s == self.symbol else INF
        sum = 0

        # otherwise try each move for current player
        for (y, x) in moves:
            state = deep_copy(board)
            state[y][x] = s
            new_hash = self.inc_hash(hash, y, x, index)

            # each state will have a score
            (_, score) = self.minimax(state, turn + 1, depth - 1, new_hash)

            if s == self.symbol:
                if best_score < score:
                    best_score = score
                    best_move = (y, x)
            else:
                if best_score > score:
                    best_score = score
                    best_move = (y, x)

        self.dict[hash] = (best_move, best_score)
        return best_move, best_score

    '''
    Hashes the current state
    '''
    def zhash(self, board, player_index):
        val = 0
        for y in range(self.h):
            for x in range(self.w):
                symbol = board[y][x]
                if symbol == " " or symbol == "-": continue
                val ^= self.hashes[y * self.h + x][player_index]

        return val

    '''
    Calculates the next hash given the current hash and player move
    '''
    def inc_hash(self, hash, y, x, player_index):
        return hash ^ self.hashes[y * self.h + x][player_index]
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
Returns true if the game is tied
'''
def is_tie(state):
    for row in state:
        for move in row:
            if move == " ":
                return False

    return True


def score_game(board, s, k):
    h = len(board)
    w = len(board[0])
    score = 0

    # for every coordinate
    for y in range(0, h):
        for x in range(0, w):

            # check symbol and make sure it's start of streak
            symbol = board[y][x]
            if symbol == " " or symbol == "-": continue
            mod = .5 if s == symbol else -2

            # try a streak going 'up and right'
            for z in range(0, k):
                if x + z >= w: break
                if y - z < 0: break
                if board[y - z][x + z] != symbol: break
                score += mod * (k ** z)

            # try a streak going 'right'
            for z in range(0, k):
                if x + z >= w: break
                if board[y][x + z] != symbol: break
                score += mod * (k ** z)


            # try a streak going 'down and right'
            for z in range(0, k):
                if x + z >= w: break
                if y + z >= h: break
                if board[y + z][x + z] != symbol: break
                score += mod * (k ** z)


            # try a streak going 'down'
            for z in range(0, k):
                if y + z >= h: break
                if board[y + z][x] != symbol: break
                score += mod * (k ** z)

    return score