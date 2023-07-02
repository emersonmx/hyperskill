import random

OPERATIONS = ["+", "-", "*"]
TASK_COUNT = 5
LEVEL_MESSAGES = {
    1: "simple operations with numbers 2-9",
    2: "integral squares of 11-29",
}


def make_simple_task():
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    op = random.choice(OPERATIONS)
    task = f"{a} {op} {b}"
    result = eval(task)
    return (task, result)


def make_integral_task():
    task = random.randint(11, 29)
    result = task * task
    return (str(task), result)


def input_level():
    while True:
        print("Which level do you want? Enter a number:")
        for k, v in LEVEL_MESSAGES.items():
            print(f"{k} - {v}")

        try:
            level = int(input())
            if level in LEVEL_MESSAGES:
                return (level, LEVEL_MESSAGES[level])
        except ValueError:
            pass
        print("Incorrect format.")


def input_answer():
    while True:
        try:
            return int(input())
        except ValueError:
            print("Wrong format! Try again.")


def main():
    tasks = []
    correct_answers = 0

    level_number, level_message = input_level()
    if level_number == 1:
        tasks = [make_simple_task() for _ in range(TASK_COUNT)]
    elif level_number == 2:
        tasks = [make_integral_task() for _ in range(TASK_COUNT)]

    for task, result in tasks:
        print(task)

        answer = input_answer()
        if answer == result:
            print("Right!")
            correct_answers += 1
        else:
            print("Wrong!")

    score_message = f"{correct_answers}/{len(tasks)}"
    save = input(
        " ".join(
            [
                f"Your mark is {score_message}.",
                "Would you like to save the result? Enter yes or no.\n",
            ]
        )
    )
    if save in ("yes", "YES", "y", "Yes"):
        username = input("What is your name?\n")
        with open("results.txt", "a+") as f:
            message = " ".join(
                [
                    f"{username}: {score_message} in level {level_number}",
                    f"({level_message}).\n",
                ]
            )
            f.write(message)

        print('The results are saved in "results.txt".')


if __name__ == "__main__":
    main()
