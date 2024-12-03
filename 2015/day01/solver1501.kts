import java.io.File
import kotlin.system.exitProcess

// Part One
val input = File("./input.txt").readText()

println(input.count { it == '(' } - input.count { it == ')' })

// Part Two

var floor = 0
input.forEachIndexed { index, c ->
    when {
        c == '(' -> floor++
        c == ')' -> floor--
    }
    if (floor == -1) {
        println("Santa enters basement at index ${index+1}")
        exitProcess(0)
    }
}
exitProcess(1)