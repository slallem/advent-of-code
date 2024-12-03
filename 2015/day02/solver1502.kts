import java.io.File
import kotlin.system.exitProcess

// Part One
var lines = File("./input.txt").readLines().filterNotNull()

val total1 = lines.map { line ->
    val (l, w, h) = line.split("x").map { it.toInt() }
    2*l*w + 2*w*h + 2*h*l + listOf(l*w, w*h, h*l).min()
}.sum()

println("Part #1 is $total1")

// Part Two

val total2 = lines.map { line ->
    val (x, y, z) = line.split("x").map { it.toInt() }.sorted()
    (x+x+y+y) + (x*y*z)
}.sum()

println("Part #2 is $total2")