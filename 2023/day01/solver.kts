
import java.io.File

val replacements = mapOf( "one" to '1', "two" to '2', "three" to '3',
        "four" to '4', "five" to '5', "six" to '6', "seven" to '7',
        "eight" to '8', "nine" to '9')

//var lines = File("./example1.txt").readLines()
//var lines = File("./example2.txt").readLines()
var lines = File("./input.txt").readLines()

var total1 = 0
var total2 = 0
lines.forEach { line ->
    total1 += evalString(line)
    total2 += "%s%s".format(getFirstDigit(line), getLastDigit(line)).toInt()
}

println("Part #1 total is %d".format(total1))
println("Part #2 total is %d".format(total2))

fun evalString(s: String) : Int {
    val numbers = s.toCharArray().filter { c -> c in '1'..'9' }
    return if (numbers.isEmpty()) 0 else "%s%s".format(numbers.first(), numbers.last()).toInt()
}

fun getFirstDigit(s: String): Char {
    var remaining = s
    loop1@ while (remaining.isNotEmpty()) {
        loop2@ for (replacement in replacements) {
            if (remaining.startsWith(replacement.key)) {
                return replacement.value
            }
        }
        // Move on by one char
        if (remaining.first() in '1'..'9')
            return remaining.first()
        remaining = remaining.substring(1)
    }
    return ' ' // notfound
}

fun getLastDigit(s: String): Char {
    var remaining = s
    loop1@ while (remaining.isNotEmpty()) {
        loop2@ for (replacement in replacements) {
            if (remaining.endsWith(replacement.key)) {
                return replacement.value
            }
        }
        // Move on by one char
        if (remaining.last() in '0'..'9')
            return remaining.last()
        remaining = remaining.substring(0, remaining.length - 1)
    }
    return ' ' // notfound
}
