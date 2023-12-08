import java.io.File
import java.math.BigDecimal
import kotlin.system.measureTimeMillis

println("2023 --- Day 8: Haunted Wasteland ---")

measureTime { solve("./example1.txt") }
measureTime { solve("./example2.txt") }
measureTime { solve("./example3.txt") }
measureTime { solve("./input.txt") }

fun measureTime(func: () -> Unit) {
    val timeInMillis = measureTimeMillis { func() }
    println("(The operation took $timeInMillis ms)")
}

fun solve(filename: String) {

    println()
    println("Solving file %s".format(filename))
    val lines = File(filename).readLines().filter { it.isNotBlank() }.toMutableList()

    // Parse lines

    val commands = lines.removeFirst().trim().toCharArray().toList()
    val cells = mutableMapOf<String, Cell>()
    for (line in lines) {
        val v = line.trim().split(" = (")
        val id = v.first()
        val rv = v.last().replace(")", "").split(",")
        cells[id] = Cell(id, rv.first().trim(), rv.last().trim(), id.last())
    }

    // --- Part 1

    var answer1 = 0L
    if (cells.containsKey("AAA")) {
        var pos = "AAA"
        var idx = -1
        while (pos != "ZZZ") {
            idx = (idx + 1) % commands.size
            answer1++
            if (commands[idx] == 'R') {
                pos = cells[pos]!!.right
            } else { // 'L'
                pos = cells[pos]!!.left
            }
        }
        println("Part #1 answer is %d".format(answer1))
    }

    // --- Part 2

    var cellsA: MutableList<Cell> = cells.keys.filter { it.endsWith("A") }.map { cells[it]!! }.toMutableList()
    var distancesToZ = mutableListOf<Long>()
    for (cell in cellsA) {
        // For each A-ended cell estimate distance to reach a Z-ended cell
        var idx2 = -1
        var pos = cell.id
        var distance = 0L
        while (!pos.endsWith("Z")) {
            idx2 = (idx2 + 1) % commands.size
            distance++
            if (commands[idx2] == 'R') {
                pos = cells[pos]!!.right
            } else { // 'L'
                pos = cells[pos]!!.left
            }
        }
        distancesToZ.add(distance)
    }

    val answer2 = ppcm(distancesToZ)

    println("Part #2 answer is %s".format(answer2.toString()))

}

fun allEndWithZ(cells: List<Cell>): Boolean {
    for (cell in cells) {
        if (cell.lastChar != 'Z') {
            return false
        }
    }
    return true
}

data class Cell(val id: String, val left: String, var right: String, val lastChar: Char)

fun ppcm(a: Long, b: Long): Long {
    val larger = if (a > b) a else b
    val maxPpcm = a * b
    var ppcm = larger
    while (ppcm <= maxPpcm) {
        if (ppcm % a == 0L && ppcm % b == 0L) {
            return ppcm
        }
        ppcm += larger
    }
    return maxPpcm
}

fun ppcm(numbers: List<Long>): Long {
    var result = numbers[0]
    for (i in 1 ..< numbers.size) {
        result = ppcm(result, numbers[i])
    }
    return result
}