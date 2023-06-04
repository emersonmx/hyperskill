import random


def input_people_count():
    try:
        return int(input())
    except Exception:  # noqa
        return 0


def input_bill_value():
    try:
        return float(input())
    except Exception:  # noqa
        return 0


def calculate_split_value(value, count):
    return round(value / count, 2)


print("Enter the number of friends joining (including you):")
people_count = input_people_count()

if people_count <= 0:
    print("No one is joining for the party")
else:
    peoples = {}
    print("Enter the name of every friend (including you), each on a new line:")
    for _ in range(people_count):
        name = input()
        peoples[name] = 0

    print("Enter the total bill value:")
    bill_value = input_bill_value()
    split_value = calculate_split_value(bill_value, people_count)
    peoples = {p: split_value for p in peoples}

    print('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
    who_is_lucky_choice = input()
    who_is_lucky_name = ""
    if who_is_lucky_choice == "Yes":
        who_is_lucky_name = random.choice(list(peoples))
        print(f"{who_is_lucky_name} is the lucky one!")
        split_value = calculate_split_value(bill_value, people_count - 1)
        peoples = {p: split_value for p in peoples}
        peoples[who_is_lucky_name] = 0
    else:
        print("No one is going to be lucky")

    print(peoples)
