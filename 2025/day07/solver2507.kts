import java.io.File

data class Pos(val row: Int, val col: Int) {
    fun offset(deltaRow: Int, deltaCol: Int) = Pos(row + deltaRow, col + deltaCol)
}

class Grid(lines: List<String>) {
    private val grid = lines
    val rows = grid.size
    val cols = if (grid.isNotEmpty()) grid[0].length else 0

    fun get(pos: Pos): Char {
        return if (pos.row in 0 until rows && pos.col in 0 until cols) {
            grid[pos.row][pos.col]
        } else ' '
    }

    fun findFirst(char: Char): Pos? {
        for (row in 0 until rows) {
            for (col in 0 until cols) {
                if (grid[row][col] == char) {
                    return Pos(row, col)
                }
            }
        }
        return null
    }
}

val inputFile = File("./input.txt")

val grid = Grid(inputFile.readLines())

// Part One

val startPos = grid.findFirst('S') ?: throw IllegalStateException("Could not find the starting position")
val positionsToEvaluate = mutableListOf<Pos>(startPos.offset(2, 0))

val beams = mutableSetOf<Int>()
var split = 0

for (row in 0 until grid.rows step 2) {
    for (col in 0 until grid.cols) {
        val pos = Pos(row, col)
        val char = grid.get(pos)
        when (char) {
            'S' -> beams.add(col)
            '^' -> {
                if (beams.contains(pos.col)) {
                    split++
                    beams.remove(col)
                    beams.add(col - 1)
                    beams.add(col + 1)
                } else {
                    // no beam present in this column, splitter is useless
                }
            }
        }
    }
}

println("Part #1 beam is split $split times")
println()

// Part Two

var beamCounts = mutableMapOf<Int, Long>()
beamCounts[startPos.col] = 1L

for (row in startPos.row until grid.rows step 2) {
    val nextBeamCounts = mutableMapOf<Int, Long>()
    
    for ((col, count) in beamCounts) {
        val char = grid.get(Pos(row, col))
        when (char) {
            '^' -> {
                // Split: add count to left and right positions
                nextBeamCounts[col - 1] = (nextBeamCounts[col - 1] ?: 0) + count
                nextBeamCounts[col + 1] = (nextBeamCounts[col + 1] ?: 0) + count
            }
            else -> {
                // Continue straight down
                nextBeamCounts[col] = (nextBeamCounts[col] ?: 0) + count
            }
        }
    }
    
    beamCounts = nextBeamCounts
}

val totalPaths = beamCounts.values.sum()

println("Part #2 there are $totalPaths total beam paths")
println()
