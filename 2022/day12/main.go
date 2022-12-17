package main

import (
	"bufio"
	"fmt"
	"github.com/albertorestifo/dijkstra"
	"log"
	"os"
	"strings"
)

func main() {

	// DAY 12

	// --- Parsing input file ---
	var lines = readFileLines("input.txt")
	var terrain = readTerrain(lines)
	fmt.Printf("Terrain size is w%d * h%d (%d cells)\n", terrain.width, terrain.height, terrain.width*terrain.height)
	fmt.Printf("E coordinates are x%d * y%d\n", terrain.end.x, terrain.end.y)

	// --- Part 1 ---
	costPart1, _ := findShortestPath(terrain.start, terrain.end, &terrain)
	fmt.Printf("Part One : shortest distance from S to E is %v\n", costPart1)

	// --- Part 2 ---
	costPart2 := costPart1
	for i := 0; i < terrain.width; i++ {
		for j := 0; j < terrain.height; j++ {
			if terrain.cells[j][i] == 1 {
				cost, _ := findShortestPath(Pos{i, j}, terrain.end, &terrain)
				if cost > 0 && cost < costPart2 { // Path must exist (0 means unreachable)
					costPart2 = cost
				}
			}
		}
	}
	fmt.Printf("Part Two : shortest distance from a to E is %v\n", costPart2)

}

func findShortestPath(from Pos, target Pos, terrain *Terrain) (int, error) {
	nodes := map[string]map[string]int{}
	for i := 0; i < terrain.width; i++ {
		for j := 0; j < terrain.height; j++ {
			pos := Pos{i, j}
			edges := map[string]int{}
			options := []Pos{
				{i - 1, j},
				{i + 1, j},
				{i, j - 1},
				{i, j + 1},
			}
			for _, option := range options {
				if canMoveTo(pos, option, terrain) {
					edges[option.id()] = 1
				}
			}
			nodes[pos.id()] = edges
		}
	}
	g := dijkstra.Graph(nodes)
	_, cost, err := g.Path(from.id(), target.id())
	return cost, err
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

type Pos struct {
	x int
	y int
}

func (p *Pos) id() string {
	return fmt.Sprintf("%d,%d", p.y, p.x)
}

type Terrain struct {
	width  int
	height int
	cells  [][]int
	start  Pos
	end    Pos
}

func canMoveTo(from Pos, to Pos, terrain *Terrain) bool {
	if to.x < 0 || to.x >= terrain.width || to.y < 0 || to.y >= terrain.height {
		// out of bounds
		return false
	}
	dist := terrain.cells[to.y][to.x] - terrain.cells[from.y][from.x]
	return dist <= 1
}

func readTerrain(lines []string) Terrain {
	var terrain Terrain
	for y, line := range lines {
		var row []int
		for x, letter := range line {
			value := int((letter - 'a') + 1)
			if letter == 'S' {
				value = 1
				terrain.start = Pos{x, y}
			} else if letter == 'E' {
				value = 26
				terrain.end = Pos{x, y}
			}
			row = append(row, value)
		}
		terrain.cells = append(terrain.cells, row)
	}
	terrain.height = len(terrain.cells)
	terrain.width = len(terrain.cells[0])
	return terrain
}
