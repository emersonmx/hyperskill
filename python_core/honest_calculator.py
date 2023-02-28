MSG_0 = "Enter an equation"
MSG_1 = "Do you even know what numbers are? Stay focused!"
MSG_2 = (
    "Yes ... an interesting math operation. "
    "You've slept through all classes, haven't you?"
)
MSG_3 = "Yeah... division by zero. Smart move..."
MSG_4 = "Do you want to store the result? (y / n):"
MSG_5 = "Do you want to continue calculations? (y / n):"
MSG_6 = " ... lazy"
MSG_7 = " ... very lazy"
MSG_8 = " ... very, very lazy"
MSG_9 = "You are"
MSG_10 = "Are you sure? It is only one digit! (y / n)"
MSG_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"
MSG_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"
OPERATORS = "+-*/"

memory = 0


def check(x, y, operator):
    message = ""
    if is_one_digit(x) and is_one_digit(y):
        message += MSG_6
    if (x == 1 or y == 1) and operator == "*":
        message += MSG_7
    if (x == 0 or y == 0) and (operator in "*+-"):
        message += MSG_8

    if message:
        message = MSG_9 + message
        print(message)


def is_one_digit(value):
    return -10 < value < 10 and value.is_integer()


running = True
while running:
    print(MSG_0)
    calc = input().split()
    x = calc[0]
    oper = calc[1]
    y = calc[2]

    if x == "M":
        x = memory
    if y == "M":
        y = memory

    try:
        x = float(x)
        y = float(y)
    except ValueError:
        print(MSG_1)
        continue

    if oper in OPERATORS:
        check(x, y, oper)
        result = 0
        if oper == "+":
            result = x + y
        elif oper == "-":
            result = x - y
        elif oper == "*":
            result = x * y
        elif oper == "/" and y != 0:
            result = x / y
        else:
            print(MSG_3)
            continue
        print(result)

        while True:
            print(MSG_4)
            answer = input()
            if answer == "y":
                if is_one_digit(result):
                    message_index = 0
                    messages = [MSG_10, MSG_11, MSG_12]

                    while True:
                        print(messages[message_index])
                        answer = input()
                        if answer == "y":
                            if message_index < len(messages) - 1:
                                message_index += 1
                            else:
                                memory = result
                                break
                        elif answer == "n":
                            break
                else:
                    memory = result
                break
            elif answer == "n":
                break

        while True:
            print(MSG_5)
            answer = input()
            if answer == "y":
                break
            elif answer == "n":
                running = False
                break

        if not running:
            break
    else:
        print(MSG_2)
