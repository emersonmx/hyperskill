import math


def calculate_annuity_payment(p, i, n):
    return p * ((i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1))


def calculate_loan_principal(a, i, n):
    return a / ((i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1))


def calculate_number_of_payments(a, p, i):
    return math.log(a / (a - i * p), 1 + i)


def calculate_differentiated_payments(p, i, n, m):
    return (p / n) + i * (p - ((p * (m - 1)) / n))


print(
    """What do you want to calculate?
type "n" for number of monthly payments,
type "a" for annuity monthly payment amount,
type "p" for loan principal:"""
)
option = input()

if option == "n":
    print("Enter the loan principal:")
    loan_principal = float(input())
    print("Enter the monthly payment:")
    annuity_payment = float(input())
    print("Enter the loan interest:")
    loan_interest = float(input()) / 12 / 100

    n_payments = math.ceil(
        calculate_number_of_payments(
            annuity_payment,
            loan_principal,
            loan_interest,
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
elif option == "a":
    print("Enter the loan principal:")
    loan_principal = float(input())
    print("Enter the number of periods:")
    periods = float(input())
    print("Enter the loan interest:")
    loan_interest = float(input()) / 12 / 100

    payment = math.ceil(
        calculate_annuity_payment(
            loan_principal,
            loan_interest,
            periods,
        )
    )

    print(f"Your monthly payment = {payment}!")
elif option == "p":
    print("Enter the annuity payment:")
    annuity_payment = float(input())
    print("Enter the number of periods:")
    periods = float(input())
    print("Enter the loan interest:")
    loan_interest = float(input()) / 12 / 100

    loan_principal = round(
        calculate_loan_principal(
            annuity_payment,
            loan_interest,
            periods,
        )
    )

    print(f"Your loan principal = {loan_principal}!")
