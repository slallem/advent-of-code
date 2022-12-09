package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {

	// DAY 8

	// --- Parsing input file ---
	var forest = loadForest(readFileLines("input.txt"))

	// --- Part 1 ---
	nbVisible := 0
	for j := 0; j < forest.getLength(); j++ {
		for i := 0; i < forest.getWidth(); i++ {
			if forest.IsTreeVisible(j, i) {
				nbVisible++
			}
		}
	}
	fmt.Printf("Part One : answer is %d\n", nbVisible)

	// --- Part 2 ---
	maxScore := 0
	for j := 0; j < forest.getLength(); j++ {
		for i := 0; i < forest.getWidth(); i++ {
			score := forest.CalculateTreeScenicScore(j, i)
			if score > maxScore {
				maxScore = score
			}
		}
	}
	fmt.Printf("Part Two : max scenic score is %d\n", maxScore)
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

type Forest struct {
	trees [][]int
}

func (f *Forest) IsTreeVisible(row, col int) bool {
	return (*f).isTreeVisibleFromAxis(row, col, 0, -1) ||
		(*f).isTreeVisibleFromAxis(row, col, 0, 1) ||
		(*f).isTreeVisibleFromAxis(row, col, -1, 0) ||
		(*f).isTreeVisibleFromAxis(row, col, 1, 0)
}

func (f *Forest) isTreeVisibleFromAxis(row, col, rowIncrement, colIncrement int) bool {
	visible := true
	treeHeight := (*f).getTreeHeight(row, col)
	r := row + rowIncrement
	c := col + colIncrement
	for (*f).isValidTree(r, c) {
		if (*f).getTreeHeight(r, c) >= treeHeight {
			visible = false
			break
		}
		r += rowIncrement
		c += colIncrement
	}
	return visible
}

func (f *Forest) CalculateTreeScenicScore(row, col int) int {
	return (*f).treeScenicScoreFromAxis(row, col, 0, -1) *
		(*f).treeScenicScoreFromAxis(row, col, 0, 1) *
		(*f).treeScenicScoreFromAxis(row, col, -1, 0) *
		(*f).treeScenicScoreFromAxis(row, col, 1, 0)
}

func (f *Forest) treeScenicScoreFromAxis(row, col, rowIncrement, colIncrement int) int {
	score := 0
	curMax := 0
	treeHeight := (*f).getTreeHeight(row, col)
	r := row + rowIncrement
	c := col + colIncrement
	for (*f).isValidTree(r, c) {
		curTreeHeight := (*f).getTreeHeight(r, c)
		if curTreeHeight >= curMax {
			score++
		}
		if curTreeHeight >= treeHeight {
			break
		}
		r += rowIncrement
		c += colIncrement
	}
	return score
}

func (f *Forest) isValidTree(row, col int) bool {
	return row >= 0 && row < (*f).getLength() && col >= 0 && col < (*f).getWidth()
}

func (f *Forest) getTreeHeight(row, col int) int {
	return (*f).trees[row][col]
}

func (f *Forest) getWidth() int {
	if len((*f).trees) == 0 {
		return 0
	} else {
		return len((*f).trees[0])
	}
}

func (f *Forest) getLength() int {
	return len((*f).trees)
}

func loadForest(lines []string) Forest {
	f := Forest{}
	f.trees = [][]int{}
	for _, line := range lines {
		var row []int
		for _, char := range line {
			value, _ := strconv.Atoi(string(char))
			row = append(row, value)
		}
		f.trees = append(f.trees, row)
	}
	return f
}
