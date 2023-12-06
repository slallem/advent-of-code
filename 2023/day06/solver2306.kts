
import java.io.File
import java.lang.RuntimeException
import kotlin.collections.first
import kotlin.math.max
import kotlin.math.pow
import kotlin.text.substring
import kotlin.text.toCharArray

println("2023 --- Day 6: Wait For It ---")

solve("./example1.txt")
solve("./input.txt")

fun solve(filename: String) {

    println()
    println("Solving file %s".format(filename))
    val lines = File(filename).readLines().filter { s: String -> s.isNotBlank() }.toMutableList()

    // Parse lines

    val times = lines[0].split(":").last()
        .split(" ").filter { it.isNotBlank() }.map { it.toLong() }.toMutableList()
    val distances = lines[1].split(":").last()
        .split(" ").filter { it.isNotBlank() }.map { it.toLong() }.toMutableList()

    // --- Part 1

    val scores1 = (0..times.size-1).toList()
        .map { countOptionsBetterThan(times[it], distances[it]) }
        .toList()

    var answer1 = scores1[0]
    scores1.drop(1).forEach { answer1 *= it }

    println("Part #1 answer is %d".format(answer1))

    // --- Part 2

    val time = lines[0].split(":").last().replace(" ","").trim().toLong()
    val distance = lines[1].split(":").last().replace(" ","").trim().toLong()

    val answer2 = countOptionsBetterThan(time, distance)

    println("Part #2 answer is %d".format(answer2))

}

fun countOptionsBetterThan(maxTime: Long, best: Long) : Long {
    var counter = 0L
    for (pressTime in 1..maxTime-1) {
        if (calcDistance(pressTime, maxTime) > best) {
            counter++
        }
    }
    return counter
}

fun calcDistance(pressTime: Long, maxTime: Long) : Long = pressTime * (maxTime - pressTime)

