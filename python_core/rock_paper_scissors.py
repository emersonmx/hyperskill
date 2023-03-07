def main():
    playerInput = input()

    result = ""
    if playerInput == "paper":
        result = "scissors"
    elif playerInput == "scissors":
        result = "rock"
    elif playerInput == "rock":
        result = "paper"

    print(f"Sorry, but the computer chose {result}")


if __name__ == "__main__":
    main()
