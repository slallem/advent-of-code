
import java.io.File
import kotlin.collections.first
import kotlin.math.pow
import kotlin.text.substring
import kotlin.text.toCharArray

println("2023 --- Day 04: Scratchcards ---")

solve("./example1.txt")
solve("./input.txt")

fun solve(filename: String) {

    println()
    println("Solving file %s".format(filename))
    val lines = File(filename).readLines().filter { s: String -> s.isNotBlank() }

    // --- Parse lines, sucha as:
    // Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

    val winCards: MutableMap<Int, List<Int>> = mutableMapOf()
    val cards: MutableMap<Int, List<Int>> = mutableMapOf()
    lines.forEach { line ->
        val p1 = line.split(":")
        val cardNo = p1[0].substring(5).trim().toInt()
        val p2 = p1[1].split("|")
        winCards[cardNo] = p2[0].split(' ')
            .filter { s: String -> s.isNotBlank() }
            .map { s: String -> s.trim().toInt() }
            .toList()
        cards[cardNo] = p2[1].split(' ')
            .filter { s: String -> s.isNotBlank() }
            .map { s: String -> s.trim().toInt() }
            .toList()
    }

    // --- Part 1 - count points

    val score: MutableMap<Int, Long> = mutableMapOf()
    val points: MutableMap<Int, Int> = mutableMapOf()
    val occurrences: MutableMap<Int, Long> = mutableMapOf()
    var answer1 = 0L
    for (k in winCards.keys) {
        score[k] = 0
        points[k] = 0
        for (n in cards[k]!!) {
            if (winCards[k]!!.contains(n)) {
                score[k] = 2f.pow(points[k]!!).toLong()
                points[k] = points[k]!! + 1
            }
        }
        answer1 += score[k]!!
    }

    // --- Part 2 - Count occurrences

    for (k in winCards.keys) {
        occurrences[k] = 1
    }

    for (k in winCards.keys) {
        for (occ in 1..occurrences[k]!!) {
            for (i in 1..points[k]!!) {
                occurrences[k + i] = occurrences[k + i]!! + 1
            }
        }
    }

    val answer2 = occurrences.values.sum()

    // --- Display results

    println("Part #1 answer is %d".format(answer1))
    println("Part #2 answer is %d".format(answer2))

}
