
import java.io.File

val inputFile = File("./input.txt")
val ranges = inputFile.readLines()
    .filter { it.isNotBlank() }
    .filter { it.contains("-") }
    .map {
        val values = it.split("-")
            .map { it.trim().toLong() }
            .toList()
        values.first() .. values.last()
    }

val ids = inputFile.readLines()
    .filter { it.isNotBlank() }
    .filter { !it.contains("-") }
    .map { it.trim().toLong() }

// Part One

var total1 = ids.count { id ->
    ranges.firstOrNull { range -> id in range } != null
}
println("Part #1 there is $total1 fresh ingredients")

// Part Two (vibecoded / windsurf Cascade / Claude Sonnet 4.5)

val mergedRanges = ranges
    .sortedBy { it.first }
    .fold(mutableListOf<LongRange>()) { merged, current ->
        if (merged.isEmpty() || merged.last().last < current.first - 1) {
            merged.add(current)
        } else {
            val last = merged.removeLast()
            merged.add(last.first..maxOf(last.last, current.last))
        }
        merged
    }

val totalElements = mergedRanges.sumOf { it.last - it.first + 1 }
//println("Part #2 merged ranges: $mergedRanges")
println("Part #2 total elements in ranges: $totalElements")


