import java.io.File

data class Pos(val x: Int, val y: Int, val z: Int) {
    fun distanceTo(other: Pos): Double {
        val dx = (x - other.x).toDouble()
        val dy = (y - other.y).toDouble()
        val dz = (z - other.z).toDouble()
        return kotlin.math.sqrt(dx * dx + dy * dy + dz * dz)
    }
}

fun findClosestPos(target: Pos, positions: List<Pos>): Pos? {
    return positions.filter { it != target }.minByOrNull { target.distanceTo(it) }
}

class CircuitTracker {
    private val circuits = mutableMapOf<Pos, Int>()
    private var nextCircuitId = 0
    
    fun connectBoxes(pos1: Pos, pos2: Pos) {
        val circuit1 = circuits[pos1]
        val circuit2 = circuits[pos2]
        
        when {
            circuit1 == null && circuit2 == null -> {
                // Both boxes are new, create a new circuit
                circuits[pos1] = nextCircuitId
                circuits[pos2] = nextCircuitId
                nextCircuitId++
            }
            circuit1 != null && circuit2 == null -> {
                // pos1 is in a circuit, add pos2 to it
                circuits[pos2] = circuit1
            }
            circuit1 == null && circuit2 != null -> {
                // pos2 is in a circuit, add pos1 to it
                circuits[pos1] = circuit2
            }
            circuit1 != null && circuit2 != null && circuit1 != circuit2 -> {
                // Both are in different circuits, merge them
                val oldCircuitId = circuit2
                circuits.entries.filter { it.value == oldCircuitId }.forEach {
                    circuits[it.key] = circuit1
                }
            }
            // If circuit1 == circuit2, they're already connected, do nothing
        }
    }
    
    fun getCircuitSizes(): List<Int> {
        return circuits.values.groupingBy { it }.eachCount().values.toList()
    }
    
    fun getCircuitOf(pos: Pos): Int? = circuits[pos]
    
    fun getAllCircuits(): Map<Int, List<Pos>> {
        return circuits.entries.groupBy({ it.value }, { it.key })
    }
    
    fun displayAllCircuits() {
        val allCircuits = getAllCircuits()
        println("Total circuits: ${allCircuits.size}")
        allCircuits.entries.sortedBy { it.key }.forEach { (circuitId, positions) ->
            println("Circuit $circuitId (size ${positions.size}): $positions")
        }
    }
}

val inputFile = File("./input.txt")

val positions = inputFile.readLines()
    .map { line ->
        val (x, y, z) = line.split(",").map { it.toInt() }
        Pos(x, y, z)
    }

// Part One - Find closest connections and build circuits

val circuitTracker = CircuitTracker()

// Generate all possible pairs and sort by distance
val allPairs = mutableListOf<Pair<Pos, Pos>>()
for (i in positions.indices) {
    for (j in i + 1 until positions.size) {
        allPairs.add(positions[i] to positions[j])
    }
}

val sortedPairs = allPairs.sortedBy { (pos1, pos2) -> pos1.distanceTo(pos2) }

// Connect the 1000 shortest pairs (or all pairs if less than 1000)
val connectionsToMake = minOf(1000, sortedPairs.size)
repeat(connectionsToMake) { index ->
    val (pos1, pos2) = sortedPairs[index]
    circuitTracker.connectBoxes(pos1, pos2)
}

val circuitSizes = circuitTracker.getCircuitSizes().sortedDescending()
//circuitTracker.displayAllCircuits()

val result = if (circuitSizes.size >= 3) {
    circuitSizes[0] * circuitSizes[1] * circuitSizes[2]
} else {
    circuitSizes.fold(1) { acc, size -> acc * size }
}

println("Part #1 - Product of three largest circuits: $result")

// Part 2 - Continue connecting all pairs until fully connected

val circuitTracker2 = CircuitTracker()
var lastConnectedPair: Pair<Pos, Pos>? = null

// Connect all pairs in order of shortest distance
for ((pos1, pos2) in sortedPairs) {
    val circuit1 = circuitTracker2.getCircuitOf(pos1)
    val circuit2 = circuitTracker2.getCircuitOf(pos2)
    
    // Only connect if they're not already in the same circuit
    // If both are null (unconnected) or different circuit IDs, connect them
    val shouldConnect = when {
        circuit1 == null && circuit2 == null -> true  // Both unconnected
        circuit1 == null || circuit2 == null -> true  // One unconnected
        circuit1 != circuit2 -> true                   // Different circuits
        else -> false                                   // Same circuit
    }
    
    if (shouldConnect) {
        circuitTracker2.connectBoxes(pos1, pos2)
        lastConnectedPair = pos1 to pos2
    }
}

println("Part #2 - Last connected pair is $lastConnectedPair")
println("Part #2 - Product of X coordinates is ${lastConnectedPair!!.first.x * lastConnectedPair!!.second.x}")

