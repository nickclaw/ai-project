from Game import Game
from WeightedPlayer import WeightedPlayer
from MinimaxPlayer import MinimaxPlayer
from UserPlayer import UserPlayer

import sys
import json

if len(sys.argv) == 2:
    file = open(sys.argv[1], "r")

    try:
        data = json.loads(file.read())
        k = data["k"]
        board = data["board"]
        players = data["players"]
        for player in players:
            player["type"]
            player["symbol"]
    except:
        print("Invalid JSON")
else:
    print("python index.py <game.json>")
    exit(1)


game = Game(board, k)

for player in players:
    if player["type"] == "WeightedPlayer": game.addPlayer(WeightedPlayer(player["name"]), player["symbol"])
    if player["type"] == "MinimaxPlayer": game.addPlayer(WeightedPlayer(player["name"]), player["symbol"])
    if player["type"] == "UserPlayer": game.addPlayer(WeightedPlayer(player["name"]), player["symbol"])

game.play()