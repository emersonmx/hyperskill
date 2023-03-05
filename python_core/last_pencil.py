PLAYERS = ["John", "Jack"]


def get_pencil_amount():
    while True:
        try:
            pencils = int(input())
        except ValueError:
            print("The number of pencils should be numeric")
            continue

        if pencils > 0:
            return pencils

        print("The number of pencils should be positive")


def get_first_player():
    while True:
        name = input()
        if name in PLAYERS:
            return name

        print("Choose between 'John' and 'Jack'")


def get_player_index(name):
    return PLAYERS.index(name)


def get_player_name(index):
    return PLAYERS[index]


def get_next_player(name):
    index = get_player_index(name)
    return get_player_name((index + 1) % len(PLAYERS))


def get_player_input(pencils):
    while True:
        try:
            player_input = int(input())
        except ValueError:
            print("Possible values: '1', '2' or '3'")
            continue

        in_range = 1 <= player_input <= 3
        if in_range:
            if player_input <= pencils:
                return player_input
            else:
                print("Too many pencils were taken")
        else:
            print("Possible values: '1', '2' or '3'")


def main() -> int:
    print("How many pencils would you like to use:")
    pencils = get_pencil_amount()

    print(f"Who will be the first ({', '.join(PLAYERS)}):")
    player = get_first_player()

    while pencils > 0:
        print("|" * pencils)
        print(f"{player}'s turn:")
        pencils -= get_player_input(pencils)
        player = get_next_player(player)

    print(f"{player} won!")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
