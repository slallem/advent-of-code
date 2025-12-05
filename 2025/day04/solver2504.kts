
import java.io.File

val grid = File("./input.txt").readLines().filter { it.isNotBlank() }
val hzRange = 0..<grid.first().length
val vtRange = 0..<grid.size

fun getCell(c: Int, r: Int): Char {
    if (c !in hzRange || r !in vtRange) return '.'
    return grid[r][c]
}

val adj = listOf(
    Pair(-1,-1),
    Pair(-1,0),
    Pair(-1,1),
    Pair(0,-1),
    Pair(0,1),
    Pair(1,-1),
    Pair(1,0),
    Pair(1,1)
)

fun getAdjacentRollCount(c: Int, r: Int): Int {
    return adj.count {
        getCell(c + it.first, r + it.second) == '@'
    }
}

// Part One

var total1 = 0L
var grid2 = grid.toMutableList()
for (c in hzRange) {
    for (r in vtRange) {
        if (getCell(c, r) == '@') {
            if (getAdjacentRollCount(c, r) < 4) {
                grid2[r] = grid2[r].substring(0, c) + 'x' + grid2[r].substring(c + 1)
                total1++
            }
        }
    }
}
println("Part #1 the is $total1 forkliftable rolls")

// Part Two

var total2 = 0L

fun removeRolls(inputGrid: List<String>, hzRange: IntRange, vtRange: IntRange): List<String> {
    var removed: Int = 0
    var grid2 = inputGrid.toMutableList()
    for (c in hzRange) {
        for (r in vtRange) {
            if (inputGrid[r][c] == '@') {
                val adjCount = adj.count {
                    val nc = c + it.first
                    val nr = r + it.second
                    nc in hzRange && nr in vtRange && inputGrid[nr][nc] == '@'
                }
                if (adjCount < 4) {
                    grid2[r] = grid2[r].substring(0, c) + 'x' + grid2[r].substring(c + 1)
                    removed++
                }
            }
        }
    }
    //println(grid2.joinToString("\n") + "\n")
    //replace all x by .
    grid2 = grid2.map { it.replace("x", ".") }.toMutableList()
    total2 += removed
    //println("Removed $removed rolls")
    return grid2
}

var oldGrid = grid
var newGrid = oldGrid
do {
    oldGrid = newGrid
    newGrid = removeRolls(oldGrid, hzRange, vtRange)
} while (oldGrid != newGrid)

println("Part #2 has removed $total2 rolls")