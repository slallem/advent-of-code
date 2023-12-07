
import java.io.File
import java.lang.RuntimeException
import kotlin.collections.first
import kotlin.contracts.contract
import kotlin.math.max
import kotlin.math.pow
import kotlin.system.measureTimeMillis
import kotlin.text.substring
import kotlin.text.toCharArray

println("2023 --- Day 7: Camel Cards ---")

// Misreading explanations lead to spaghetti code and endless debugging :)
// (many dead code cleaned afterward !)

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

    val hands = mutableListOf<Hand>()
    for (line in lines) {
        val v = line.trim().split(" ")
        val h = v.first()
        val bid = v.last().toLong()
        hands.add(Hand(h, sortable(h), bid))
    }

    // --- Part 1

    var answer1 = 0L
    hands.sortBy { it.sort }
    hands.forEachIndexed { i, h ->  answer1 += ((i+1) * h.bid) }

    hands.forEachIndexed() { i, v ->
        //println("%d : %s --> %s (%d)".format(i+1, v.hand, v.sort, v.bid))
    }

    println("Part #1 answer is %d".format(answer1))

    // --- Part 2

    var answer2 = 0L
    hands.forEach { it.sort = sortable2(it.hand) }
    hands.sortBy { it.sort }
    hands.forEachIndexed { i, h -> answer2 += ((i+1) * h.bid) }

    hands.forEachIndexed() { i, v ->
       //println("%d : %s --> %s (%d)".format(i+1, v.hand, v.sort, v.bid))
    }

    println("Part #2 answer is %d".format(answer2))

}

fun sortable(s: String) : String {
    val h = s
        .replace("T", "B")
        .replace("J","C")
        .replace("Q", "D")
        .replace("K","E")
        .replace("A","F")
    // Count occurrences (Map Card -> Count)
    val f = mutableMapOf<Char, Int>()
    for (c in h.toCharArray()) {
        if (f.containsKey(c)) {
            f[c] = f[c]!! + 1
        } else {
            f[c] = 1
        }
    }
    val handType = f.values.map { it.toString() }.sortedByDescending { it }.joinToString("")
    return "%s-%s".format(handType, h)
}

fun sortable2(s: String) : String {
    val h = s
        .replace("T", "B")
        .replace("J","0") // J is lowest
        .replace("Q", "D")
        .replace("K","E")
        .replace("A","F")
    // Count occurrences
    val f = mutableMapOf<Char, Int>()
    for (c in h.toCharArray()) {
        if (f.containsKey(c)) {
            f[c] = f[c]!! + 1
        } else {
            f[c] = 1
        }
    }
    // Evaluate occurrences of cards (except J)
    var hsTmp = "" // not 250492861 not 250646090 too high
    for (i in 5 downTo 1) {
        hsTmp += f.filter { it.key != '0' }
            .filter { it.value == i }
            .map{it.key.toString().repeat(it.value)}
            .sortedDescending()
            .joinToString("")
    }
    // If hand contains one or more jacks (jacks only excepted)
    // then jacks counts as the best known occurrence to improve hand type to the max
    if (f.containsKey('0') && f.size > 1) {
        val bestOccurrence = hsTmp[0]
        f[bestOccurrence] = f[bestOccurrence]!! + f['0']!!
        f.remove('0')
    }
    val handType = f.values.map { it.toString() }.sortedByDescending { it }.joinToString("")
    return "%s-%s".format(handType, h)
}

data class Hand(val hand: String, var sort: String, val bid : Long)
