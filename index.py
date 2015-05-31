from Game import Game
from WeightedPlayer import WeightedPlayer

board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

game = Game(board, 3)
game.addPlayer(WeightedPlayer(), 'X')
game.addPlayer(WeightedPlayer(), 'O')

game.play()