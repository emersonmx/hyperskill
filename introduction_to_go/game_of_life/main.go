package main

import (
	"fmt"
	"math/rand"
)

func makeCells(size int) [][]bool {
	cells := make([][]bool, size)
	for i := range cells {
		cells[i] = make([]bool, size)
	}
	return cells
}

func initAtRandom(cells [][]bool) {
	for i, row := range cells {
		for j := range row {
			cells[i][j] = rand.Intn(2) == 1
		}
	}
}

type World struct {
	size  int
	cells [][]bool
}

func NewWorld(cells [][]bool) *World {
	return &World{
		size:  len(cells),
		cells: cells,
	}
}

func (w *World) at(i, j int) bool {
	wi, wj := i%w.size, j%w.size
	if wi < 0 {
		wi = w.size + wi
	}
	if wj < 0 {
		wj = w.size + wj
	}
	return w.cells[wi][wj]
}

func (w *World) countNeighbors(i, j int) int {
	count := 0
	if w.at(i-1, j-1) {
		count++
	}
	if w.at(i-1, j) {
		count++
	}
	if w.at(i-1, j+1) {
		count++
	}
	if w.at(i, j-1) {
		count++
	}
	if w.at(i, j+1) {
		count++
	}
	if w.at(i+1, j-1) {
		count++
	}
	if w.at(i+1, j) {
		count++
	}
	if w.at(i+1, j+1) {
		count++
	}
	return count
}

func (w *World) NextGeneration() {
	newCells := makeCells(w.size)

	for i, row := range w.cells {
		for j := range row {
			neighbors := w.countNeighbors(i, j)
			if w.at(i, j) {
				if neighbors == 2 || neighbors == 3 {
					newCells[i][j] = true
				}
			} else {
				if neighbors == 3 {
					newCells[i][j] = true
				}
			}
		}
	}

	w.cells = newCells
}

func (w *World) GetAlive() int {
	count := 0
	for _, row := range w.cells {
		for _, column := range row {
			if column {
				count++
			}
		}
	}
	return count
}

func (w *World) Display() {
	for _, row := range w.cells {
		for _, column := range row {
			if column {
				fmt.Print("O")
			} else {
				fmt.Print(" ")
			}
		}
		fmt.Println()
	}
}

func main() {
	var size int

	fmt.Scan(&size)

	cells := makeCells(size)
	initAtRandom(cells)
	world := NewWorld(cells)

	for i := 1; i <= 10; i++ {
		world.NextGeneration()
		fmt.Printf("Generation #%d\n", i)
		fmt.Println("Alive:", world.GetAlive())
		world.Display()
	}
}
