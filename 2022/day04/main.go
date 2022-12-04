package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
)

func main() {

	// DAY 4

	// --- Parsing input file ---
	var lines = readFileLines("input.txt")

	// --- Part 1 ---
	r := regexp.MustCompile(`(\d*)-(\d*),(\d*)-(\d*)`)
	var nbFullyIncluded = 0
	var nbOverlapping = 0
	for _, line := range lines {
		res := r.FindStringSubmatch(line)
		min1, _ := strconv.Atoi(res[1])
		max1, _ := strconv.Atoi(res[2])
		min2, _ := strconv.Atoi(res[3])
		max2, _ := strconv.Atoi(res[4])
		if (isInRange(min1, min2, max2) && isInRange(max1, min2, max2)) || (isInRange(min2, min1, max1) && isInRange(max2, min1, max1)) {
			nbFullyIncluded++
		}
		if (isInRange(min1, min2, max2) || isInRange(max1, min2, max2)) || (isInRange(min2, min1, max1) || isInRange(max2, min1, max1)) {
			nbOverlapping++
		}
	}
	fmt.Printf("Part One: number of fully included sections is %d\n", nbFullyIncluded)

	// --- Part 2 ---
	fmt.Printf("Part Two: number of overlapping pairs is %d\n", nbOverlapping)

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

func isInRange(value int, rangeFrom int, rangeTo int) bool {
	return value >= rangeFrom && value <= rangeTo
}
