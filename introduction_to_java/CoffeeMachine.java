import java.util.Scanner;

public class CoffeeMachine {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Machine machine = new Machine();

        machine.execute("on");
        while (machine.isTurnedOn()) {
            machine.execute(scanner.nextLine());
        }
    }
}

class Machine {
    enum State {
        MENU, BUY, FILL_WATER, FILL_MILK, FILL_COFFEE, FILL_CUPS, OFF,
    }

    private State state = State.OFF;
    private int moneyAmount = 550;
    private int waterAmount = 400;
    private int milkAmount = 540;
    private int coffeeAmount = 120;
    private int cupsAmount = 9;

    public boolean isTurnedOn() {
        return state != State.OFF;
    }

    public void execute(String input) {
        switch (state) {
            case MENU:
                menuAction(input);
                break;
            case BUY:
                buyAction(input);
                break;
            case FILL_WATER:
                fillWaterAction(input);
                break;
            case FILL_MILK:
                fillMilkAction(input);
                break;
            case FILL_COFFEE:
                fillCoffeeAction(input);
                break;
            case FILL_CUPS:
                fillCupsAction(input);
                break;
            case OFF:
                offAction(input);
                break;
            default:
                break;
        }
    }

    private void showEmptyLine() {
        System.out.println();
    }

    private void showMenu() {
        System.out.println("Write action (buy, fill, take, remaining, exit):");
        state = State.MENU;
    }

    private void showBuy() {
        System.out.println("""
                What do you want to buy? \
                1 - espresso, 2 - latte, 3 - cappuccino, \
                back - to main menu:""");
        state = State.BUY;
    }

    private void showFillWater() {
        System.out.println("Write how many ml of water you want to add:");
        state = State.FILL_WATER;
    }

    private void showFillMilk() {
        System.out.println("Write how many ml of milk you want to add:");
        state = State.FILL_MILK;
    }

    private void showFillCoffee() {
        System.out.println("Write how many grams of coffee beans you want to add:");
        state = State.FILL_COFFEE;
    }

    private void showFillCups() {
        System.out.println("Write how many disposable cups you want to add:");
        state = State.FILL_CUPS;
    }

    private void showRemaining() {
        System.out.println("The coffee machine has:");
        System.out.println("%d ml of water".formatted(waterAmount));
        System.out.println("%d ml of milk".formatted(milkAmount));
        System.out.println("%d g of coffee beans".formatted(coffeeAmount));
        System.out.println("%d disposable cups".formatted(cupsAmount));
        System.out.println("$%d of money".formatted(moneyAmount));
        state = State.MENU;
    }

    private void menuAction(String input) {
        switch (input) {
            case "buy":
                showEmptyLine();
                showBuy();
                break;
            case "fill":
                showEmptyLine();
                showFillWater();
                break;
            case "take":
                showEmptyLine();
                takeAction();
                showEmptyLine();
                showMenu();
                break;
            case "remaining":
                showEmptyLine();
                showRemaining();
                showEmptyLine();
                showMenu();
                break;
            case "exit":
                state = State.OFF;
                break;
            default:
                showEmptyLine();
                showMenu();
                break;
        }
    }

    private void takeAction() {
        System.out.println("I gave you $%d".formatted(moneyAmount));
        moneyAmount = 0;
        state = State.MENU;
    }

    private void buyAction(String input) {
        switch (input) {
            case "1":
                makeEspresso();
                showEmptyLine();
                showMenu();
                break;
            case "2":
                makeLatte();
                showEmptyLine();
                showMenu();
                break;
            case "3":
                makeCappuccino();
                showEmptyLine();
                showMenu();
                break;
            case "back":
                showEmptyLine();
                showMenu();
                break;
            default:
                showEmptyLine();
                showBuy();
                break;
        }
    }

    private void fillWaterAction(String input) {
        int value = Integer.parseInt(input);
        waterAmount += value;
        showFillMilk();
    }

    private void fillMilkAction(String input) {
        int value = Integer.parseInt(input);
        milkAmount += value;
        showFillCoffee();
    }

    private void fillCoffeeAction(String input) {
        int value = Integer.parseInt(input);
        coffeeAmount += value;
        showFillCups();
    }

    private void fillCupsAction(String input) {
        int value = Integer.parseInt(input);
        cupsAmount += value;
        showEmptyLine();
        showMenu();
    }

    private void offAction(String input) {
        if (input.equals("on")) {
            showMenu();
        }
    }

    private String getMissingResource(int water, int milk, int coffee) {
        if (water > waterAmount) {
            return "water";
        }
        if (milk > milkAmount) {
            return "milk";
        }
        if (coffee > coffeeAmount) {
            return "coffee";
        }
        if (cupsAmount <= 0) {
            System.out.println("Sorry, not enough cups!");
            return "cups";
        }
        return "";
    }

    private void makeEspresso() {
        final int water = 250;
        final int milk = 0;
        final int coffee = 16;
        final int price = 4;

        String resource = getMissingResource(water, milk, coffee);
        if (resource != "") {
            System.out.println("Sorry, not enough %s!".formatted(resource));
            return;
        }

        System.out.println("I have enough resources, making you a coffee!");

        waterAmount -= water;
        coffeeAmount -= coffee;
        cupsAmount--;
        moneyAmount += price;
    }

    private void makeLatte() {
        final int water = 350;
        final int milk = 75;
        final int coffee = 20;
        final int price = 7;

        String resource = getMissingResource(water, milk, coffee);
        if (resource != "") {
            System.out.println("Sorry, not enough %s!".formatted(resource));
            return;
        }

        System.out.println("I have enough resources, making you a coffee!");

        waterAmount -= water;
        milkAmount -= milk;
        coffeeAmount -= coffee;
        cupsAmount--;
        moneyAmount += price;
    }

    private void makeCappuccino() {
        final int water = 200;
        final int milk = 100;
        final int coffee = 12;
        final int price = 6;

        String resource = getMissingResource(water, milk, coffee);
        if (resource != "") {
            System.out.println("Sorry, not enough %s!".formatted(resource));
            return;
        }

        System.out.println("I have enough resources, making you a coffee!");

        waterAmount -= water;
        milkAmount -= milk;
        coffeeAmount -= coffee;
        cupsAmount--;
        moneyAmount += price;
    }
}
