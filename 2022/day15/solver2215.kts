
import java.io.File
import java.lang.RuntimeException

println("2022 --- Day 15: Beacon Exclusion Zone ---")

solve("./example1.txt", 10, 0, 20)
solve("./input.txt", 2000000, 0,4000000)

fun solve(filename: String, givenRow: Int, part2from: Int, part2to: Int) {

    println("Solving file %s".format(filename))

    // Decode sensor data

    val sensors: MutableList<Sensor> = mutableListOf()
    val lines = File(filename).readLines().filter { it.isNotBlank() }
    lines.forEach { line ->
        val match = Regex("Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)").find(line)!!
        val (sx, sy, nbx, nby) = match.destructured
        sensors.addLast(Sensor(Pos(sx.toInt(),sy.toInt()), Pos(nbx.toInt(), nby.toInt())))
    }

    sensors.sortBy { sensor -> sensor.minReachableX() }
    val minX = sensors.first().minReachableX()
    sensors.sortBy { sensor -> sensor.maxReachableX() }
    val maxX = sensors.last().maxReachableX()

    val impossibilities: MutableSet<Int> = mutableSetOf()
    for (x in minX..maxX) {
        for (sensor in sensors) {
            if (Pos(x, givenRow).manhattanDistanceTo(sensor.pos) <= sensor.distanceToNearestBeacon()) {
                impossibilities.add(x)
            }
        }
    }

    // Remove known beacons from list
    sensors.forEach { sensor ->
        if (sensor.nearestBeacon.y == givenRow && impossibilities.contains(sensor.nearestBeacon.x)) {
            impossibilities.remove(sensor.nearestBeacon.x)
        }
    }

    val answer1 = impossibilities.size
    println("Part #1 answer is %d".format(answer1))

    // --- Part 2 ---

    var answer2 : Long = 0
    loop1@ for (sensor in sensors) {
        val candidates : MutableMap<String, Pos> = mutableMapOf()
        visitManhattanBorders(sensor.pos, sensor.distanceToNearestBeacon()+1) { x, y ->
            if (x in part2from..part2to && y in part2from..part2to) {
                val p = Pos(x,y)
                candidates[p.getUid()] = p
            }
        }
        for (ptEval in candidates.values) {
            var found = true
            loop2@ for (sensor2 in sensors) {
                if (ptEval.manhattanDistanceTo(sensor2.pos) <= sensor2.distanceToNearestBeacon()) {
                    // covered by a sensor
                    found = false
                    break@loop2
                }
            }
            if (found) {
                // Found !
                println("Found coordinates %d,%d".format(ptEval.x, ptEval.y))
                answer2 = (ptEval.x * 4000000L) + ptEval.y
            }
        }
        if (answer2 > 0) {
            break@loop1
        }
    }

    println("Part #2 answer is %d".format(answer2))
    
    println()
}

// --- Utility classes ---

fun visitAllManhattanDistances(p: Pos, distance: Int, callback: (vx: Int, vy: Int) -> Unit) {
    for (x in -distance..distance) { // max distance to visit on X (+/- Manhattan distance)
        val rd = distance - Math.abs(x) // remaining distance to visit on Y
        for (y in -rd .. rd) {
            callback(p.x + x, p.y + y)
        }
    }
}

fun visitManhattanBorders(p: Pos, distance: Int, callback: (vx: Int, vy: Int) -> Unit) {
    for (x in -distance..distance) { // max distance to visit on X (+/- Manhattan distance)
        val rd = distance - Math.abs(x) // remaining distance to visit on Y
        callback(p.x + x, p.y - rd)
        if (rd!=0) callback(p.x + x, p.y + rd)
    }
}

class Pos(var x: Int, var y: Int) {
    fun getUid() : String = "%d,%d".format(x,y)
    fun manhattanDistanceTo(another: Pos) : Int {
        return Math.abs(x - another.x) + Math.abs(y - another.y)
    }
}

class Sensor(val pos: Pos, val nearestBeacon: Pos) {
    fun distanceToNearestBeacon() : Int = pos.manhattanDistanceTo(nearestBeacon)
    fun minReachableX() : Int = pos.x - distanceToNearestBeacon()
    fun maxReachableX() : Int = pos.x + distanceToNearestBeacon()

}