TIMEOUT = 5000

class Game:

    def __init__(self, board, k):
        self.winner = None
        self.turn = 0
        self.players = []
        self.board = board
        self.k = k

    '''
    Adds a player to the game
    '''
    def addPlayer(self, player, symbol):
        self.players.append((player, symbol))
        return self

    '''
    Plays through the game
    '''
    def play(self):
        for player in self.players:
            player.init(self.board)

        while not self.finished():
            self.step()

    '''
    Plays one step of the game
    '''
    def step(self):
        index = self.turn % len(self.players)

        #  make sure player is still in the game
        if self.players[index] == None: return

        # get player and have them move
        (player, symbol) = self.players[index]
        (move, remark) = timeout(
            func=player.move,
            args=(self.board),
            kwargs={},
            default=(None, "I give up.")
        )

        # check for timeout or give up
        if (move == None):
            self.players[index] = None
            return

        # make sure valid move
        (y, x) = move
        if self.board[y][x] != ' ':
            self.players[index] = None
            return
        else:
            self.board[y][x] = symbol

    '''
    Returns true if the game is finished
    '''
    def finished(self):

        # check cached winning result
        if self.winner != None: return True

        # TODO check for tie
        # if tied: return True

        # otherwise check if one player left
        playing = filter(lambda (player, symbol): player != None, self.players)
        if len(playing) == 1:
            self.winner = playing[0]
            return True

        # otherwise check for k in a row
        winningSymbol = has_winner(self.board, self.k)
        if winningSymbol == None: return False

        self.winner = filter(lambda (player, symbol): symbol == winningSymbol, self.players)[0]
        return True


def has_winner(board, k):
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
                if z == k: return symbol # WINNER

            # try a streak going 'right'
            for z in range(1, k):
                if x + z >= w: break
                if board[y][x + z] != symbol: break
                if z == k: return symbol # WINNER

            # try a streak going 'down and right'
            for z in range(1, k):
                if x + z >= w: break
                if y + z >= h: break
                if board[y + z][x + z] != symbol: break
                if z == k: return symbol # WINNER

            # try a streak going 'down'
            for z in range(1, k):
                if y + z >= h: break
                if board[y + z][x] != symbol: break
                if z == k: return symbol # WINNER
    return None

'''
Taken from hw5
'''
import sys
import time
import threading
def timeout(func, args=(), kwargs={}, default=None):
    '''This function will spawn a thread and run the given function using the args, kwargs and
    return the given default value if the timeout_duration is exceeded
    '''
    class PlayerThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default
        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except:
                print("Seems there was a problem with the time.")
                print(sys.exc_info())
                self.result = default

    pt = PlayerThread()

    pt.start()
    started_at = time.time()
    pt.join(TIMEOUT)
    ended_at = time.time()
    diff = ended_at - started_at

    print("Time used in makeMove: %0.4f seconds" % diff)
    if pt.isAlive():
        return None, "I can't think of a move"
    else:
        return pt.result
