
import java.io.File
import java.lang.RuntimeException
import kotlin.collections.first
import kotlin.contracts.contract
import kotlin.math.max
import kotlin.math.pow
import kotlin.system.measureTimeMillis
import kotlin.text.substring
import kotlin.text.toCharArray

println("2023 --- Day 12: Hot Springs ---")

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

    val springDefs = mutableListOf<Pair<String, List<Int>>>()
    for (line in lines) {
        val v = line.split(" ")
        val status = v.first()
        val groups = v.last().split(",").map { it.toInt() }
        springDefs.add(Pair(status, groups))
    }

    // --- Part 1

    val answer1 = springDefs.map {p -> countCombos(p.first, p.second) }.sum()
    println("Part #1 answer is %d".format(answer1))

    // --- Part 2

//    val answer2 = 0
//    println("Part #2 answer is %d".format(answer2))

}

fun countCombos(def: String, groups: List<Int>) : Long {
    var comboCount = 0L
    val chars = def.toCharArray()
    val qmCount = chars.count { it == '?' }
    for (filler in 0..<power(2, qmCount)) {
        val bits = filler.toULong().toString(radix = 2).reversed() + "0".repeat(20)
        var filled = ""
        var index = -1
        chars.forEach { c ->
            if (c=='?') {
                index++
                filled += if (bits[index] == '0') '.' else '#'
            } else {
                filled += c
            }
        }
        //var status = "no"
        if (matchGroups(filled, groups)) {
            comboCount++
            //status = "YES"
        }
        //println("%s : %s %s".format(bits, filled, status))
    }
    //println("%s %s ==> %d arrangements".format(def, groups, comboCount))
    return comboCount
}

fun matchGroups(def: String, groups: List<Int>) : Boolean {
    val g : List<Int> = def.split(".").map { it.length }.filter { it > 0 }
    return g == groups
}

fun power(baseVal: Int, exponentVal: Int): Long {
    val base = baseVal
    var exponent = exponentVal
    var result : Long = 1

    while (exponent != 0) {
        result *= base.toLong()
        --exponent
    }
    return result
}