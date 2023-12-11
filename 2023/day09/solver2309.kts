
import java.io.File
import java.lang.RuntimeException
import kotlin.collections.first
import kotlin.contracts.contract
import kotlin.math.max
import kotlin.math.pow
import kotlin.system.measureTimeMillis
import kotlin.text.substring
import kotlin.text.toCharArray

println("2023 --- Day 9: Mirage Maintenance ---")

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

    val series = lines.map { it.split(" ").map { it.toLong() }.toList() }

    // --- Part 1

    val answer1 = series.map { findNext(it) }.sum()
    println("Part #1 answer is %d".format(answer1))

    // --- Part 2

    val answer2 = series.map { findPrevious(it) }.sum()
    println("Part #2 answer is %d".format(answer2))

}

fun findNext(serie: List<Long>) : Long {
    val subSeries = mutableListOf<List<Long>>()
    subSeries.addLast(serie)
    while (!allZeroes(subSeries.last())) {
        val s = (0..<subSeries.last().size - 1)
            .map { subSeries.last()[it + 1] - subSeries.last()[it] }
            .toList()
        subSeries.addLast(s)
    }
    var lastdiff = 0L
    var nextVal = 0L
    for (i in subSeries.size downTo 1) {
        val lastValueUp = subSeries[i-1].last()
        nextVal = lastValueUp + lastdiff
        // prepare next iteration
        lastdiff = nextVal
    }
    return nextVal
}

fun findPrevious(serie: List<Long>) : Long {
    val subSeries = mutableListOf<List<Long>>()
    subSeries.addLast(serie)
    while (!allZeroes(subSeries.last())) {
        val s = (0..<subSeries.last().size - 1)
            .map { subSeries.last()[it + 1] - subSeries.last()[it] }
            .toList()
        subSeries.addLast(s)
    }
    var lastdiff = 0L
    var prevVal = 0L
    for (i in subSeries.size downTo 1) {
        val firstValueUp = subSeries[i-1].first()
        prevVal = firstValueUp - lastdiff
        // prepare next iteration
        lastdiff = prevVal
    }
    return prevVal
}

fun allZeroes(serie: List<Long>) : Boolean = serie.none { it != 0L }