package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	for {
		fmt.Print("Enter a command and data: ")
		if !scanner.Scan() {
			break
		}

		input := strings.Split(scanner.Text(), " ")
		command, data := input[0], strings.Join(input[1:], " ")

		if command == "exit" {
			break
		}
		fmt.Printf("%s %s\n", command, data)
		fmt.Println()
	}

	fmt.Println("[Info] Bye!")
}
