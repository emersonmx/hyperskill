import requests


def fetch_data(currency):
    url = f"http://www.floatrates.com/daily/{currency.lower()}.json"
    if response := requests.get(url, timeout=5):
        return response.json()
    return None


def main():
    cache = {}
    from_currency = input()

    if data := fetch_data(from_currency):
        if from_currency == "usd":
            cache["eur"] = data["eur"]["rate"]
        elif from_currency == "eur":
            cache["usd"] = data["usd"]["rate"]
        else:
            cache["usd"] = data["usd"]["rate"]
            cache["eur"] = data["eur"]["rate"]

    while True:
        to_currency_input = input().upper()
        if to_currency_input == "":
            break

        to_currency = to_currency_input.lower()
        amount = float(input())

        print("Checking the cache...")
        if to_currency in cache:
            print("Oh! It is in the cache!")
        elif data := fetch_data(from_currency):
            print("Sorry, but it is not in the cache!")
            cache[to_currency] = data[to_currency]["rate"]
        else:
            print("Error!")

        rate = cache[to_currency]
        result = rate * amount
        print(f"You received {result:.2f} {to_currency_input}.")


if __name__ == "__main__":
    main()
