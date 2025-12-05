
import java.io.File

val ranges = File("./input.txt").readLines().joinToString { it }.split(",").map {
    val range = it.split("-")
    range.first().toLong() .. range.last().toLong()
}

// Part One

var total1 = 0L
ranges.forEach {  range ->
    for (id in range) {
        //println("Testing ID $id")
        val idStr = id.toString()
        val idHalfSize = idStr.length/2
        val left = idStr.take(idHalfSize)
        val right: String = idStr.substring(idHalfSize)
        if (left == right) {
            //println("Invalid ID $id")
            total1 += id
        }
    }
}

println("Part #1 total of invalid IDs is $total1")

// Part Two

var invalids = mutableSetOf<Long>()
ranges.forEach {  range ->
    for (id in range) {
        //println("Testing ID $id")
        val idStr = id.toString()
        for (fragSize in 1..idStr.length/2) {
            val frag = idStr.take(fragSize)
            val repeats = (idStr.length/fragSize)
            val repeated = List(repeats) { frag }.joinToString("")
            if (repeated == idStr) {
                //println("Invalid ID $id")
                invalids += id
            }
        }
    }
}

val total2 = invalids.sum()

println("Part #2 total of invalid IDs is $total2")