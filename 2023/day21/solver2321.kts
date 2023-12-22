
import java.io.File
import java.lang.RuntimeException
import kotlin.collections.first
import kotlin.contracts.contract
import kotlin.math.max
import kotlin.math.pow
import kotlin.system.measureTimeMillis
import kotlin.text.substring
import kotlin.text.toCharArray

println("2023 --- Day 21: Step Counter ---")

measureTime { solve("./example1.txt") }
//measureTime { solve("./input.txt") }

fun measureTime(func: () -> Unit) {
    val timeInMillis = measureTimeMillis { func() }
    println("(The operation took $timeInMillis ms)")
}

fun solve(filename: String) {

    println()
    println("Solving file %s".format(filename))
    val lines = File(filename).readLines().filter { it.isNotBlank() }.toMutableList()

    // Parse lines
    val board = Board(lines)

    // --- Part 1

    var positions: Set<Pair<Int,Int>> = setOf(board.start)
    for (step in 1..64) {
        positions = board.computeSteps(positions)
    }
    val answer1 = positions.size
    println("Part #1 answer is %d".format(answer1))

    // --- Part 2

    positions = setOf(board.start)
    for (step in 1..100) {
        positions = board.computeStepsPart2(positions)
        println("Step %d gives %d".format(step, positions.size))
    }
    val answer2 = 0
    println("Part #2 answer is %d".format(answer2))

}

class Board(var data: MutableList<String>) {
    var start = Pair(-1,-1)
    var width = -1
    var height = -1
    init {
        // Boundings
        width = data[0].length
        height = data.size
        // Calculates starting point
        for (y in 0..<data.size) {
            val x = data[y].indexOf('S')
            if (x>=0) {
                start = Pair(x,y)
                data[y] = data[y].replace("S",".")
            }
        }
    }
    fun getCharAt(x: Int, y: Int) : Char {
        return if (x<0 || x>=width || y<0 || y>= height) '#' else data[y][x]
    }
    fun computeMoves(x: Int, y: Int) : List<Pair<Int,Int>> {
        return listOf(
            Pair(x-1,y),
            Pair(x+1,y),
            Pair(x,y-1),
            Pair(x,y+1))
            .filter { p -> getCharAt(p.first, p.second) == '.' }
    }
    fun computeSteps(positions: Set<Pair<Int,Int>>) : Set<Pair<Int,Int>> {
        return positions.flatMap { p -> computeMoves(p.first, p.second) }.toSet()
    }
    // Part 2
    fun getCharAtInfinite(x: Int, y: Int) : Char {
        return data[y.mod(height)][x.mod(width)]
    }
    fun computeMovesPart2(x: Int, y: Int) : List<Pair<Int,Int>> {
        return listOf(
            Pair(x-1,y),
            Pair(x+1,y),
            Pair(x,y-1),
            Pair(x,y+1))
            .filter { p -> getCharAtInfinite(p.first, p.second) == '.' }
    }
    fun computeStepsPart2(positions: Set<Pair<Int,Int>>) : Set<Pair<Int,Int>> {
        return positions.flatMap { p -> computeMovesPart2(p.first, p.second) }.toSet()
    }
}
