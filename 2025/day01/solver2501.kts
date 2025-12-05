
import java.io.File

val values = File("./input.txt").readLines().map {
    s -> s[0] to s.substring(1).toInt()
}

// Part One

var pos = 50
val zeroes: Int = values.map {
    when (it.first) {
        'L' ->  pos = (pos - it.second) % 100
        'R' ->  pos = (pos + it.second) % 100
    }
    pos
}.count { it == 0 }

println("Part #1 points to zero %d times".format(zeroes))

// Part Two

val dial = Dial(50)
values.forEach {
    dial.turn(it.first, it.second)
}

println("Part #2 points to zero %d times".format(dial.crossedZero))

// -----------------

class Dial(
    var pos: Int = 50
) {
    var crossedZero = 0
    fun turn(direction: Char, value: Int) {
        val step = if (direction == 'L') -1 else 1
        for (i in 1..value) {
            pos = (100 + pos + step) % 100
            if (pos == 0) { crossedZero ++ }
        }
        //println("Dial is rotated $direction $value to position $pos")
    }
}