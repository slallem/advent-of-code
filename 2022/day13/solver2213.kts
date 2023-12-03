
import java.io.File
import java.lang.RuntimeException

println("2022 Day 13")

var total1 = 0

//var lines = File("./example1.txt").readLines()
var lines = File("./input.txt").readLines()
lines = lines.filter { it.isNotBlank() }
val lines2 = lines.toList()

// --- Part 1 ---

var idx = 0
while (lines.size > 0) {
    idx++
    val a = Packet.ofString(lines.removeFirst())
    val b = Packet.ofString(lines.removeFirst())
//    println(a.toString())
//    println(b.toString())
//    println(a.compareTo(b))
//    println()
    if (a.compareTo(b) < 0) {
        total1 += idx
    }
}

println("Part #1 total is %d".format(total1))

// --- Part 2 ---

val divider1 = Packet.ofString("[[2]]")
val divider2 = Packet.ofString("[[6]]")
//val packets = lines.map { it to Packet.ofString(it) }.toMap()
val packets = lines2.map { Packet.ofString(it) }.toMutableList()
packets.addLast(divider1)
packets.addLast(divider2)

val comparator = Comparator { o1: Any, o2: Any ->
    return@Comparator Packet.compareValues(o1, o2)
}
packets.sortWith(comparator)

//for (packet in packets) {
//    println(packet.toString())
//}

var soluce2 = (packets.indexOf(divider1)+1) * (packets.indexOf(divider2)+1)
println("Part #2 decoder key is %d".format(soluce2))

// --- Utility classes ---
class Packet() {
    var items: List<Any> = mutableListOf()
    companion object {
        fun ofSingleInteger(i: Int): Packet {
            val c = Packet()
            c.addItem(i)
            return c
        }
        fun ofString(s: String) : Packet {
            //Example: [[5,[4,[8,3,4],1,1,[3,8,9,4,0]],4]]
            val sTmp = s.replace("10","A")
            var current: Packet? = null
            val stack: List<Packet> = mutableListOf()
            for (c in sTmp.toCharArray()) {
                when(c) {
                    '[' -> {
                        val newComp = Packet()
                        current?.addItem(newComp)
                        stack.addLast(newComp)
                        current = newComp
                    }
                    ']' -> {
                        stack.removeLast()
                        if (stack.isNotEmpty()) current = stack.last()
                    }
                    '0','1','2','3','4','5','6','7','8','9','A' -> {
                        val v = if (c=='A') 10 else c.toString().toInt()
                        current!!.addItem(v)
                    }
                }
            }
            if (current==null) {
                throw RuntimeException("Malformed packet: %s".format(s))
            }
            return current
        }
        fun compareValues(v1: Any, v2: Any) : Int {
            if (v1 is Int && v2 is Int) {
                return v1 - v2
            } else if (v1 is Int && v2 is Packet) {
                return compareValues(ofSingleInteger(v1), v2)
            } else if (v1 is Packet && v2 is Int) {
                return compareValues(v1, ofSingleInteger(v2))
            } else if (v1 is Packet && v2 is Packet) {
                // both composite
                val commonSize = Math.min(v1.items.size, v2.items.size)
                for (i in 0..commonSize-1) {
                    val comp = compareValues(v1.getNthValue(i), v2.getNthValue(i))
                    if (comp!=0) {
                        return comp
                    }
                }
                return v1.items.size - v2.items.size
            }
            throw RuntimeException("Unexpected types")
        }

    }
    fun addItem(v: Any) {
        items.addLast(v)
    }
    override fun toString() : String {
        var s = "["
        for (item in items) {
            s += item.toString()
            s += ","
        }
        s += "]"
        return s
    }
    fun getNthValue(index: Int) : Any {
        return if (index<0 || index >= items.size) -1 else items[index]
    }
    fun compareTo(another: Packet) : Int {
        return compareValues(this, another)
    }
}