import random


def main():
    inputs = ["rock", "paper", "scissors"]
    playerInput = input()
    computerInput = random.choice(inputs)

    i = inputs.index(playerInput)
    j = i + 1
    check_list = inputs[j:] + inputs[:i]

    if playerInput == computerInput:
        print(f"There is a draw ({playerInput})")
    elif check_list.index(computerInput) == 0:
        print(f"Sorry, but the computer chose {computerInput}")
    elif check_list.index(computerInput) == 1:
        print(f"Well done. The computer chose {computerInput} and failed")


if __name__ == "__main__":
    main()
