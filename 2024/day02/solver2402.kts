
import java.io.File

val values = File("./input.txt").readLines().map { s -> s.split(" ").filterNotNull().map { it.toInt() } }

// Part One

val safeCount = values.count { isSafe(it) }

println("Part #1 total is %d".format(safeCount))

// Part Two

val total2 = values.count { isSafe2(it) }

println("Part #2 total is %d".format(total2))

// Helper functions

fun isSafe(items: List<Int>) : Boolean {
    val steps = (0..items.size - 2).map { i -> items[i + 1] - items[i] }
    val allPositive = steps.filter { it > 0 }.size == (items.size - 1)
    val allNegative = steps.filter { it < 0 }.size == (items.size - 1)
    return (allPositive || allNegative) && (steps.filter { Math.abs(it) in 1..3 }.size == (items.size - 1))
}

fun isSafe2(items: List<Int>) : Boolean {
    val variations = (0..items.size-1).map { i -> items.toMutableList().also { it.removeAt(i) } }
    return isSafe(items) || variations.firstOrNull { isSafe(it) } != null
}
