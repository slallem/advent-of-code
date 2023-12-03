
import java.io.File
import kotlin.collections.first
import kotlin.text.substring
import kotlin.text.toCharArray

//var lines = File("./example1.txt").readLines()
var lines = File("./input.txt").readLines()

var total1 = 0
var total2 = 0

var values: List<Value> = mutableListOf()

for (yy in 0..lines.size-1) {
    var v: Value? = null
    for (xx in 0..lines[yy].length-1) {
        val c = lines[yy][xx]
        if (c in '0'..'9') {
            if (v==null) {
                v = Value(xx, xx, yy, yy, "")
                values.addLast(v)
            }
            v!!.addDigit(c, xx, yy)
        } else {
            v = null
        }
    }
}

for (yy in 0..lines.size-1) {
    for (xx in 0..lines[yy].length-1) {
        if (isSpecialChar(lines[yy][xx])) {
            for (v in values) {
                if (v.isAdjacent(xx, yy)) {
                    total1 += v.value.toInt()
                }
            }
        }
    }
}

for (yy in 0..lines.size-1) {
    for (xx in 0..lines[yy].length-1) {
        if (isSpecialChar(lines[yy][xx])) {
            var current = 1
            var nbAdj = 0
            for (v in values) {
                if (v.isAdjacent(xx, yy)) {
                    nbAdj++
                    current *= v.value.toInt()
                }
            }
            if (nbAdj == 2) {
                total2 += current
            }
        }
    }
}

println("Part #1 total is %d".format(total1))
println("Part #2 total is %d".format(total2))

data class Value(var minx: Int,
                 var maxx: Int,
                 var miny: Int,
                 var maxy: Int,
                 var value: String) {

    fun addDigit(c: Char, x: Int, y: Int) {
        value += c.toString()
        miny = y
        maxy = y
        if (x<minx) minx = x
        if (x>maxx) maxx = x
        if (y<miny) miny = y
        if (y>maxy) maxy = y
    }
    fun isAdjacent(x: Int, y: Int) : Boolean {
        return (x>=minx-1 && y>=miny-1 && x<=maxx+1 && y<= maxy+1)
    }
}

fun isSpecialChar(c: Char) : Boolean {
    return !".0123456789".contains(c)
}
