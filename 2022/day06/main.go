package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {

	// DAY 5

	// --- Parsing input file ---
	var lines = readFileLines("input.txt")

	// --- Part 1 ---
	for _, line := range lines {
		for i := 3; i < len(line); i++ {
			var set = map[uint8]uint8{}
			set[line[i-3]] = 1
			set[line[i-2]] = 1
			set[line[i-1]] = 1
			set[line[i]] = 1
			if len(set) == 4 {
				fmt.Printf("%s: first marker after character %d", line, i+1)
				break
			}
		}
	}

	//--fmt.Printf("Part One: message is: %s\n", message1)

	// --- Part 2 ---
	//--fmt.Printf("Part Two: message is: %s\n", message2)

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
