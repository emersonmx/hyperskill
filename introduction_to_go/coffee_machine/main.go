package main

import "fmt"

const (
	formattedShowRemainingMessage = `The coffee machine has:
%d ml of water
%d ml of milk
%d g of coffee beans
%d disposable cups
%d of money
`
	showMenuMessage             = "Write action (buy, fill, take, remaining, exit):"
	buyMenuMessage              = "What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:"
	waterFillActionMessage      = "Write how many ml of water you want to add:"
	milkFillActionMessage       = "Write how many ml of milk you want to add:"
	coffeeFillActionMessage     = "Write how many grams of coffee beans you want to add:"
	cupsFillActionMessage       = "Write how many disposable cups you want to add:"
	formattedTakeActionMessage  = "I gave you $%d\n"
	haveEnoughResourcesMessage  = "I have enough resources, making you a coffee!"
	formattedNotEnoughResources = "Sorry, not enough %s!\n"
)

func main() {
	var (
		water   = 400
		milk    = 540
		coffee  = 120
		cups    = 9
		money   = 550
		running = true
	)

	for running {
		fmt.Println(showMenuMessage)
		action := getAction()
		switch action {
		case "buy":
			fmt.Println()
			buyAction(&water, &milk, &coffee, &cups, &money)
			fmt.Println()
		case "fill":
			fmt.Println()
			fillAction(&water, &milk, &coffee, &cups)
			fmt.Println()
		case "take":
			fmt.Println()
			takeAction(&money)
			fmt.Println()
		case "remaining":
			fmt.Println()
			showRemaining(water, milk, coffee, cups, money)
			fmt.Println()
		case "exit":
			running = false
		}
	}
}

func getStringInput() string {
	var input string
	_, err := fmt.Scanln(&input)
	if err != nil {
		return ""
	}
	return input
}

func getIntInput() int {
	var input int
	_, err := fmt.Scanln(&input)
	if err != nil {
		return 0
	}
	return input
}

func getAction() string {
	return getStringInput()
}

func buyAction(water *int, milk *int, coffee *int, cups *int, money *int) {
	fmt.Println(buyMenuMessage)
	item := getBuyItem()

	var (
		waterUsage  = 0
		milkUsage   = 0
		coffeeUsage = 0
		cupsUsage   = 1
		price       = 0
	)

	switch item {
	case 1:
		waterUsage = 250
		coffeeUsage = 16
		price = 4
	case 2:
		waterUsage = 350
		milkUsage = 75
		coffeeUsage = 20
		price = 7
	case 3:
		waterUsage = 200
		milkUsage = 100
		coffeeUsage = 12
		price = 6
	default:
		return
	}

	missingResource := ""
	if waterUsage > *water {
		missingResource = "water"
	} else if milkUsage > *milk {
		missingResource = "milk"
	} else if coffeeUsage > *coffee {
		missingResource = "coffee"
	} else if cupsUsage > *cups {
		missingResource = "cups"
	}

	if missingResource != "" {
		fmt.Printf(formattedNotEnoughResources, missingResource)
		return
	}

	*water -= waterUsage
	*milk -= milkUsage
	*coffee -= coffeeUsage
	*cups -= cupsUsage
	*money += price

	fmt.Println(haveEnoughResourcesMessage)
}

func getBuyItem() int {
	return getIntInput()
}

func fillAction(water *int, milk *int, coffee *int, cups *int) {
	fmt.Println(waterFillActionMessage)
	*water += getIntInput()

	fmt.Println(milkFillActionMessage)
	*milk += getIntInput()

	fmt.Println(coffeeFillActionMessage)
	*coffee += getIntInput()

	fmt.Println(cupsFillActionMessage)
	*cups += getIntInput()
}

func takeAction(money *int) {
	fmt.Printf(formattedTakeActionMessage, *money)
	*money = 0
}

func showRemaining(water int, milk int, coffee int, cups int, money int) {
	fmt.Printf(formattedShowRemainingMessage, water, milk, coffee, cups, money)
}
