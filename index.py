from Game import Game
from WeightedPlayer import WeightedPlayer
from MinimaxPlayer import MinimaxPlayer
from UserPlayer import UserPlayer

board = [
    [' ', ' ', ' ', ' ', ' '],
    [' ', '-', ' ', '-', ' '],
    [' ', ' ', '-', ' ', ' '],
    [' ', '-', ' ', '-', ' '],
    [' ', ' ', ' ', ' ', ' ']
]

game = Game(board, 4)
game.addPlayer(MinimaxPlayer(), 'O')
game.addPlayer(UserPlayer(), 'X')

game.play()
# game.init()
# game.step()
# game.step()
# game.print_state()