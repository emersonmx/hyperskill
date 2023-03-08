import random


def clean_input():
    return input().strip()


def main():
    inputs = ["rock", "paper", "scissors"]
    options = inputs + ["!exit"]

    while True:
        playerInput = clean_input()
        if playerInput not in options:
            print("Invalid input")
            continue
        if playerInput == "!exit":
            break

        computerInput = random.choice(inputs)

        i = inputs.index(playerInput)
        j = i + 1
        checks = inputs[j:] + inputs[:i]

        if playerInput == computerInput:
            print(f"There is a draw ({playerInput})")
        elif checks.index(computerInput) == 0:
            print(f"Sorry, but the computer chose {computerInput}")
        elif checks.index(computerInput) == 1:
            print(f"Well done. The computer chose {computerInput} and failed")

    print("Bye!")


if __name__ == "__main__":
    main()
