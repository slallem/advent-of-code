
import java.io.File

val inputFile = File("./input.txt")

val lines: List<String> = inputFile.readLines()
    .filter { it.isNotBlank() }
    .map { it.replace(Regex("\\s+"), " ").trim() }

val operators = lines
    .last()
    .split(" ")

val values: List<List<Long>> = lines
    .subList(0, lines.size-1)
    .map {
        it.split(" ").map(String::toLong)
    }

// Part One

fun List<Long>.product(): Long = reduce { acc, num -> acc * num }

val results1: List<Long> = operators.mapIndexed { index, operator ->
    when (operator) {
        "+" -> values.sumOf { it[index] }
        "*" ->  values.map { it[index] }.product()
        else -> throw IllegalArgumentException("Unrecognised operator: '$operator'")
    }
}
//println("values: $values")
//println("operators: $operators")
//println("Part #1 totals are $results1")
val total1 = results1.sum()
println("Part #1 grand total is $total1")
println()

// Part Two

val rawValues: List<String> = inputFile.readLines()
    .filter { it.isNotBlank() }
    .subList(0, lines.size-1)

var lines2 = ""
val maxLineLen = rawValues.maxOf { it.length }
for (i in 0..<maxLineLen) {
    for (j in 0..rawValues.lastIndex) {
        if (i>rawValues[j].length-1) {
            lines2 += ' '
        } else {
            lines2 += when (rawValues[j][i]) {
                '+', '*' -> ';'
                else -> rawValues[j][i]
            }
        }
    }
    lines2 += ' '
}

val values2 = lines2
    .replace(List(rawValues.size+1){" "}.joinToString(""), ";")
    .replace(";;",";")
    .replace(Regex("\\s+"), " ")
    .trim()
    .split(";")
    .map { it.trim() }
    //.also { println(it) }
    .map { it.split(" ").map { it.toLong() }}

//println(values2)
//println(operators)
val results2: List<Long> = operators.mapIndexed { index, operator ->
    when (operator) {
        "+" -> values2[index].sum()
        "*" ->  values2[index].product()
        else -> throw IllegalArgumentException("Unrecognised operator: '$operator'")
    }
}
val total2 = results2.sum()
println("Part #2 grand total is $total2")
println()

