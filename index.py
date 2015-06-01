from Game import Game
from WeightedPlayer import WeightedPlayer
from MinimaxPlayer import MinimaxPlayer
from AlphaBetaPlayer import AlphaBetaPlayer

board = [
    [' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ']
]

game = Game(board, 3)
game.addPlayer(WeightedPlayer(), 'X')
game.addPlayer(AlphaBetaPlayer(), 'V')

game.play()