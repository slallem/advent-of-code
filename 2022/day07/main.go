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

	// DAY 7

	// --- Parsing input file ---
	var lines = readFileLines("input.txt")

	// Parse commands and compute dir sizes
	var dirSizes = map[string]int{}
	currentDir := "/"
	dirSizes[currentDir] = 0
	regexSizeAndFilename := regexp.MustCompile(`(\d*) (.*)`)
	for _, line := range lines {
		//--fmt.Print(fmt.Sprintf("%-30s", line)[0:30])
		if line == "$ ls" {
			//RAS
		} else if line[0:4] == "dir " {
			dirName := line[4:]
			if _, ok := dirSizes[dirName]; !ok {
				dirSizes[currentDir+dirName+"/"] = 0
			}
		} else if line[0:5] == "$ cd " {
			dirName := line[5:]
			if dirName == ".." {
				pos := strings.LastIndex(currentDir[:len(currentDir)-1], "/")
				currentDir = currentDir[0 : pos+1]
			} else if dirName[0] == '/' { // Absolute
				currentDir = dirName
			} else { // Relative
				currentDir += dirName + "/"
			}
		} else if regexSizeAndFilename.MatchString(line) {
			res := regexSizeAndFilename.FindStringSubmatch(line)
			fileSize, _ := strconv.Atoi(res[1])
			//--fmt.Printf("Found file %s of size %d -> adding to %s", res[2], fileSize, currentDir)
			// Count the file size in all directories that contains it (directly on not)
			parts := strings.Split(currentDir[0:len(currentDir)-1], "/")
			dir := ""
			for _, part := range parts {
				dir += part + "/"
				dirSizes[dir] += fileSize
			}
		}
		//--fmt.Printf("; currentDir is %s\n", currentDir)
	}

	// --- Part 1 ---
	totalPart1 := 0
	for _, dirSize := range dirSizes {
		if dirSize <= 100000 {
			//--fmt.Printf("%s has a size of %d (and is not over 100000)\n", dirName, dirSize)
			totalPart1 += dirSize
		}
	}
	fmt.Printf("Part One : total size is %d\n", totalPart1)

	// --- Part 2 ---
	totalSpace := 70000000
	unusedSpaceNeeded := 30000000
	totalUsed := dirSizes["/"]
	actualFree := totalSpace - totalUsed
	minimumBytesToFree := unusedSpaceNeeded - actualFree
	//--fmt.Printf("Total used %d free %d minimum to free %d\n", totalUsed, actualFree, minimumBytesToFree)
	totalPart2 := totalUsed
	for _, dirSize := range dirSizes {
		if dirSize >= minimumBytesToFree {
			if dirSize < totalPart2 {
				totalPart2 = dirSize
			}
		}
	}
	fmt.Printf("Part Two : size of directory is %d\n", totalPart2)
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
