import argparse
import math


def calculate_annuity_payment(p, i, n):
    return p * ((i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1))


def calculate_loan_principal(a, i, n):
    return a / ((i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1))


def calculate_number_of_payments(a, p, i):
    return math.log(a / (a - i * p), 1 + i)


def calculate_differentiated_payments(p, i, n, m):
    return (p / n) + i * (p - ((p * (m - 1)) / n))


def has_errors(args):
    args_tuple = (
        args.type,
        args.payment,
        args.principal,
        args.periods,
        args.interest,
    )
    type_, payment, _, periods, interest = args_tuple
    if type_ not in ["annuity", "diff"]:
        return True
    if len([a for a in args_tuple if a is not None]) != 4:
        return True
    if type_ == "diff":
        if payment is not None:
            return True
        if periods < 0:
            return True
    if type_ == "annuity" and interest is None:
        return True
    return False


def show_annuity_payment(args):
    payment = args.payment
    principal = args.principal
    periods = args.periods
    interest = args.interest / 12 / 100

    payment = math.ceil(
        calculate_annuity_payment(
            principal,
            interest,
            periods,
        )
    )

    print(f"Your monthly payment = {payment}!")


def show_loan_principal(args):
    payment = args.payment
    periods = args.periods
    interest = args.interest / 12 / 100

    loan_principal = round(
        calculate_loan_principal(
            payment,
            interest,
            periods,
        )
    )

    print(f"Your loan principal = {loan_principal}!")


def show_number_of_payments(args):
    payment = args.payment
    principal = args.principal
    interest = args.interest / 12 / 100

    n_payments = math.ceil(
        calculate_number_of_payments(
            payment,
            principal,
            interest,
        )
    )
    years, months = divmod(n_payments, 12)

    years_message = ""
    if years == 1:
        years_message += f"{years} year"
    elif years > 1:
        years_message += f"{years} years"

    month_message = ""
    if months == 1:
        month_message += f"{months} month"
    elif months > 1:
        month_message += f"{months} months"

    if years_message and month_message:
        years_month_message = f"{years_message} and {month_message}"
    else:
        years_month_message = f"{years_message}{month_message}".strip()

    message = f"It will take {years_month_message} to repay this loan!"
    print(message)
    print()
    overpayment = int(n_payments * payment - principal)
    print(f"Overpayment = {overpayment}")


def show_differentiated_payments(args):
    principal = args.principal
    periods = args.periods
    interest = args.interest / 12 / 100
    sum = 0
    for month in range(1, args.periods + 1):
        result = int(
            math.ceil(
                calculate_differentiated_payments(
                    principal,
                    interest,
                    periods,
                    month,
                )
            )
        )
        sum += result
        print(f"Month {month}: payment is {result}")

    print()
    print(f"Overpayment = {int(sum - principal)}")


parser = argparse.ArgumentParser()
parser.add_argument("--type")
parser.add_argument("--payment", type=float)
parser.add_argument("--principal", type=float)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)

args = parser.parse_args()

if has_errors(args):
    print("Incorrect parameters")
elif args.type == "annuity":
    if args.payment is None:
        show_annuity_payment(args)
    if args.principal is None:
        show_loan_principal(args)
    if args.periods is None:
        show_number_of_payments(args)
elif args.type == "diff":
    show_differentiated_payments(args)
