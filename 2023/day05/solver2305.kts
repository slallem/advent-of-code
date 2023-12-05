
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
    val lines = File(filename).readLines().filter { s: String -> s.isNotBlank() }

    // Parse lines

    val seeds = lines.removeFirst().split(":").last()
        .split(" ").filter { it.isNotBlank() }.map { it.toLong() }.toList()
    var category = Category("","","", mutableListOf())
    val categories : MutableMap<String, Category> = mutableMapOf()
    lines.forEach { line ->
        if ("0123456789".contains(line[0])) {
            // Values
            val triplet = line.split(" ").filter { it.isNotBlank() }.map { it.toLong() }
            category.ranges.addLast(ValueRange(triplet[1], triplet[0], triplet[2]))
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
        .map { categories["seed-to-soil"]!!.map(it) }
        .map { categories["soil-to-fertilizer"]!!.map(it) }
        .map { categories["fertilizer-to-water"]!!.map(it) }
        .map { categories["water-to-light"]!!.map(it) }
        .map { categories["light-to-temperature"]!!.map(it) }
        .map { categories["temperature-to-humidity"]!!.map(it) }
        .map { categories["humidity-to-location"]!!.map(it) }

    val lowestLocation = locations.minOf { it }
    val answer1 = lowestLocation

    println("Part #1 answer is %d".format(answer1))

    // Part2

    // FIXME WIP = headache for now ;)
    //  To be continued
    /*
    val reverseCategories : MutableMap<String, Category> = mutableMapOf()

    val seedRanges : List<SimpleRange> = mutableListOf()
    while (seeds.isNotEmpty()) {
        seedRanges.addLast(SimpleRange(seeds.removeFirst(), seeds.removeFirst()))
    }

    val s1 = categories["seed-to-soil"]!!.mapRange()

    val locationRanges = seedRanges
        .map { categories["seed-to-soil"]!!.mapRange(it) }
        .map { categories["soil-to-fertilizer"]!!.mapRange(it) }
        .map { categories["fertilizer-to-water"]!!.mapRange(it) }
        .map { categories["water-to-light"]!!.mapRange(it) }
        .map { categories["light-to-temperature"]!!.mapRange(it) }
        .map { categories["temperature-to-humidity"]!!.mapRange(it) }
        .map { categories["humidity-to-location"]!!.mapRange(it) }
    for see


    val reverseSeedranges =
        categories["humidity-to-location"]
            .reverseMap { categories["humidity-to-location"]!!.map(it) }
            .reverseMap { categories["temperature-to-humidity"]!!.map(it) }

            .map { categories["seed-to-soil"]!!.map(it) }
            .map { categories["soil-to-fertilizer"]!!.map(it) }
            .map { categories["fertilizer-to-water"]!!.map(it) }
            .map { categories["water-to-light"]!!.map(it) }
            .map { categories["light-to-temperature"]!!.map(it) }


            .reverseMap()

    val answer2 = 0

    println("Part #2 answer is %d".format(answer2))
    */

}

data class Category(var id: String, var idFrom: String, var idTo: String, val ranges : MutableList<ValueRange>) {
    fun map(value: Long): Long {
        var result = value
        for (r in ranges) {
            if (value in r.source..r.source+r.length) {
                result = r.destination + (value - r.source)
                break
            }
        }
        return result
    }
    fun reverseMap(value: Long): Long {
        var result = value
        for (r in ranges) {
            if (value in r.destination..r.destination+r.length) {
                result = r.source + (value - r.source)
                break
            }
        }
        return result
    }
    fun mapRange(input: SimpleRange): Set<SimpleRange> {
        var results = mutableSetOf<SimpleRange>()
        for (r in ranges) {
            results.addAll(r.transpose(input))
        }
        //println("%s reverse map value %d to %d".format(id, value, result))
        return results
    }
}

data class SimpleRange(val from: Long, val to: Long)
data class ValueRange(val source: Long, val destination: Long, val length: Long) {
    fun transpose(value: Long): Long {
        var result = value
        if (value in source..source+length) {
            result = destination + (value - source)
        }
        return result
    }
    fun transpose(s: SimpleRange): Set<SimpleRange> {
        var results = mutableSetOf<SimpleRange>()
        if (s.from < source && s.to > source+length) {
            // overlapping all
            results.add(SimpleRange(transpose(s.from), transpose(source-1)))
            results.add(SimpleRange(transpose(source), transpose(source+length)))
            results.add(SimpleRange(transpose(source+length+1), transpose(s.to)))
        } else if (s.from < source && s.to in source..source+length) {
            // overlapping left
            results.add(SimpleRange(transpose(s.from), transpose(source-1)))
            results.add(SimpleRange(transpose(source), transpose(s.to)))
        } else if (s.from in source..source+length && s.to in source..source+length) {
            // included
            results.add(SimpleRange(transpose(s.from), transpose(s.to)))
        } else if (s.from in source..source+length && s.to > source+length) {
            // overlapping right
            results.add(SimpleRange(transpose(s.from), transpose(source+length)))
            results.add(SimpleRange(transpose(source+length+1), transpose(s.to)))
        } else {
            // totally before or totally after
            results.add(s)
        }
        return results
    }
}