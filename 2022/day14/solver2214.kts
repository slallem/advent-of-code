
import java.io.File
import java.lang.RuntimeException

println("2022 --- Day 14: Regolith Reservoir ---")

solve("./example1.txt")
solve("./input.txt")

fun solve(filename: String) {

    println("Solving file %s".format(filename))

    // Prepare terrain (rocks)

    var board : MutableMap<Int, Char> = mutableMapOf()
    val lines = File(filename).readLines().filter { it.isNotBlank() }
    var lastRockY = 0
    lines.forEach {  line ->
        // Decode key rocks
        val groups = line.split("->").map { s: String -> s.trim() }
        val dots: List<Pos> = groups.map { s: String ->
            val parts = s.split(",")
            Pos(parts[0].toInt(), parts[1].toInt())
        }.toList()
        // Deduct rock lines + compute "bottom"
        for (i in 0..dots.size-2) {
            val y1 = Math.min(dots[i].y, dots[i+1].y)
            val y2 = Math.max(dots[i].y, dots[i+1].y)
            val x1 = Math.min(dots[i].x, dots[i+1].x)
            val x2 = Math.max(dots[i].x, dots[i+1].x)
            for (y in y1..y2) {
                for (x in x1..x2) {
                    board[Pos(x, y).getId()] = '#'
                    if (y > lastRockY) lastRockY = y
                }
            }
        }
    }

    // Go sand !

    var rest = 0
    var sand = Pos(500,0)
    // move sand unit until one of them reaches the 'infinite' bottom end
    while (sand.y <= lastRockY) {
        if (!board.containsKey(Pos(sand.x, sand.y + 1).getId())) {
            sand.y++
        } else if (!board.containsKey(Pos(sand.x - 1, sand.y + 1).getId())) {
            sand.x--
            sand.y++
        } else if (!board.containsKey(Pos(sand.x + 1, sand.y + 1).getId())) {
            sand.x++
            sand.y++
        } else {
            // Sand unit cannot move further
            board[sand.getId()] = 'o' // rest
            rest++
            // launch another sand unit
            sand = Pos(500, 0)
        }
    }

    val answer1 = rest
    println("Part #1 answer is %d".format(answer1))

    // --- Part 2 ---

    // Clear sand of part 1 (only keep rocks)
    board = board.filter { entry -> entry.value == '#'}.toMutableMap()

    // Go sand !

    rest = 0
    sand = Pos(500,0)
    // move sand unit until it rests and stack up to the sand insertion point
    while (!board.containsKey(Pos(500,0).getId())) {
        if (!board.containsKey(Pos(sand.x, sand.y + 1).getId())) {
            sand.y++
        } else if (!board.containsKey(Pos(sand.x - 1, sand.y + 1).getId())) {
            sand.x--
            sand.y++
        } else if (!board.containsKey(Pos(sand.x + 1, sand.y + 1).getId())) {
            sand.x++
            sand.y++
        } else {
            // Sand unit cannot move further
            board[sand.getId()] = 'o' // rest
            rest++
            // launch another sand unit
            sand = Pos(500, 0)
        }
        if (sand.y > lastRockY) {
            // Bottom reached (last+1, as floor is last+2)
            board[sand.getId()] = 'o' // rest
            rest++
            // launch another sand unit
            sand = Pos(500, 0)
        }
    }

    val answer2 = rest
    println("Part #2 answer is %d".format(answer2))
    println()
}

// --- Utility classes ---

class Pos(var x: Int, var y: Int) {
    fun getId() : Int = y * 10000 + x
}
