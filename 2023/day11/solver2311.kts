
import java.io.File
import java.lang.RuntimeException
import kotlin.collections.first
import kotlin.contracts.contract
import kotlin.math.max
import kotlin.math.pow
import kotlin.system.measureTimeMillis
import kotlin.text.substring
import kotlin.text.toCharArray

println("2023 --- Day 11: Cosmic Expansion ---")

measureTime { solve("./example1.txt") }
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

    val galaxies = mutableListOf<Galaxy>()
    val colEpands = mutableListOf<Int>()
    val rowEpands = mutableListOf<Int>()
    var galaxyId = 0
    for (j in 0..<lines.size) {
        var rowIsEmpty = true
        for (i in 0..<lines[0].length) {
            if (lines[j][i] == '#') {
                galaxies.add(Galaxy(++galaxyId, i, j, i.toLong(), j.toLong()))
                rowIsEmpty = false
            }
        }
        if (rowIsEmpty) {
            rowEpands.add(j)
        }
    }
    for (i in 0..<lines[0].length) {
        var colIsEmpty = true
        loopJ@ for (j in 0..<lines.size) {
            if (lines[j][i] == '#') {
                colIsEmpty = false
                break@loopJ
            }
        }
        if (colIsEmpty) {
            colEpands.add(i)
        }
    }

    // Expand empty cols and rows
    colEpands.forEach { col -> galaxies.filter { galaxy -> galaxy.ox > col }.forEach { galaxy -> galaxy.x++ } }
    rowEpands.forEach { row -> galaxies.filter { galaxy -> galaxy.oy > row }.forEach { galaxy -> galaxy.y++ } }

    // --- Part 1

    val combinations = mutableListOf<Pair<Galaxy,Galaxy>>()
    for (z1 in 0..<galaxies.size-1) {
        for (z2 in z1+1..<galaxies.size) {
            combinations.add(Pair(galaxies[z1],galaxies[z2]))
        }
    }

    combinations.forEach {p ->
        //println("between %d and %d = %d".format(p.first.id, p.second.id, p.first.manhattanDistanceTo(p.second) ))
    }

    val answer1 = combinations.map {p -> p.first.manhattanDistanceTo(p.second) }.sum()
    println("Part #1 answer is %d".format(answer1))

    // --- Part 2

    // Reset abnd expand empty cols and rows
    galaxies.forEach { g ->
        g.x = g.ox.toLong()
        g.y = g.oy.toLong()
    }
    colEpands.forEach { col -> galaxies.filter { galaxy -> galaxy.ox > col }.forEach { galaxy -> galaxy.x += 1000000-1 } }
    rowEpands.forEach { row -> galaxies.filter { galaxy -> galaxy.oy > row }.forEach { galaxy -> galaxy.y += 1000000-1 } }

    val answer2 = combinations.map {p -> p.first.manhattanDistanceTo(p.second) }.sum()
    println("Part #2 answer is %d".format(answer2))

}

data class Galaxy(val id: Int, val ox: Int, val oy: Int, var x: Long, var y: Long) {
    fun manhattanDistanceTo(another: Galaxy) : Long {
        return Math.abs(x - another.x) + Math.abs(y - another.y)
    }
}
