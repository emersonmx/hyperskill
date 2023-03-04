print("How many pencils would you like to use:")
pencils = int(input())

players = ["John", "Jack"]
print(f"Who will be the first ({', '.join(players)}):")
player_index = players.index(input())

while pencils > 0:
    print("|" * pencils)
    player_name = players[player_index]
    print(f"{player_name}'s turn:")
    player_input = int(input())
    pencils -= player_input
    player_index = (player_index + 1) % len(players)
