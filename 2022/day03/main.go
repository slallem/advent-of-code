package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func main() {

	// DAY 3

	// --- Parsing input file ---
	rucksacks := readFileLines("input.txt")

	// --- Part 1 ---
	scorePart1 := 0
	for _, rucksack := range rucksacks {
		// Split compartments
		halfLen := len(rucksack)/2
		compartment1 := rucksack[0:halfLen]
		compartment2 := rucksack[halfLen:]
		// Identify error
		for _, c := range []rune(compartment1) {
			if strings.Contains(compartment2, string(c)) {
				scorePart1 += priorityScore(c)
				break
			}
		}
	}
	fmt.Printf("Part One : Total score of misplaced items is %d \n", scorePart1)

	// --- Part 2 ---
	scorePart2 := 0
	for i := 0; i < len(rucksacks); i+=3 {
		common := commonChars(commonChars(rucksacks[i], rucksacks[i+1]), rucksacks[i+2])
		scorePart2 += priorityScore(rune(common[0]))
	}
	fmt.Printf("Part Two : Total score of group badges is %d \n", scorePart2)

}

func readFileLines(filename string) []string {
	f, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	var ls []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		ls = append(ls, scanner.Text())
	}
	return ls
}

func priorityScore(c rune) int {
	res := 0
	a := int(c)
	if a >= int('a') && a <= int('z') {
		res = 1 + (a - int('a'))
	} else if a >= int('A') && a <= int('Z') {
		res = 27 + (a - int('A'))
	}
	return res
}

func commonChars(s1, s2 string) string {
	res := ""
	for _, c := range []rune(s1) {
		if strings.Contains(s2, string(c)) {
			if !strings.Contains(res, string(c)) {
				res += string(c)
			}
		}
	}
	return res
}
