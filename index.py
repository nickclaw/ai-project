from Game import Game
from WeightedPlayer import WeightedPlayer
from MinimaxPlayer import MinimaxPlayer

board = [
    [' ', ' ', ' ', ' ', ' '],
    [' ', '-', ' ', '-', ' '],
    [' ', ' ', '-', ' ', ' '],
    [' ', '-', ' ', '-', ' '],
    [' ', ' ', ' ', ' ', ' ']
]

game = Game(board, 4)
game.addPlayer(MinimaxPlayer(), 'O')
game.addPlayer(WeightedPlayer(), 'X')

game.play()
# game.init()
# game.step()
# game.step()
# game.print_state()