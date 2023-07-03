package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type Card struct {
	Term       string
	Definition string
}

type App struct {
	cards       []Card
	terms       map[string]struct{}
	definitions map[string]struct{}
	cardIndex   int
}

func NewApp() *App {
	return &App{
		cards:       []Card{},
		terms:       map[string]struct{}{},
		definitions: map[string]struct{}{},
		cardIndex:   0,
	}
}

func (a *App) HasTerm(term string) bool {
	_, exists := a.terms[strings.ToLower(term)]
	return exists
}

func (a *App) HasDefinition(definition string) bool {
	_, exists := a.definitions[strings.ToLower(definition)]
	return exists
}

func (a *App) GetSuggestion(definition string) string {
	var suggestion string
	for _, card := range a.cards {
		if definition == card.Definition {
			suggestion = card.Term
			break
		}
	}
	return suggestion
}

func (a *App) AddCard(card Card) {
	a.cards = append(a.cards, card)
	a.terms[strings.ToLower(card.Term)] = struct{}{}
	a.definitions[strings.ToLower(card.Definition)] = struct{}{}
}

func (a *App) RemoveCard(term string) {
	index := -1
	for i, card := range a.cards {
		if card.Term == term {
			index = i
			break
		}
	}
	if index == -1 {
		return
	}

	cardToDelete := a.cards[index]
	delete(a.terms, strings.ToLower(cardToDelete.Term))
	delete(a.definitions, strings.ToLower(cardToDelete.Definition))
	a.cards = append(a.cards[:index], a.cards[index+1:]...)
}

func (a *App) ResetCardIndex() {
	a.cardIndex = 0
}

func (a *App) CurrentCard() Card {
	return a.cards[a.cardIndex]
}

func (a *App) Check(definition string) bool {
	card := &a.cards[a.cardIndex]
	a.cardIndex++
	a.cardIndex = a.cardIndex % len(a.cards)
	return card.Definition == definition
}

func (a *App) Import(path string) (int, error) {
	cardsJson, err := os.ReadFile(path)
	if err != nil {
		return 0, err
	}

	var cards []Card
	if err := json.Unmarshal(cardsJson, &cards); err != nil {
		return 0, err
	}

	i := 0
	for _, card := range cards {
		if a.HasTerm(card.Term) {
			a.RemoveCard(card.Term)
		}
		a.AddCard(card)
		i++
	}

	return i, nil
}

func (a *App) Export(path string) int {
	cardsJson, err := json.Marshal(a.cards)
	if err != nil {
		return 0
	}

	if err := os.WriteFile(path, cardsJson, 0644); err != nil {
		return 0
	}

	return len(a.cards)
}

func readLine() string {
	scanner := bufio.NewScanner(os.Stdin)
	if scanner.Scan() {
		return scanner.Text()
	}
	return ""
}

func main() {
	app := NewApp()
	running := true
	for running {
		fmt.Println("Input the action (add, remove, import, export, ask, exit):")
		action := readLine()
		switch action {
		case "add":
			addAction(app)
		case "remove":
			removeAction(app)
		case "import":
			importAction(app)
		case "export":
			exportAction(app)
		case "ask":
			askAction(app)
		case "exit":
			fmt.Println("Bye bye!")
			running = false
		}
	}
}

func addAction(app *App) {
	fmt.Println("The card:")
	var term string
	for {
		term = readLine()
		if app.HasTerm(term) {
			fmt.Printf("The card \"%s\" already exists. Try again:\n", term)
		} else {
			break
		}
	}

	fmt.Println("The definition of the card:")
	var definition string
	for {
		definition = readLine()
		if app.HasDefinition(definition) {
			fmt.Printf("The definition \"%s\" already exists. Try again:\n", definition)
		} else {
			break
		}
	}

	app.AddCard(Card{Term: term, Definition: definition})
	fmt.Printf("The pair (\"%s\":\"%s\") has been added.\n", term, definition)
	fmt.Println()
}

func removeAction(app *App) {
	fmt.Println("Which card?")
	term := readLine()
	if app.HasTerm(term) {
		app.RemoveCard(term)
		fmt.Println("The card has been removed.")
	} else {
		fmt.Printf("Can't remove \"%s\": there is no such card.\n", term)
	}
	fmt.Println()
}

func importAction(app *App) {
	fmt.Println("File name:")
	filename := readLine()
	count, err := app.Import(filename)
	if err != nil {
		fmt.Println("File not found.")
	} else {
		fmt.Printf("%d cards have been loaded.\n", count)
	}
	fmt.Println()
}

func exportAction(app *App) {
	fmt.Println("File name:")
	filename := readLine()
	count := app.Export(filename)
	fmt.Printf("%d cards have been saved.\n", count)
	fmt.Println()
}

func askAction(app *App) {
	fmt.Println("How many times to ask?")
	var times int
	_, err := fmt.Scan(&times)
	if err != nil {
		fmt.Println("Wrong input")
		return
	}

	app.ResetCardIndex()
	for i := 0; i < times; i++ {
		card := app.CurrentCard()
		fmt.Printf("Print the definition of \"%s\":\n", card.Term)
		definition := readLine()

		if app.Check(definition) {
			fmt.Println("Correct!")
		} else {
			suggestion := app.GetSuggestion(definition)
			if suggestion == "" {
				fmt.Printf("Wrong. The right answer is \"%s\".\n", card.Definition)
			} else {
				fmt.Printf("Wrong. The right answer is \"%s\", but your definition is correct for \"%s\".\n", card.Definition, suggestion)
			}
		}
	}
	fmt.Println()
}
