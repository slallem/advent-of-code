package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func main() {

	// DAY 18

	// --- Parsing input file ---
	var lines = readFileLines("input.txt")

	// Read droplets
	r := regexp.MustCompile(`(\d*),(\d*),(\d*)`)
	droplets := map[string]Cube{}
	for _, line := range lines {
		res := r.FindStringSubmatch(line)
		x, _ := strconv.Atoi(res[1])
		y, _ := strconv.Atoi(res[2])
		z, _ := strconv.Atoi(res[3])
		d := newCube(x, y, z)
		droplets[d.id] = d
	}

	// Remove obstructed exposedFaces
	for _, d1 := range droplets {
		for _, d2 := range droplets {
			delete(d1.exposedFaces, d2.id)
		}
	}

	// Count remaining exposed faces
	part1 := 0
	for _, d1 := range droplets {
		part1 += d1.exposedCount()
	}

	// --- Part 1 ---
	fmt.Printf("Part One : number of exposed faces is %v\n", part1)

	//--- Part2 ---
	// Find bubbles

	// Reinit droplets
	droplets = map[string]Cube{}
	for _, line := range lines {
		res := r.FindStringSubmatch(line)
		x, _ := strconv.Atoi(res[1])
		y, _ := strconv.Atoi(res[2])
		z, _ := strconv.Atoi(res[3])
		d := newCube(x, y, z)
		droplets[d.id] = d
	}
	// List bubble candidates (all droplets faces are candidates)
	bubbleCandidates := map[string]Cube{}
	for _, d := range droplets {
		for key := range d.exposedFaces {
			res := r.FindStringSubmatch(key)
			x, _ := strconv.Atoi(res[1])
			y, _ := strconv.Atoi(res[2])
			z, _ := strconv.Atoi(res[3])
			d := newCube(x, y, z)
			bubbleCandidates[d.id] = d
		}
	}
	// Exclude actual droplets as bubbles candidates
	for _, d := range droplets {
		delete(bubbleCandidates, d.id)
	}

	// Determine bounds
	bounds := newBoundsFromCubes(droplets)

	// Find bubbles
	fmt.Printf("There is %d bubble candidates\n", len(bubbleCandidates))
	bubbles := map[string]Cube{}
	for _, candidate := range bubbleCandidates {
		_, exists := bubbles[candidate.id]
		if !exists {
			found := evaluateBubblesFrom(candidate, droplets, bounds)
			if len(found) > 0 {
				fmt.Printf("Found %v-sized bubble at %v \n", len(found), candidate.id)
			}
			for _, cube := range found {
				bubbles[cube.id] = cube
			}
		}
	}

	// Remove obstructed exposedFaces = count remaining exposed faces
	part2 := 0
	for _, d1 := range droplets {
		for _, d2 := range droplets {
			delete(d1.exposedFaces, d2.id)
		}
		for _, b := range bubbles {
			delete(d1.exposedFaces, b.id)
		}
		part2 += d1.exposedCount()
	}

	fmt.Printf("Part Two : remaining exterior faces are %d\n", part2)

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

func evaluateBubblesFrom(bs Cube, droplets map[string]Cube, bounds Bounds) []Cube {
	visited := map[string]bool{}
	queued := map[string]bool{}
	spots := []Cube{bs}
	var results []Cube
	for len(spots) > 0 {
		spot := spots[0]
		results = append(results, spot)
		spots = spots[1:]
		_, alreadyVisited := visited[spot.id]
		if !alreadyVisited {
			visited[spot.id] = true
			if bounds.excludes(spot) {
				// cannot be a bubble if expansion can reach outside
				return []Cube{}
			}
			for id := range spot.exposedFaces {
				_, isDroplet := droplets[id]
				_, alreadyQueued := queued[id]
				if !isDroplet && !alreadyQueued {
					spots = append(spots, newCubeFromId(id))
					queued[id] = true
				}
			}
		}
	}
	return results
}

type Bounds struct {
	minX, minY, minZ, maxX, maxY, maxZ int
}

func newBoundsFromCubes(cubes map[string]Cube) Bounds {
	var bounds *Bounds = nil
	for _, c := range cubes {
		if bounds == nil {
			bounds = &(Bounds{c.x, c.y, c.z, c.x, c.y, c.z})
		} else {
			bounds.extend(c)
		}
	}
	return *bounds
}

func (b *Bounds) extend(cube Cube) {
	if cube.x < b.minX {
		b.minX = cube.x
	}
	if cube.y < b.minY {
		b.minY = cube.y
	}
	if cube.z < b.minZ {
		b.minZ = cube.z
	}
	if cube.x > b.maxX {
		b.maxX = cube.x
	}
	if cube.y > b.maxY {
		b.maxY = cube.x
	}
	if cube.z > b.maxZ {
		b.maxZ = cube.z
	}
}

func (b *Bounds) excludes(c Cube) bool {
	return c.x < b.minX || c.x > b.maxX || c.y < b.minY || c.y > b.maxY || c.z < b.minZ || c.z > b.maxZ
}
func (b *Bounds) includes(c Cube) bool {
	return !b.excludes(c)
}

type Cube struct {
	x            int
	y            int
	z            int
	id           string
	exposedFaces map[string]bool
}

func (d *Cube) exposedCount() int {
	return len(d.exposedFaces)
}

func newCubeFromId(id string) Cube {
	r := regexp.MustCompile(`(\d*),(\d*),(\d*)`)
	res := r.FindStringSubmatch(id)
	x, _ := strconv.Atoi(res[1])
	y, _ := strconv.Atoi(res[2])
	z, _ := strconv.Atoi(res[3])
	return newCube(x, y, z)
}

func newCube(ax, ay, az int) Cube {
	res := Cube{
		x:  ax,
		y:  ay,
		z:  az,
		id: idFromXYZ(ax, ay, az),
		exposedFaces: map[string]bool{
			idFromXYZ(ax+1, ay, az): true,
			idFromXYZ(ax-1, ay, az): true,
			idFromXYZ(ax, ay+1, az): true,
			idFromXYZ(ax, ay-1, az): true,
			idFromXYZ(ax, ay, az+1): true,
			idFromXYZ(ax, ay, az-1): true,
		},
	}
	return res
}

func idFromXYZ(ax, ay, az int) string {
	return fmt.Sprintf("%d,%d,%d", ax, ay, az)
}
