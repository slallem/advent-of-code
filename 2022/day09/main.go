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

	// DAY 9

	// --- Parsing input file ---
	var lines = readFileLines("input.txt")
	var moves = loadMoves(lines)

	// --- Part 1 ---
	{
		head := Pos{0, 0}
		tail := Pos{0, 0}
		var visited = map[string]bool{}
		visited[tail.getUID()] = true
		for _, move := range moves {
			for step := 0; step < move.distance; step++ {
				head.move(move.direction, 1)
				tail.follow(head)
				visited[tail.getUID()] = true
			}
		}
		fmt.Printf("Part One : number of locations visited by tail %d\n", len(visited))
	}

	// --- Part 2 ---
	{
		nbKnots := 10
		headIndex := 0
		tailIndex := nbKnots - 1
		var knots []Pos
		for i := 0; i < nbKnots; i++ {
			knots = append(knots, Pos{0, 0})
		}
		visited := map[string]bool{}
		visited[knots[tailIndex].getUID()] = true
		for _, move := range moves {
			for step := 0; step < move.distance; step++ {
				knots[headIndex].move(move.direction, 1)
				for k := 1; k < nbKnots; k++ {
					knots[k].follow(knots[k-1])
				}
				visited[knots[tailIndex].getUID()] = true
			}
			//--displayDots(knots)
		}
		fmt.Printf("Part Two : number of locations visited by tail %d\n", len(visited))
	}

}

func displayDots(dots []Pos) {
	// Determine bounds
	minx, maxx, miny, maxy := 0, 0, 0, 0
	for k := 0; k < len(dots); k++ {
		if dots[k].x < minx {
			minx = dots[k].x
		} else if dots[k].x > maxx {
			maxx = dots[k].x
		}
		if dots[k].y < miny {
			miny = dots[k].y
		} else if dots[k].y > maxy {
			maxy = dots[k].y
		}
	}
	// Display all
	for j := miny - 1; j <= maxy+1; j++ {
		for i := minx - 1; i <= maxx+1; i++ {
			car := "."
			for k := len(dots) - 1; k >= 0; k-- {
				if dots[k].x == i && dots[k].y == j {
					car = fmt.Sprintf("%d", k)
					if car == "0" {
						car = "H"
					}
				}
			}
			fmt.Print(car)
		}
		fmt.Print("\n")
	}
	fmt.Print("\n")
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
		if strings.Contains(scanner.Text(), "-----") {
			break
		}
		lines = append(lines, scanner.Text())
	}
	return lines
}

type Move struct {
	direction uint8 // uint8 == char ('R', 'U', 'L', 'B')
	distance  int
}

func loadMoves(lines []string) []Move {
	var moves []Move
	for _, line := range lines {
		var m Move
		m.direction = line[0]
		m.distance, _ = strconv.Atoi(line[2:])
		moves = append(moves, m)
	}
	return moves
}

type Pos struct {
	x int
	y int
}

func (p *Pos) move(direction uint8, distance int) {
	switch direction {
	case 'R': // Right
		(*p).x += distance
	case 'L': // Left
		(*p).x -= distance
	case 'U': // Up
		(*p).y -= distance
	case 'D': // Down
		(*p).y += distance
	default:
		log.Fatal("Invalid move: " + string(direction))
	}
}

func (p *Pos) follow(given Pos) {
	// Check distances to see if knot needs to move
	diffX := (*p).x - given.x
	diffY := (*p).y - given.y
	//fmt.Printf("diff x %d y %d \n", diffX, diffY)
	if (Abs(diffX) == 2 && diffY == 0) || (Abs(diffY) == 2 && diffX == 0) {
		// If the head is ever two steps directly up, down, left, or right from the tail,
		// the tail must also move one step in that direction so it remains close enough:
		(*p).x -= ZeroOrSign(diffX)
		(*p).y -= ZeroOrSign(diffY)
	} else if Abs(diffX) > 1 || Abs(diffY) > 1 {
		// Otherwise, if the head and tail aren't touching and aren't in the same row or column,
		// the tail always moves one step diagonally to keep up:
		(*p).x -= ZeroOrSign(diffX)
		(*p).y -= ZeroOrSign(diffY)
	} else {
		// No need to move
	}
}

func (p *Pos) getUID() string {
	return fmt.Sprintf("%d:%d", (*p).x, (*p).y)
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func ZeroOrSign(x int) int {
	if x == 0 {
		return 0
	} else if x < 0 {
		return -1
	} else {
		return 1
	}
}
