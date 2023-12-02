
import java.io.File

val maxByColor = mapOf("red" to  12, "green" to 13, "blue" to 14)

//var lines = File("./example1.txt").readLines()
var lines = File("./input.txt").readLines()

var total1 = 0
var total2 = 0

lines.forEach { line ->
    val split1 = line.split(":")
    val gameNo = split1[0].trim().split(" ")[1].toInt()
    val groups = split1[1].split(";")
    var isValid = true
    val colorCounts = mutableMapOf("red" to  0, "green" to 0, "blue" to 0)
    groups.forEach { groupe ->
        val couples = groupe.split(",")
        couples.forEach { couple ->
            val split3 = couple.trim().split(" ")
            val nb = split3[0].toInt()
            val color = split3[1].trim()
            if (nb > maxByColor.getOrDefault(color, 0)) {
                // mismatch
                isValid = false
            }
            if (nb > colorCounts.getOrDefault(color, 0)) {
                colorCounts[color] = nb
            }
        }
    }
    if (isValid) {
        total1 += gameNo
    }
    total2 += colorCounts.getOrDefault("red", 0) *
            colorCounts.getOrDefault("green", 0) *
            colorCounts.getOrDefault("blue", 0)
}

println("Part #1 total is %d".format(total1))
println("Part #2 total is %d".format(total2))
