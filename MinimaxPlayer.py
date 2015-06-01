from Player import Player

INF = float('inf')

class MinimaxPlayer(Player):

    def init(self, board, k, symbol, players):
        Player.init(self, board, k, symbol, players)


    def move(self, board, turn):
        (move, _) = self.minimax(board, turn)
        return (move, "")


    def minimax(self, board, turn):
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
        best_score = -INF if s == self.symbol else INF
        sum = 0

        # otherwise try each move for current player
        for (y, x) in moves:
            state = deep_copy(board)
            state[y][x] = s

            # each state will have a score
            (_, score) = self.minimax(state, turn + 1)

            if (s == self.symbol):
                if best_score < score:
                    best_score = score
                    best_move = (y, x)
            else:
                if best_score > score:
                    best_score = score
                    best_move = (y, x)

        return best_move, best_score



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