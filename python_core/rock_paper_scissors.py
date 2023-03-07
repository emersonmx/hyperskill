import random


def main():
    inputs = ["rock", "paper", "scissors"]
    playerInput = input()
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


if __name__ == "__main__":
    main()
