package main

import (
	"fmt"
	"sort"
)

type Monkey struct {
	items       []int
	operation   func(int) int
	divisibleBy int
	trueGoesTo  int
	falseGoesTo int
	counter     int
}

func main() {

	// DAY 11

	// --- Part 1 ---
	{
		monkeys := inputMonkeys()
		for turn := 1; turn <= 20; turn++ {
			for index := range &monkeys {
				monkey := &monkeys[index]
				for len(monkey.items) > 0 {
					monkey.counter++
					item := monkey.items[0]
					monkey.items = monkey.items[1:]
					newItem := monkey.operation(item) / 3
					var nextMonkey *Monkey
					if newItem%monkey.divisibleBy == 0 {
						nextMonkey = &monkeys[monkey.trueGoesTo]
					} else {
						nextMonkey = &monkeys[monkey.falseGoesTo]
					}
					nextMonkey.items = append(nextMonkey.items, newItem)
				}
				//fmt.Printf("Turn %d after monkey %d :  %v\n", turn, index, monkeys)
			}
			//fmt.Printf("Turn %d : %v\n", turn, monkeys)
		}
		// Find the two max
		var inspections []int
		for _, m := range monkeys {
			inspections = append(inspections, m.counter)
		}
		sort.Sort(sort.Reverse(sort.IntSlice(inspections)))
		fmt.Printf("Part One : top2 inspections are %d and %d then solution is %d\n",
			inspections[0], inspections[1], inspections[0]*inspections[1])
	}

	// --- Part 2 ---
	{
		monkeys := inputMonkeys()
		var allDividers int = 1
		for _, m := range monkeys {
			allDividers = allDividers * m.divisibleBy
		}
		for turn := 1; turn <= 10000; turn++ {
			for index := range &monkeys {
				monkey := &monkeys[index]
				for len(monkey.items) > 0 {
					monkey.counter++
					item := monkey.items[0]
					monkey.items = monkey.items[1:]
					newItem := monkey.operation(item) % allDividers // reduce value without changing its divisibility
					var nextMonkey *Monkey
					if newItem%monkey.divisibleBy == 0 {
						nextMonkey = &monkeys[monkey.trueGoesTo]
					} else {
						nextMonkey = &monkeys[monkey.falseGoesTo]
					}
					nextMonkey.items = append(nextMonkey.items, newItem)
				}
			}
		}
		// Find the two max
		var inspections []int
		for _, m := range monkeys {
			inspections = append(inspections, m.counter)
		}
		sort.Sort(sort.Reverse(sort.IntSlice(inspections)))
		fmt.Printf("Part Two : top2 inspections are %d and %d then solution is %d\n",
			inspections[0], inspections[1], inspections[0]*inspections[1])
	}

}

func inputMonkeysTest() [4]Monkey {
	return [...]Monkey{
		{
			items:       []int{79, 98},
			operation:   func(old int) int { return old * 19 },
			divisibleBy: 23,
			trueGoesTo:  2,
			falseGoesTo: 3,
		}, {
			items:       []int{54, 65, 75, 74},
			operation:   func(old int) int { return old + 6 },
			divisibleBy: 19,
			trueGoesTo:  2,
			falseGoesTo: 0,
		}, {
			items:       []int{79, 60, 97},
			operation:   func(old int) int { return old * old },
			divisibleBy: 13,
			trueGoesTo:  1,
			falseGoesTo: 3,
		}, {
			items:       []int{74},
			operation:   func(old int) int { return old + 3 },
			divisibleBy: 17,
			trueGoesTo:  0,
			falseGoesTo: 1,
		},
	}
}

func inputMonkeys() [8]Monkey {
	return [...]Monkey{
		{
			items:       []int{89, 74},
			operation:   func(old int) int { return old * 5 },
			divisibleBy: 17,
			trueGoesTo:  4,
			falseGoesTo: 7,
		}, {
			items:       []int{75, 69, 87, 57, 84, 90, 66, 50},
			operation:   func(old int) int { return old + 3 },
			divisibleBy: 7,
			trueGoesTo:  3,
			falseGoesTo: 2,
		}, {
			items:       []int{55},
			operation:   func(old int) int { return old + 7 },
			divisibleBy: 13,
			trueGoesTo:  0,
			falseGoesTo: 7,
		}, {
			items:       []int{69, 82, 69, 56, 68},
			operation:   func(old int) int { return old + 5 },
			divisibleBy: 2,
			trueGoesTo:  0,
			falseGoesTo: 2,
		}, {
			items:       []int{72, 97, 50},
			operation:   func(old int) int { return old + 2 },
			divisibleBy: 19,
			trueGoesTo:  6,
			falseGoesTo: 5,
		}, {
			items:       []int{90, 84, 56, 92, 91, 91},
			operation:   func(old int) int { return old * 19 },
			divisibleBy: 3,
			trueGoesTo:  6,
			falseGoesTo: 1,
		}, {
			items:       []int{63, 93, 55, 53},
			operation:   func(old int) int { return old * old },
			divisibleBy: 5,
			trueGoesTo:  3,
			falseGoesTo: 1,
		}, {
			items:       []int{50, 61, 52, 58, 86, 68, 97},
			operation:   func(old int) int { return old + 4 },
			divisibleBy: 11,
			trueGoesTo:  5,
			falseGoesTo: 4,
		},
	}
}
