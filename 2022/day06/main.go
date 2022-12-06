package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {

	// DAY 6

	// --- Parsing input file ---
	var line = readFileLines("input.txt")[0]

	// --- Part 1 ---
	fmt.Printf("Part One : first marker after character %d\n", findFirstMarker(line,4))

	// --- Part 2 ---
	fmt.Printf("Part Two : first marker after character %d\n", findFirstMarker(line,14))

}

func findFirstMarker(line string, markerLen int) int {
	res := -1
	for i := markerLen-1; i < len(line); i++ {
		var set = map[uint8]uint8{}
		for j := 0; j < markerLen; j++ {
			set[line[i-j]] = 1
		}
		if len(set) == markerLen {
			res = i+1
			break
		}
	}
	return res
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
