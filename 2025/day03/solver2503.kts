
import java.io.File

val banks = File("./input.txt").readLines().map {
    line -> line.toCharArray().toList().map { it.digitToInt() }
}

// Part One

var total1 = 0L
banks.forEach {  bank ->
    val maxDizaine = bank.subList(0, bank.size - 1).max()
    val pos = bank.indexOf(maxDizaine)
    val maxUnite = bank.subList(pos+1, bank.size).max()
    val maxJoltage = (maxDizaine * 10) + maxUnite
    //println("Max joltage for $bank is $maxJoltage")
    total1 += maxJoltage
}

println("Part #1 total of max joltages is $total1")

// Part Two

var total2 = 0L
banks.forEach {  bank ->
    var curPos = 0
    val digits = mutableListOf<Int>()
    for (digit in 1..12) {
        val maxShift = bank.size - 12
        val frag = bank.subList(curPos, digit+maxShift)
        val maxDigit = frag.max()
        curPos += frag.indexOf(maxDigit)+1
        digits.add(maxDigit)
    }
    val maxJoltage = digits.joinToString("") { it.toString() }.toLong()
    //println("Max joltage for $bank is $maxJoltage")
    total2 += maxJoltage
}

println("Part #2 total of max joltages is $total2")