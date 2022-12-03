package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
)

func main() {

	// DAY 1

	// --- Parsing ---

	var liste, err = readLines("input.txt")
	if err != nil {
		log.Fatal(err)
	}

	// --- Part 1 ---

	var elves[]int
	var currentCalories int = 0
	var maxCalories int = 0
	for _, element := range liste {
		if len(element) > 0 {
			if currentCalories == 0 {
				elves = append(elves, 0)
			}
			var calories, _ = strconv.Atoi(element)
			currentCalories += calories
			elves[len(elves)-1] = currentCalories
		} else {
			currentCalories = 0
		}
		maxCalories = Max(maxCalories, currentCalories)
	}
	fmt.Printf("There is  %d elves\n", len(elves))
	fmt.Printf("Part One: maxCalories is %d\n", maxCalories)

	// --- Part 2 ---

	sort.Sort(sort.Reverse(sort.IntSlice(elves)))
	fmt.Printf("Part Two: Top three elves %d + %d + %d = %d\n",
		elves[0], elves[1], elves[2], elves[0] + elves[1] + elves[2])

}

func Max(x, y int) int {
	if x < y {
		return y
	}
	return x
}

func readLines(filename string)  ([]string, error) {
	f, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	var ls[]string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		ls = append(ls, scanner.Text())
	}
	return ls, nil
}
