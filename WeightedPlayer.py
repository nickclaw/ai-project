'''
Nicholas Clawson and Daniel Nakamura CSE 415, Spring 2015, University of Washington
Assignment 5
Our working K in a row player
'''

import random
from Player import Player

'''
Global Variables
'''

class WeightedPlayer(Player):

    def move(self, board):
        best_score = None
        best_move = None

         # for each coordinate that is empty
        for y in range(0, self.h):
            for x in range(0, self.w):
                if board[y][x] != " ": continue

                # evaluate the score _if_ we moved there
                new_state = deep_copy(board)
                new_state[y][x] = self.symbol
                score = self.eval(new_state)

                # if this is the first run
                # _or_ this position is better than our current best
                # save the new move information
                if best_score == None:
                    best_score = score
                    best_move = (y, x)
                elif score > best_score:
                    best_score = score
                    best_move = (y, x)

        return best_move, ""

    '''
    Evaluate the current state
    Positive return is good for player
    Negative return is bad for player
    '''
    def eval(self, state):
        myScore = 0
        theirScore = 0

        for (player, symbol) in self.players:
            for streak in self.build_list(state, symbol):
                count = streak_score(streak, state, symbol)
                if count > 0 and symbol == self.symbol:
                    myScore += self.k ** (count - 1)
                elif count > 0 and symbol != self.symbol:
                    theirScore += self.k ** (count)

        return myScore - theirScore / (len(self.players) - 1)

    def build_list(self, state, side):
        h = self.h
        w = self.w
        K = self.k
        STREAKS = []

        # for each coordinate on the board
        for y in range(0, h):
            for x in range(0, w):

                # try a streak going 'up and right'
                streak = []
                for z in range(0, K):
                    if x + z >= w: break
                    if y - z < 0: break
                    if state[y -z][x + z] != " " and state[y - z][x + z] != side: break
                    streak.append((x + z, y - z))
                if len(streak) == K: STREAKS.append(streak)

                # try the streak going 'right'
                streak = []
                for z in range(0, K):
                    if x + z >= w: break
                    if state[y][x + z] != " " and state[y][x + z] != side: break
                    streak.append((x + z, y))
                if len(streak) == K: STREAKS.append(streak)

                # try the streak going 'down right'
                streak = []
                for z in range(0, K):
                    if x + z >= w: break
                    if y + z >= h: break
                    if state[y + z][x + z] != " " and state[y + z][x + z] != side: break
                    streak.append((x + z, y + z))
                if len(streak) == K: STREAKS.append(streak)

                # try the streak going 'down'
                streak = []
                for z in range(0, K):
                    if y + z >= h: break
                    if state[y + z][x] != " " and state[y + z][x] != side: break
                    streak.append((x, y + z))
                if len(streak) == K: STREAKS.append(streak)
        return STREAKS


'''
Deep copy the two dimensional board state
'''
def deep_copy(state):
    return [s[:] for s in state]


'''
Count how many pieces of a side are in a streak
Assumed that the streak is valid (e.g. only " " or side pieces)
'''
def streak_score(streak, state, side):
    count = 0
    for x,y in streak:
        if state[y][x] == side: count += 1
        elif state[y][x] == " ": continue
    return count