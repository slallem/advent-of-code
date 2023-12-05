
import java.io.File
import java.lang.RuntimeException
import kotlin.collections.first
import kotlin.math.pow
import kotlin.text.substring
import kotlin.text.toCharArray

println("2023 --- Day 5: If You Give A Seed A Fertilizer ---")

solve("./example1.txt")
solve("./input.txt")

fun solve(filename: String) {

    println()
    println("Solving file %s".format(filename))
    val lines = File(filename).readLines().filter { s: String -> s.isNotBlank() }.toMutableList()

    // Parse lines

    val seeds = lines.removeFirst().split(":").last()
        .split(" ").filter { it.isNotBlank() }.map { it.toLong() }.toMutableList()
    var category = Category("","","", mutableListOf())
    val categories : MutableMap<String, Category> = mutableMapOf()
    lines.forEach { line ->
        if ("0123456789".contains(line[0])) {
            // Values
            val triplet = line.split(" ").filter { it.isNotBlank() }.map { it.toLong() }
            category.ranges.add(ValueRange(triplet[1], triplet[0], triplet[2]))
        } else {
            // Title like "soil-to-fertilizer map:"
            val mapId = line.split("map:").first().trim()
            val couple = mapId.split("_to_")
            category = Category(mapId, couple.first(), couple.last(), mutableListOf())
            categories[category.id] = category
        }
    }

    // --- Part 1 - count points

    val locations = seeds
        .map { categories["seed-to-soil"]!!.mapVal(it) }
        .map { categories["soil-to-fertilizer"]!!.mapVal(it) }
        .map { categories["fertilizer-to-water"]!!.mapVal(it) }
        .map { categories["water-to-light"]!!.mapVal(it) }
        .map { categories["light-to-temperature"]!!.mapVal(it) }
        .map { categories["temperature-to-humidity"]!!.mapVal(it) }
        .map { categories["humidity-to-location"]!!.mapVal(it) }

    val lowestLocation = locations.minOf { it }
    val answer1 = lowestLocation

    println("Part #1 answer is %d".format(answer1))

    // --- Part 2

    // Consider seeds couple values as ranges
    val seedRanges = mutableListOf<SimpleRange>()
    while (seeds.isNotEmpty()) {
        val start = seeds.removeFirst()
        val len = seeds.removeFirst()
        seedRanges.add(SimpleRange(start, start+len))
    }

    // Chain mapping of ranges (splitting ranges into smaller pieces when needed)
    val soilRanges = categories["seed-to-soil"]!!.mapRanges(seedRanges)
    val fertilizerRanges = categories["soil-to-fertilizer"]!!.mapRanges(soilRanges)
    val waterRanges = categories["fertilizer-to-water"]!!.mapRanges(fertilizerRanges)
    val lightRanges = categories["water-to-light"]!!.mapRanges(waterRanges)
    val tempRanges = categories["light-to-temperature"]!!.mapRanges(lightRanges)
    val humidityRanges = categories["temperature-to-humidity"]!!.mapRanges(tempRanges)
    val locationRanges = categories["humidity-to-location"]!!.mapRanges(humidityRanges)

    val answer2 = locationRanges.map { it.from }.min()

    println("Part #2 answer is %d".format(answer2))

}

data class Category(var id: String, var idFrom: String, var idTo: String, val ranges : MutableList<ValueRange>) {
    fun mapVal(value: Long): Long {
        var result = value
        for (r in ranges) {
            if (value in r.source..r.source+r.length) {
                result = r.destination + (value - r.source)
                break
            }
        }
        return result
    }
    fun mapRanges(inputRanges: List<SimpleRange>): List<SimpleRange> {
        val results = mutableSetOf<SimpleRange>()
        for (ir in inputRanges) {
            val subRanges = ir.splitRange(getBreaks()) // split range into smaller ones (if applicable)
                .map { SimpleRange(mapVal(it.from), mapVal(it.to)) } // then transpose them
            results.addAll(subRanges)
        }
        return results.toList()
    }
    private fun getBreaks() : List<Long> {
        val results = mutableListOf<Long>()
        ranges.forEach {
            results.add(it.source)
            results.add(it.source + it.length + 1)
        }
        return results
    }
}

data class SimpleRange(val from: Long, val to: Long) {
    fun splitRange(breaks: List<Long>) : List<SimpleRange> {
        // Given a range, split it into several sub-ranges according to breaks
        val results = mutableListOf<SimpleRange>()
        val stops = mutableListOf<Long>(from, to+1)
        stops.addAll(breaks.filter { it in from..to })
        stops.sort()
        for (i in 0..stops.size-2) {
            results.add(SimpleRange(stops[i], stops[i+1]-1))
        }
        return results
    }
}
data class ValueRange(val source: Long, val destination: Long, val length: Long)