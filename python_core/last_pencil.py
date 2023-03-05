print("How many pencils would you like to use:")
pencils = 0
while True:
    pencils = input().strip()
    is_negative = pencils.startswith("-") and pencils[1:].isdigit()
    is_zero = pencils.isdigit() and pencils == "0"
    if is_negative or is_zero:
        print("The number of pencils should be positive")
    elif pencils.isdigit():
        pencils = int(pencils)
        break
    else:
        print("The number of pencils should be numeric")

players = ["John", "Jack"]
player_index = 0
print(f"Who will be the first ({', '.join(players)}):")
while True:
    player_name = input()
    if player_name in players:
        player_index = players.index(player_name)
        break
    else:
        print("Choose between 'John' and 'Jack'")

while pencils > 0:
    print("|" * pencils)
    player_name = players[player_index]
    print(f"{player_name}'s turn:")
    player_input = 0
    while True:
        player_input = input()
        if not player_input.isdigit():
            print("Possible values: '1', '2' or '3'")
            continue

        player_input = int(player_input)
        in_range = 1 <= player_input <= 3
        if in_range:
            if player_input <= pencils:
                break
            else:
                print("Too many pencils were taken")
        else:
            print("Possible values: '1', '2' or '3'")

    pencils -= player_input
    player_index = (player_index + 1) % len(players)

player_name = players[player_index]
print(f"{player_name} won!")
