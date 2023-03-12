import random


def clean_input():
    return input().strip()


def get_result(inputs, player1, player2):
    i = inputs.index(player1)
    j = i + 1
    checks = inputs[j:] + inputs[:i]
    if player1 == player2:
        return None
    elif checks.index(player2) == 0:
        return player2
    elif checks.index(player2) == 1:
        return player1


def fetch_score(player_name):
    with open("rating.txt", "r") as f:
        for line in f:
            name, score = line.strip().split()
            if player_name == name:
                return int(score)
    return 0


def calculate_score(player1, player2, result):
    if result == player1:
        return 100
    elif result == player2:
        return 0
    else:
        return 50


def main():
    inputs = ["rock", "paper", "scissors"]
    options = inputs + ["!rating", "!exit"]

    print("Enter your name:")
    player_name = clean_input()
    print(f"Hello, {player_name}")
    score = fetch_score(player_name)
    print(score)

    while True:
        player1 = clean_input()
        if player1 not in options:
            print("Invalid input")
            continue
        if player1 == "!rating":
            print(f"Your rating: {score}")
            continue
        if player1 == "!exit":
            break

        player2 = random.choice(inputs)

        result = get_result(inputs, player1, player2)
        score += calculate_score(player1, player2, result)
        if result == player1:
            print(f"Well done. The computer chose {player2} and failed")
        elif result == player2:
            print(f"Sorry, but the computer chose {player2}")
        else:
            print(f"There is a draw ({player1})")

    print("Bye!")


if __name__ == "__main__":
    main()
