from Game import Game
from WeightedPlayer import WeightedPlayer
from MinimaxPlayer import MinimaxPlayer

board = [
    [' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ']
]

game = Game(board, 4)
game.addPlayer(WeightedPlayer(), 'X')
game.addPlayer(MinimaxPlayer(), 'O')
game.addPlayer(MinimaxPlayer(), 'V')
game.addPlayer(WeightedPlayer(), 'A')

game.play()
# game.init()
# game.step()
# game.step()
# game.print_state()