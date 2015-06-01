from Game import Game
from WeightedPlayer import WeightedPlayer
from MinimaxPlayer import MinimaxPlayer
#
# board = [
#     [' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ']
# ]

board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

game = Game(board, 3)
game.addPlayer(WeightedPlayer(), 'X')
game.addPlayer(MinimaxPlayer(), 'O')

game.play()
# game.init()
# game.step()
# game.step()
# game.print_state()