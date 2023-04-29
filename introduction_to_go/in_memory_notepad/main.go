package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	var notes []string
	var maxNotes int

	fmt.Print("Enter the maximum number of notes: ")
	fmt.Scanln(&maxNotes)
	fmt.Println()

	scanner := bufio.NewScanner(os.Stdin)
	running := true
	for running {
		fmt.Print("Enter a command and data: ")
		if !scanner.Scan() {
			running = false
			continue
		}

		command, data, _ := strings.Cut(scanner.Text(), " ")

		switch command {
		case "create":
			switch {
			case len(data) == 0:
				fmt.Println("[Error] Missing note argument")
				fmt.Println()
			case len(notes) < maxNotes:
				notes = append(notes, data)
				fmt.Println("[OK] The note was successfully created")
				fmt.Println()
			default:
				fmt.Println("[Error] Notepad is full")
				fmt.Println()
			}
		case "list":
			switch {
			case len(notes) > 0:
				for i, note := range notes {
					fmt.Printf("[Info] %d: %s\n", i+1, note)
				}
				fmt.Println()
			default:
				fmt.Println("[Info] Notepad is empty")
				fmt.Println()
			}
		case "update":
			inputIndex, newTitle, _ := strings.Cut(data, " ")
			if inputIndex == "" {
				fmt.Println("[Error] Missing position argument")
				fmt.Println()
				continue
			}

			index, err := strconv.Atoi(inputIndex)
			if err != nil {
				fmt.Printf("[Error] Invalid position: %s\n", inputIndex)
				fmt.Println()
				continue
			}

			if newTitle == "" {
				fmt.Println("[Error] Missing note argument")
				fmt.Println()
				continue
			}

			index--
			if index < 0 || index >= maxNotes {
				fmt.Printf("[Error] Position %d is out of the boundaries [1, %d]\n", index+1, maxNotes)
				fmt.Println()
				continue
			}

			if index < len(notes) {
				notes[index] = newTitle
				fmt.Printf("[OK] The note at position %d was successfully updated\n", index+1)
			} else {
				fmt.Println("[Error] There is nothing to update")
			}
			fmt.Println()
		case "delete":
			if len(data) == 0 {
				fmt.Println("[Error] Missing position argument")
				fmt.Println()
				continue
			}

			index, err := strconv.Atoi(data)
			if err != nil {
				fmt.Printf("[Error] Invalid position: %s\n", data)
				fmt.Println()
				continue
			}

			index--
			if index < 0 || index >= maxNotes {
				fmt.Printf("[Error] Position %d is out of the boundaries [1, %d]\n", index+1, maxNotes)
				fmt.Println()
				continue
			}

			if index < len(notes) {
				notes = append(notes[:index], notes[index+1:]...)
			} else if index == len(notes)-1 {
				notes = notes[:index-1]
			} else {
				fmt.Println("[Error] There is nothing to delete")
				fmt.Println()
				continue
			}
			fmt.Printf("[OK] The note at position %d was successfully deleted\n", index+1)
			fmt.Println()
		case "clear":
			notes = nil
			fmt.Println("[OK] All notes were successfully deleted")
			fmt.Println()
		case "exit":
			running = false
			continue
		default:
			fmt.Println("[Error] Unknown command")
			fmt.Println()
		}
	}

	fmt.Println("[Info] Bye!")
}
