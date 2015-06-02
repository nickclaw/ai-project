from Player import Player
from random import randint
import lang

INF = float('inf')

class MinimaxPlayer(Player):

    def __init__(self):
        Player.__init__(self)
        self.hashes = []
        self.dict = {}
        self.memory = {}
        self.hobbies = {}


    def init(self, board, k, symbol, players):
        Player.init(self, board, k, symbol, players)
        hobbies = {0: 'work', 1: 'drink', 2: 'play football', 3: 'snowboard'}

        for i in range(self.h * self.w):
            self.hashes.append([])
            for j in range(len(players)):
                self.hashes[i].append(randint(0, 4294967296))


    def move(self, board, turn, remarks):
        index = turn % len(self.players)
        hash = self.zhash(board, index)
        (move, _) = self.minimax(board, turn, -INF, INF, 5, hash)
        return (move, "")


    def minimax(self, board, turn, a, b, depth, hash):
        moves = get_moves(board)
        index = turn % len(self.players)
        (player, s) = self.players[index]

        # check for hash
        if hash in self.dict:
            return self.dict[hash]

        # base case
        if is_tie(board) or depth == 0:
            score = score_game(board, self.symbol, self.k)
            self.dict[hash] = None, score
            return None, score

        best_move = None
        best_score = a if s == self.symbol else b
        sum = 0

        # otherwise try each move for current player
        for (y, x) in moves:
            state = deep_copy(board)
            state[y][x] = s
            new_hash = self.inc_hash(hash, y, x, index)

            # each state will have a score
            (_, score) = self.minimax(state, turn + 1, a, b, depth - 1, new_hash)

            if s == self.symbol:
                if best_score < score:
                    best_score = score
                    best_move = (y, x)
                a = max(a, score)
                if b <= a:
                    break

            else:
                if best_score > score:
                    best_score = score
                    best_move = (y, x)
                b = min(b, score)
                if b <= a:
                    break

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
    Responds to opponent based of their conversation
    '''
    def respond(self, input):
        hi = ['hello', 'hi', 'howdy', 'hey']
        wordlist = lang.remove_punctuation(input).split(' ')
        # undo any initial capitalization:
        wordlist[0] = wordlist[0].lower()
        mappedWordlist = you_me_map(wordlist)
        mappedWordlist[0] = mappedWordlist[0].capitalize()
        if 'name' in self.memory:
            self.memory['name'] = stringify(wordlist)
            return "Hi " + stringify(wordlist)
        if wordlist[0]=='':
            return "Please tell me something about you."
        if wordlist[0] in hi:
            return hi[randint(0, len(hi) - 1)]
        if wordlist[0:2] == ['i','am']:
            return ("Please tell me why you are " +\
                  stringify(mappedWordlist[2:]) + '.')
        if wpred(wordlist[0]):
            print(wordlist)
            if 'name' in wordlist and 'your' in wordlist:
                ext = "what is your name?"
                if 'name' in self.memory:
                    ext = "but you should already know that " + self.memory['name']
                return "My name is Ray the Bartender, " + ext
            if 'hobby' in wordlist:
                rand = randint(0, len(self.hobbies) - 1)
                if 'hobbies' in self.memory and self.memory['hobbies'] == self.hobbies[rand]:
                    rand = (rand + 1) % len(self.hobbies)
                self.memory['hobbies'] = self.hobbies[rand]
                return "I like to " + self.hobbies[rand] + ' in my free time.'
            return ("You tell me " + wordlist[0] + ".")
        if 'name' in wordlist:
            if 'name' in self.memory:
                name = getName(wordlist)
                if self.memory['name'] == name:
                    self.memory['cutoff'] = True
                    return "You already told me your name is " + self.memory['name'] + "... Are you drunk? You're cut off."
                return "You told me you're name was " + self.memory['name'] + ". Did you lie?"
            else:
                name = getName(wordlist)
                self.memory['name'] = name
                if name == '':
                    return "I'm sorry what was your name?"
                return "Hi, " + self.memory['name'] + " can I make you a drink?"
        if wordlist[0:2] == ['i','have']:
            return ("How do you possibly have " +\
                  stringify(mappedWordlist[2:]) + '.')
        if wordlist[0:2] == ['i','feel']:
            feelings = ['fat', 'smart', 'cool', 'dumb', 'stupid', 'lazy', 'bored', 'loved', 'happy']
            for word in wordlist[2:]:
                if word in feelings:
                    return "Hey, everyone feels " + word + " sometimes. Have another drink."
            return "I'm not sure I know that feeling. Sorry :("
        if 'because' in wordlist:
            return "I don't need your reasons, just tell me you need another drink."
        if 'yes' in wordlist:
            return "Yes, you'd like another drink? Coming right up."
        if verbp(wordlist[0]):
            return ("If i go " +\
                  stringify(mappedWordlist) + ' with you will you leave me alone?')
        if wordlist[0:3] == ['do','you','think']:
            return "After as many drinks as you've had, I'm surprised you can think at all."
        if wordlist[0:2]==['can','you'] or wordlist[0:2]==['could','you']:
            return "Perhaps I " + wordlist[0] + ' ' +\
                 stringify(mappedWordlist[2:]) + ' however you never know the repercussions of ' +\
                   stringify(mappedWordlist[2:])
        if 'love' in wordlist:
            return "Hey, the bar probably isn't the best place to be talking of love."
        if 'no' in wordlist:
            return "Why don't you try saying 'yes' every so often?"
        if 'maybe' in wordlist:
            return "Give it a try, you never know till you try."
        if 'you' in mappedWordlist or 'You' in mappedWordlist:
            return stringify(mappedWordlist) + '.'
        return punt()

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
            symbols = [" ", symbol]
            if symbol == " " or symbol == "-": continue
            mod = 1 if s == symbol else -5

            # try a streak going 'up and right'
            sum = 0
            for z in range(0, k):
                if x + z >= w or y - z < 0 or board[y - z][x + z] not in symbols:
                    sum = 0
                    break
                if board[y - z][x + z] == symbol:
                    sum += 1
            score += mod * (k ** sum)

            # try a streak going 'right'
            sum = 0
            for z in range(0, k):
                if x + z >= w or board[y][x + z] not in symbols:
                    sum = 0
                    break
                if board[y][x + z] == symbol:
                    sum += 1
            score += mod * (k ** sum)


            # try a streak going 'down and right'
            sum = 0
            for z in range(0, k):
                if x + z >= w or y + z >= h or board[y + z][x + z] != symbol:
                    sum = 0
                    break
                if board[y + z][x + z] == symbol:
                    sum += 1
            score += mod * (k ** sum)


            # try a streak going 'down'
            sum = 0
            for z in range(0, k):
                if y + z >= h or board[y + z][x] != symbol:
                    sum = 0
                    break
                if board[y + z][x] == symbol:
                    sum += 1
            score += mod * (k ** sum)

    return score

def wpred(w):
    'Returns True if w is one of the question words.'
    return (w in ['what', 'when','why','where','how'])

def dpred(w):
    'Returns True if w is an auxiliary verb.'
    return (w in ['do','can','should','would'])

def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)

def you_me(w):
    'Changes a word from 1st to 2nd person or vice-versa.'
    try:
        result = lang.case_map[w]
    except KeyError:
        result = w
    return result

def you_me_map(wordlist):
    'Applies YOU-ME to a whole sentence or phrase.'
    return [you_me(w) for w in wordlist]

def verbp(w):
    'Returns True if w is one of these known verbs.'
    return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add'])

PUNTS = ['What kind of move was that?',
         'Do I need to take that beer away from you?',
         'What does that indicate?',
         'I will open a tab for you.']

punt_count = 0
def punt():
    'Returns one from a list of default responses.'
    global punt_count
    punt_count += 1
    return PUNTS[punt_count % 6]

def getName(wordlist):
    name = ""
    for word in wordlist:
        if word[0].isupper():
            name = word
    return name
