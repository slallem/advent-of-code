package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func main() {

	// DAY 5

	// --- Parsing input file ---
	var lines = readFileLines("input.txt")
	var stacks []Stack
	var moves []Move

	// --- Part 1 ---
	stacks, moves = readInitialStacksAndMoves(lines)
	for _, m := range moves {
		for i := 0; i < m.qty; i++ {
			crate := stacks[m.from-1].Pop()
			stacks[m.to-1].Push(crate)
		}
	}
	message1 := ""
	for _, stack := range stacks {
		message1 += stack.Pick()
	}
	fmt.Printf("Part One: message is: %s\n", message1)

	// --- Part 2 ---
	stacks, moves = readInitialStacksAndMoves(lines)
	for _, m := range moves {
		var tmp Stack
		for i := 0; i < m.qty; i++ {
			crate := stacks[m.from-1].Pop()
			tmp.Push(crate)
		}
		for !tmp.IsEmpty() {
			stacks[m.to-1].Push(tmp.Pop())
		}
	}
	message2 := ""
	for _, stack := range stacks {
		message2 += stack.Pick()
	}
	fmt.Printf("Part Two: message is: %s\n", message2)

}

func readInitialStacksAndMoves(lines []string) ([]Stack, []Move) {
	var stacks []Stack
	var moves []Move
	regexpMove := regexp.MustCompile(`move (\d*) from (\d*) to (\d*)`)
	for _, line := range lines {
		if strings.Contains(line, "[") {
			for i := 1; i < len(line); i += 4 { // columns 1, 5, 9...
				stackIndex := (i - 1) / 4 // stack no 0, 1, 2...
				for j := len(stacks); j <= stackIndex; j++ {
					stacks = append(stacks, []string{})
				}
				if line[i-1] == '[' && line[i+1] == ']' {
					stacks[stackIndex].InsertBottom(string(line[i]))
				}
			}
		} else if strings.Contains(line, "move") {
			res := regexpMove.FindStringSubmatch(line)
			var m Move
			m.qty, _ = strconv.Atoi(res[1])
			m.from, _ = strconv.Atoi(res[2])
			m.to, _ = strconv.Atoi(res[3])
			moves = append(moves, m)
		} else if strings.Contains(line, "---") {
			break
		}
	}
	return stacks, moves
}

type Move struct {
	qty int
	from int
	to int
}

type Stack []string

// IsEmpty : check if stack is empty
func (s *Stack) IsEmpty() bool {
	return len(*s) == 0
}

// Push a new value onto the stack
func (s *Stack) Push(item string) {
	*s = append(*s, item) // Simply append the new value to the end of the stack
}

// InsertBottom inserts an item at the bottom of the stack
func (s *Stack) InsertBottom(item string) {
	*s = append([]string{item}, *s...)
}

// Pop removes and return top element of stack. Returns false if stack is empty.
func (s *Stack) Pop() string {
	if s.IsEmpty() {
		log.Fatal("Cannot pop an empty stack")
	}
	index := len(*s) - 1 // Get the index of the top most element.
	element := (*s)[index] // Index into the slice and obtain the element.
	*s = (*s)[:index] // Remove it from the stack by slicing it off.
	return element
}

func (s *Stack) Pick() string {
	if s.IsEmpty() {
		return ""
	} else {
		return (*s)[len(*s) - 1]
	}
}

func readFileLines(filename string) []string {
	f, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer func(f *os.File) {
		err := f.Close()
		if err != nil {
			log.Fatal(err)
		}
	}(f)
	var lines []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines
}
