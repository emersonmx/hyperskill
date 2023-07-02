from enum import Enum


class CoffeeMachine:
    class State(str, Enum):
        OFF = "off"
        MENU = "menu"
        BUY = "buy"
        FILL_WATER = "fill_water"
        FILL_MILK = "fill_milk"
        FILL_COFFEE = "fill_coffee"
        FILL_CUPS = "fill_cups"

        def __str__(self):
            return self.value

    class Command(str, Enum):
        MENU = "menu"
        BUY = "buy"
        FILL = "fill"
        TAKE = "take"
        REMAINING = "remaining"
        BACK = "back"
        EXIT = "exit"

        def __str__(self):
            return self.value

    def __init__(self) -> None:
        self._water = 400
        self._milk = 540
        self._coffee = 120
        self._cups = 9
        self._money = 550
        self._state = self.State.OFF

    @property
    def turned_on(self):
        return self._state != self.State.OFF

    def execute(self, input_):
        action = f"_handle_{self._state.value}_state"
        func = getattr(self, action, lambda _: None)
        func(input_)

    def _show_prompt(self):
        prompts = {
            self.State.MENU: "Write action (buy, fill, take, remaining, exit):",
            self.State.BUY: (
                "What do you want to buy? "
                "1 - espresso, 2 - latte, 3 - cappuccino, "
                "back - to main menu:"
            ),
            self.State.FILL_WATER: "Write how many ml of water you want to add:",
            self.State.FILL_MILK: "Write how many ml of milk you want to add:",
            self.State.FILL_COFFEE: (
                "Write how many grams of coffee beans you want to add:"
            ),
            self.State.FILL_CUPS: "Write how many disposable cups you want to add:",
        }
        print(prompts[self._state])

    def _handle_off_state(self, input_):
        if input_ == self.Command.MENU:
            self._state = self.State.MENU
            self._show_prompt()

    def _handle_menu_state(self, input_):
        if input_ == self.Command.BUY:
            self._state = self.State.BUY
            print()
            self._show_prompt()
        elif input_ == self.Command.FILL:
            self._state = self.State.FILL_WATER
            print()
            self._show_prompt()
        elif input_ == self.Command.TAKE:
            print()
            print(f"I gave you ${self._money}")
            print()
            self._money = 0
            self._show_prompt()
        elif input_ == self.Command.REMAINING:
            self._show_remaining()
            self._show_prompt()
        elif input_ == self.Command.EXIT:
            self._state = self.State.OFF

    def _handle_buy_state(self, input_):
        self._state = self.State.MENU

        water_usage, milk_usage, coffee_usage, cups_usage, price = 0, 0, 0, 1, 0
        if input_ == "1":
            water_usage, coffee_usage, price = 250, 16, 4
        elif input_ == "2":
            water_usage, milk_usage, coffee_usage, price = 350, 75, 20, 7
        elif input_ == "3":
            water_usage, milk_usage, coffee_usage, price = 200, 100, 12, 6
        elif input_ == self.Command.BACK:
            print()
            self._show_prompt()
            return
        elif input_ == self.Command.BUY:
            self._state = self.State.BUY
            self._show_prompt()
            return

        missing_resource = ""
        if water_usage > self._water:
            missing_resource = "water"
        elif milk_usage > self._milk:
            missing_resource = "milk"
        elif coffee_usage > self._coffee:
            missing_resource = "coffee"
        elif cups_usage > self._cups:
            missing_resource = "cups"

        if missing_resource == "":
            print("I have enough resources, making you a coffee!")
        else:
            print(f"Sorry, not enough {missing_resource}!")
            print()
            self._show_prompt()
            return

        self._water -= water_usage
        self._milk -= milk_usage
        self._coffee -= coffee_usage
        self._cups -= cups_usage
        self._money += price
        print()
        self._show_prompt()

    def _handle_fill_water_state(self, input_):
        self._water += int(input_)
        self._state = self.State.FILL_MILK
        self._show_prompt()

    def _handle_fill_milk_state(self, input_):
        self._milk += int(input_)
        self._state = self.State.FILL_COFFEE
        self._show_prompt()

    def _handle_fill_coffee_state(self, input_):
        self._coffee += int(input_)
        self._state = self.State.FILL_CUPS
        self._show_prompt()

    def _handle_fill_cups_state(self, input_):
        self._cups += int(input_)
        self._state = self.State.MENU
        print()
        self._show_prompt()

    def _show_remaining(self):
        print()
        print("The coffee machine has:")
        print(f"{self._water} ml of water")
        print(f"{self._milk} ml of milk")
        print(f"{self._coffee} g of coffee beans")
        print(f"{self._cups} disposable cups")
        print(f"${self._money} of money")
        print()


def main():
    machine = CoffeeMachine()
    machine.execute(CoffeeMachine.Command.MENU)
    while machine.turned_on:
        line = input()
        machine.execute(line)


if __name__ == "__main__":
    main()
