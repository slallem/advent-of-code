
import java.io.File

val values = File("./input.txt").readLines().map { s -> s.split(" ").filterNotNull() }
var leftValues = values.map { it.first().toInt() }.sorted()
var rightValues = values.map { it.last().toInt() }.sorted()

// Part One

val distances = leftValues.zip(rightValues).map{ Math.abs(it.first - it.second) }

println("Part #1 total is %d".format(distances.sum()))

// Part Two

val total2 = leftValues.map { it * rightValues.filter { r -> r == it }.size }.sum()

println("Part #2 total is %d".format(total2))
