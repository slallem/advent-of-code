
import java.io.File

val input = File("./input.txt").readText()

// Part One

val muls = """mul\([0-9]+\,[0-9]+\)""".toRegex().findAll(input).map { it.value }
val values = muls.map { mul ->
    val ints = "[0-9]+".toRegex().findAll(mul).map { it.value.toInt() }
    ints.first() * ints.last()
}

val total1 = values.sum()

println("Part #1 total is %d".format(total1))

// Part Two

val mulsDoDont = """mul\([0-9]+\,[0-9]+\)|do\(\)|don\'t\(\)""".toRegex().findAll(input).map { it.value }
var total2 : Int = 0
var enabled = true
mulsDoDont.forEach { op ->
    when {
        op == "do()" -> enabled = true
        op == "don't()" -> enabled = false
        enabled -> {
            val ints = "[0-9]+".toRegex().findAll(op).map { it.value.toInt() }
            total2 += ints.first() * ints.last()
        }
    }
}

println("Part #2 total is %d".format(total2))
