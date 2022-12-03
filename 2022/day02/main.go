package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func main() {

	// DAY 2

	// --- Parsing input file ---

	var opponentMoves []string
	var myMovesPart1 []string
	var myMovesPart2 []string

	var filename = "input.txt"
	var debug = false

	if debug {
		filename = "input_test.txt"
	}

	f, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer func(f *os.File) {
		err := f.Close()
		if err != nil {}
	}(f)
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		var move1 = scanner.Text()[0:1]
		var move2 = scanner.Text()[2:3]
		opponentMoves = append(opponentMoves, decodeLetterPart1(move1))
		myMovesPart1 = append(myMovesPart1, decodeLetterPart1(move2))
		myMovesPart2 = append(myMovesPart2, decodeLetterPart2(decodeLetterPart1(move1), move2))
	}
	if err != nil {
		log.Fatal(err)
	}

	// --- Part 1 ---

	var opponentScorePart1 = 0
	var myScorePart1 = 0
	for index := range opponentMoves {
		var sp1, sp2 = computeScores(opponentMoves[index], myMovesPart1[index])
		if debug {
			fmt.Printf("Part1 Round #%d: Scores P1 %d P2 %d\n", index+1, sp1, sp2)
		}
		opponentScorePart1 += sp1
		myScorePart1 += sp2
	}
	fmt.Printf("Part One: My total score is %d\n", myScorePart1)

	// --- Part 2 ---
	var opponentScorePart2 = 0
	var myScorePart2 = 0
	for index := range opponentMoves {
		var sp1, sp2 = computeScores(opponentMoves[index], myMovesPart2[index])
		if debug {
			fmt.Printf("Part2 Round #%d: Move1 %s Move2 %s ScoreP1 %d ScoreP2 %d\n", index+1,
				opponentMoves[index], myMovesPart2[index], sp1, sp2)
		}
		opponentScorePart2 += sp1
		myScorePart2 += sp2
	}
	fmt.Printf("Part Two: My total score is %d\n", myScorePart2)

}

// A,X = Rock
// B,Y = Paper
// C,Z = Scissors

func computeScores(p1, p2 string) (int, int) {
	// Evaluate winning situations
	var win1 = (p1=="R" && p2=="S") || (p1=="P" && p2=="R") || (p1=="S" && p2=="P")
	var win2 = (p2=="R" && p1=="S") || (p2=="P" && p1=="R") || (p2=="S" && p1=="P")
	// Base scores
	var s1 = scoreOf(p1)
	var s2 = scoreOf(p2)
	// Bonuses
	if win2 && !win1 {
		s2 += 6
	} else if win1 && !win2 {
		s1 += 6
	} else { // draw
		s1 += 3
		s2 += 3
	}
	return s1, s2
}

func scoreOf(c string) int {
	switch {
	case c == "R":
		return 1
	case c == "P":
		return 2
	case c == "S":
		return 3
	}
	return 0
}

func decodeLetterPart1(c string) string {
	switch {
	case strings.Contains("AX", c):
		return "R"
	case strings.Contains("BY", c):
		return "P"
	case strings.Contains("CZ", c):
		return "S"
	}
	return "?"
}

func decodeLetterPart2(opponentMove, secretMove string) string {
	var res = ""
	switch {
	case secretMove == "X": // lose
		if opponentMove == "R" {
			res = "S"
		} else if opponentMove == "P" {
			res = "R"
		} else if opponentMove == "S" {
			res = "P"
		}
	case secretMove == "Y": // draw
		res = opponentMove
	case secretMove == "Z": // win
		if opponentMove == "R" {
			res = "P"
		} else if opponentMove == "P" {
			res = "S"
		} else if opponentMove == "S" {
			res = "R"
		}
	}
	return res
}

