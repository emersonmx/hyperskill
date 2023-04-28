package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func loadWords(filename string) []string {
	file, err := os.Open(filename)
	if err != nil {
		return nil
	}
	defer file.Close()

	words := make([]string, 0)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		words = append(words, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		return nil
	}

	return words
}

func main() {
	var filename string
	fmt.Scanln(&filename)
	tabooWords := loadWords(filename)

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		if line == "exit" {
			break
		}

		for _, tabooWord := range tabooWords {
			for _, word := range strings.Split(line, " ") {
				if strings.ToLower(word) == strings.ToLower(tabooWord) {
					line = strings.ReplaceAll(line, word, strings.Repeat("*", len(word)))
				}
			}
		}

		fmt.Println(line)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	fmt.Println("Bye!")
}
