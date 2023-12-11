
import java.io.File
import java.lang.RuntimeException
import kotlin.collections.first
import kotlin.contracts.contract
import kotlin.math.max
import kotlin.math.pow
import kotlin.system.measureTimeMillis
import kotlin.text.substring
import kotlin.text.toCharArray

println("2023 --- Day 10: Pipe Maze ---")

measureTime { solve("./example1.txt",'F') }
measureTime { solve("./example2.txt",'7') }
measureTime { solve("./input.txt", '-') }

fun measureTime(func: () -> Unit) {
    val timeInMillis = measureTimeMillis { func() }
    println("(The operation took $timeInMillis ms)")
}

fun solve(filename: String, placeHolder: Char) {

    println()
    println("Solving file %s".format(filename))
    val lines = File(filename).readLines().filter { it.isNotBlank() }.toMutableList()

    // Parse lines
    val cells = mutableListOf<Cell>()
    for (j in 0..<lines.size) {
        for (i in 0..<lines[j].length) {
            cells.add(Cell(lines[j][i], i, j, null, null, null, null))
        }
    }
    var startCell: Cell? = null
    cells.forEach { cell ->
        if (cell.c == 'S') {
            cell.c = placeHolder
            startCell = cell
        }
    }
    cells.forEach { cell ->
        if (listOf('J','L','|').contains(cell.c)) {
            cell.north = cells.findValidCell(cell.x, cell.y - 1, listOf('7', 'F', '|'))
        }
        if (listOf('7','F','|').contains(cell.c)) {
            cell.south = cells.findValidCell(cell.x, cell.y + 1, listOf('J', 'L', '|'))
        }
        if (listOf('7','J','-').contains(cell.c)) {
            cell.west = cells.findValidCell(cell.x - 1, cell.y, listOf('L','F','-'))
        }
        if (listOf('F','L','-').contains(cell.c)) {
            cell.east = cells.findValidCell(cell.x + 1, cell.y, listOf('7', 'J', '-'))
        }
    }

    // --- Part 1

    val path = solvePipe(startCell!!)
    val answer1 = path.size / 2
    println("Part #1 answer is %d".format(answer1))

    // --- Part 2

    var answer2 = 0L
    for (j in 0..<lines.size) {
        for (i in 0..<lines[j].length) {
            if (!path.containsCell(i,j) && (path.countVerticalCrossings(i, j) % 2 == 1)) {
                answer2++
                val chars = lines[j].toCharArray()
                chars[i] = 'O'
                lines[j]= chars.joinToString("")
            }
        }
        //println(lines[j])
    }

    println("Part #2 answer is %d".format(answer2))

}

fun solvePipe(from: Cell) : List<Cell> {
    // returns all cells of the loop (or empty list if not a loop)
    if (from.c == '.') {
        return listOf()
    }
    var cur : Cell? = from
    val visited = mutableListOf<Cell>()
    while (cur != null) {
        visited.add(cur)
        val next = cur.getOptions().firstOrNull { !visited.contains(it) }
        if (next==null) {
            // 2 options: loop or dead end
            if (cur.getOptions().firstOrNull { it == from } == null) {
                // dead end
                visited.clear()
            }
            break
        }
        cur = next
    }
    return visited
}

fun List<Cell>.containsCell(x: Int, y: Int) : Boolean = findCell(x,y) != null

fun List<Cell>.findCell(x: Int, y: Int) : Cell? = this.firstOrNull { it.x == x && it.y == y }

fun List<Cell>.findValidCell(x: Int, y: Int, allowedChars: List<Char>) : Cell? {
    val cell = this.firstOrNull { it.x == x && it.y == y }
    return if (cell!=null && allowedChars.contains(cell.c)) cell else null
}

fun List<Cell>.countVerticalCrossings(x: Int, y: Int) : Int {
    // Count how many crossings (odd crossing = inside, pair crossing = outside)
    return this
        .filter { it.c=='|' || it.c=='L' || it.c=='J' }
        .filter { (it.y == y) && (it.x < x) }
        .size
}

class Cell(var c: Char,
                val x: Int, val y: Int,
                var north: Cell?,
                var south: Cell?,
                var west: Cell?,
                var east: Cell?
) {
    fun getOptions() : List<Cell> = listOf(north, south, west, east).filterNotNull().map { it }
}
