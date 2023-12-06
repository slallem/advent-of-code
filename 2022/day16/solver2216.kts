
import java.io.File
import java.lang.RuntimeException

println("2022 --- Day 16: Proboscidea Volcanium ---")

// TODO a revoir en utilisant les graphes

solve("./example1.txt")
//solve("./input.txt")

fun solve(filename: String) {

    println("Solving file %s".format(filename))

    // Decode sensor data

    val valves: MutableMap<String, Valve> = mutableMapOf()
    val lines = File(filename).readLines().filter { it.isNotBlank() }
    lines.forEach { line ->
        val pattern = "Valve ([A-Z]+) has flow rate=([-0-9]+); tunnel[s]? lead[s]? to valve[s]? (.+)$"
        val match = Regex(pattern).find(line)!!
        val (valveId, flowRate, leadTo) = match.destructured
        val leads = leadTo.split(",").map { s: String -> s.trim() }.toMutableList()
        val valve = Valve(valveId, false, flowRate.toInt(), leads)
        valves[valve.id] = valve
    }

    // Starting situation
    val startingSituation = Situation(0, valves, "AA",0)

    var answer1 = 0
    val besties : MutableMap<String,Int> = mutableMapOf()
    startingSituation.explore(besties) {
        if (it.pressure > answer1) {
            answer1 = it.pressure
            println("Final pressure: %d".format(it.pressure))
        }
    }

    // display
    //valves.forEach { valve: Valve -> println(valve.toString()) }

    //


    println("Part #1 answer is %d".format(answer1))

    // --- Part 2 ---


    val answer2 = 0
    println("Part #2 answer is %d".format(answer2))
    
    println()
}

// --- Utility classes ---

data class Valve(val id: String, var opened: Boolean, val flowRate: Int, val leadsTo: MutableList<String>) {
    override fun toString(): String {
        return "Valve %s : flowrate %d leads to %s".format(id, flowRate, leadsTo.toString())
    }
}

class Situation(var minutes: Int, val valves: Map<String,Valve>, var position: String, var pressure: Int) {
    var minutesAllOpen : Int = 0
    fun explore(besties: Map<String,Int>, endCallback: (finalSituation: Situation) -> Unit) = explore("", besties, endCallback)
    fun explore(comingFrom: String, besties: Map<String,Int>, endCallback: (finalSituation: Situation) -> Unit) {
        // Time goes by
        minutes++
        // Computes added pressure (if any)
        pressure += valves.values.filter { it.opened }.sumOf { it.flowRate }
        if (isAllOpened()) {
            // No need to move anymore as all valves are opened
            minutesAllOpen = minutes
            while (minutes < 30) {
                minutes++
                // Computes added pressure (if any)
                pressure += valves.values.filter { it.opened }.sumOf { it.flowRate }
            }
        }
        // Stop or continue exploration
        if (minutes == 30) {
            // Final situation
            endCallback(this)
        } else {
            // Explore possible options from here (open valve and/or move to other tunnels)
            if (!getCurrentValve().opened) {
                // Explore closing valve
                val s2 = clone()
                s2.getCurrentValve().opened = true
                s2.explore(position, besties, endCallback)
            }
            for (valveId in getCurrentValve().leadsTo) {
                val s3 = clone()
                s3.position = valveId
                s3.explore(position, besties, endCallback)
            }
        }
    }
    fun getCurrentValve() : Valve = valves[position]!!
    fun clone() : Situation {
        return Situation(minutes, valves.mapValues { it.value.copy() }.toMap(), position, pressure)
    }
    fun getOpenTag() = valves.filterValues { it.opened }.toList().joinToString { "" }
    fun isAllOpened() = valves.filterValues { !it.opened }.toList().isEmpty()
    fun getMinutesAllOpen() = minutesAllOpen
}
