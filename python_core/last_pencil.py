import random


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
        if name in ["John", "Jack"]:
            return name

        print("Choose between 'John' and 'Jack'")


def get_next_player(name):
    return "Jack" if name == "John" else "John"


def get_player_input(pencils):
    while True:
        try:
            player_input = int(input())
        except ValueError:
            print("Possible values: '1', '2' or '3'")
            continue

        if 1 <= player_input <= 3:
            if player_input <= pencils:
                return player_input
            else:
                print("Too many pencils were taken")
        else:
            print("Possible values: '1', '2' or '3'")


def get_bot_input(pencils):
    taken_pencils = random.randint(1, min(3, pencils))
    if pencils % 4 == 0:
        taken_pencils = 3
    elif pencils % 4 == 3:
        taken_pencils = 2
    elif pencils % 4 == 2:
        taken_pencils = 1

    print(taken_pencils)
    return taken_pencils


def main() -> int:
    print("How many pencils would you like to use:")
    pencils = get_pencil_amount()

    print("Who will be the first (John, Jack):")
    player = get_first_player()

    while pencils > 0:
        print("|" * pencils)
        print(f"{player}'s turn:")
        if player == "John":
            pencils -= get_player_input(pencils)
        else:
            pencils -= get_bot_input(pencils)
        player = get_next_player(player)

    print(f"{player} won!")

    return 0


if __name__ == "__main__":
    main()
