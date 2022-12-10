package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func main() {

	// DAY 10

	// --- Parsing input file ---
	var lines = readFileLines("input.txt")

	// --- Part 1 ---
	x := 1
	total1 := 0
	cycle := 1
	for _, line := range lines {
		if line == "noop" {
			cycle++
			total1 += signalValueAt(cycle, x)
		} else if line[0:5] == "addx " {
			value, _ := strconv.Atoi(line[5:])
			cycle++
			total1 += signalValueAt(cycle, x)
			cycle++
			x += value
			total1 += signalValueAt(cycle, x)
		}
	}
	fmt.Printf("Part One : signal strengh is %d\n", total1)

	// --- Part 2 ---
	fmt.Printf("Part Two:\n")
	x = 1
	cycle = 1
	drawPixel(cycle, x)
	for _, line := range lines {
		if line == "noop" {
			cycle++
			drawPixel(cycle, x)
		} else if line[0:5] == "addx " {
			value, _ := strconv.Atoi(line[5:])
			cycle++
			drawPixel(cycle, x)
			cycle++
			x += value
			drawPixel(cycle, x)
		}
	}

}

func signalValueAt(cycle, x int) int {
	res := 0
	if (cycle+20)%40 == 0 {
		res = cycle * x
	}
	//--fmt.Printf("cycle %v x %v res %v\n", cycle, x, res)
	return res
}

func drawPixel(cycle, x int) {
	hPos := ((cycle - 1) % 40) + 1 // = 1..40
	if hPos >= x && hPos < x+3 {
		fmt.Print("██")
	} else {
		fmt.Print("  ")
	}
	if hPos == 40 { // end of line
		fmt.Print("\n")
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
		if strings.Contains(scanner.Text(), "---") {
			break
		}
		lines = append(lines, scanner.Text())
	}
	return lines
}
