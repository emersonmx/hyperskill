import random

WORDS = ["python", "java", "swift", "javascript"]

score = {"win": 0, "loss": 0}


def input_letter(guessed_word):
    while True:
        print()
        print("".join(guessed_word))
        letter = input("Input a letter: ")

        if len(letter) != 1:
            print("Please, input a single letter.")
        elif letter < "a" or letter > "z":
            print("Please, enter a lowercase letter from the English alphabet.")
        elif letter in guessed_word:
            print("You've already guessed this letter.")
        else:
            return letter


def play_game():
    global score

    secret_word = random.choice(WORDS)
    guessed_word = ["-"] * len(secret_word)
    attempts = 8
    while attempts > 0:
        letter = input_letter(guessed_word)
        found = False
        has_improvements = True
        for i, c in enumerate(secret_word):
            if c == letter:
                has_improvements = has_improvements and guessed_word[i] == "-"
                guessed_word[i] = c
                found = True

        if secret_word == "".join(guessed_word):
            break
        elif found and has_improvements:
            continue
        elif not has_improvements:
            print("No improvements.")
        else:
            print("That letter doesn't appear in the word.")

        attempts -= 1

    print()
    if secret_word == "".join(guessed_word):
        print(f"You guessed the word {secret_word}!")
        print("You survived!")
        score["win"] += 1
    else:
        print("You lost!")
        score["loss"] += 1


def show_results():
    global score
    print(f"You won: {score['win']} times")
    print(f"You lost: {score['loss']} times")


def main():
    print("H A N G M A N")

    while True:
        command = input(
            'Type "play" to play the game, "results" to show '
            'the scoreboard, and "exit" to quit: '
        )
        if command == "play":
            play_game()
        elif command == "results":
            show_results()
        elif command == "exit":
            break


if __name__ == "__main__":
    main()
