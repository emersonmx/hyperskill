import random

DRAW = 0
PLAYER1 = -1
PLAYER2 = 1


def clean_input():
    return input().strip()


def get_options():
    input_line = clean_input()
    if not input_line:
        return ["rock", "paper", "scissors"]

    options = input_line.split(",")
    return [o.strip() for o in options]


def get_result(options, player1, player2):
    i = options.index(player1)
    j = i + 1
    checks = options[j:] + options[:i]
    half_index = int(len(checks) / 2)
    if player1 == player2:
        return DRAW
    elif checks.index(player2) < half_index:
        return PLAYER2
    else:
        return PLAYER1


def get_score(player_name):
    with open("rating.txt", "r") as f:
        for line in f:
            name, score = line.strip().split()
            if player_name == name:
                return int(score)
    return 0


def calculate_score(result):
    if result == PLAYER1:
        return 100
    elif result == PLAYER2:
        return 0
    else:
        return 50


def main():
    print("Enter your name:")
    player_name = clean_input()
    print(f"Hello, {player_name}")
    score = get_score(player_name)

    options = get_options()
    available_options = options + ["!rating", "!exit"]

    print("Okay, let's start")
    while True:
        player1 = clean_input()
        if player1 not in available_options:
            print("Invalid input")
            continue
        if player1 == "!rating":
            print(f"Your rating: {score}")
            continue
        if player1 == "!exit":
            break

        player2 = random.choice(options)

        result = get_result(options, player1, player2)
        score += calculate_score(result)
        if result == PLAYER1:
            print(f"Well done. The computer chose {player2} and failed")
        elif result == PLAYER2:
            print(f"Sorry, but the computer chose {player2}")
        else:
            print(f"There is a draw ({player1})")

    print("Bye!")


if __name__ == "__main__":
    main()
