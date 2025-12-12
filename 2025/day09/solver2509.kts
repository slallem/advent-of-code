import java.io.File

data class Point(val x: Long, val y: Long)
data class LineSegment(val p1: Point, val p2: Point)
data class Rectangle(val p1: Point, val p2: Point) {
    val area: Long
        get() {
            val width = kotlin.math.abs(p2.x - p1.x) + 1L
            val height = kotlin.math.abs(p2.y - p1.y) + 1L
            return width * height
        }
}


fun solve(filename: String) {
    println("=== Solving $filename ===")
    
    val inputFile = File(filename)
    val points = inputFile.readLines()
        .map { line ->
            val (x, y) = line.split(",").map { it.toLong() }
            Point(x, y)
        }

    // Part One
    var maxArea = 0L
    for (i in points.indices) {
        for (j in i + 1 until points.size) {
            val rectangle = Rectangle(points[i], points[j])
            if (rectangle.area > maxArea) {
                maxArea = rectangle.area
            }
        }
    }

    val result = maxArea
    println("Part #1 - largest area is: $result")

    // Part 2 - Find largest rectangle contained within polygon

    // Step 1: Build polygon from horizontal and vertical segments
    // Calculate segments from ALL combinations of 2 points (as user requested)
    val horizontalSegments = mutableListOf<LineSegment>()
    val verticalSegments = mutableListOf<LineSegment>()
    
    for (i in points.indices) {
        for (j in i + 1 until points.size) {
            val p1 = points[i]
            val p2 = points[j]
            
            if (p1.x == p2.x) {
                // Vertical segment (same x-coordinate)
                verticalSegments.add(LineSegment(p1, p2))
            } else if (p1.y == p2.y) {
                // Horizontal segment (same y-coordinate)
                horizontalSegments.add(LineSegment(p1, p2))
            }
            // Ignore diagonal segments (different x and y)
        }
    }
    
    val allPolygonSegments = horizontalSegments + verticalSegments

    /*if (filename.contains("example")) {
        println("Points: $points")
        println("Horizontal segments: ${horizontalSegments.size}")
        println("Vertical segments: ${verticalSegments.size}")
        println("Total polygon segments: ${allPolygonSegments.size}")
        for (seg in allPolygonSegments) {
            println("  Segment: ${seg.p1} -> ${seg.p2}")
        }
    }*/


    // Step 2: For each rectangle, check validity by ensuring it doesn't cross any segments
    fun isValidRectangle(p1: Point, p2: Point): Boolean {
        val x1 = minOf(p1.x, p2.x)
        val x2 = maxOf(p1.x, p2.x)
        val y1 = minOf(p1.y, p2.y)
        val y2 = maxOf(p1.y, p2.y)
        
        if (x1 >= x2 || y1 >= y2) return false
        
        // Check if any polygon segment passes through the rectangle interior
        for (segment in allPolygonSegments) {
            val sp1 = segment.p1
            val sp2 = segment.p2
            
            // For horizontal segments
            if (sp1.y == sp2.y) {
                val y = sp1.y
                val segX1 = minOf(sp1.x, sp2.x)
                val segX2 = maxOf(sp1.x, sp2.x)
                
                // Check if horizontal segment crosses through rectangle interior
                if (y > y1 && y < y2 && segX2 > x1 && segX1 < x2) {
                    return false
                }
            }
            
            // For vertical segments  
            if (sp1.x == sp2.x) {
                val x = sp1.x
                val segY1 = minOf(sp1.y, sp2.y)
                val segY2 = maxOf(sp1.y, sp2.y)
                
                // Check if vertical segment crosses through rectangle interior
                if (x > x1 && x < x2 && segY2 > y1 && segY1 < y2) {
                    return false
                }
            }
        }
        
        return true
    }


    // Parse all combinations and check that rectangles are valid
    var maxValidArea = 0L
    var validCount = 0

    for (i in points.indices) {
        for (j in i + 1 until points.size) {
            val p1 = points[i]
            val p2 = points[j]
            
            if (isValidRectangle(p1, p2)) {
                validCount++
                val width = kotlin.math.abs(p2.x - p1.x) + 1
                val height = kotlin.math.abs(p2.y - p1.y) + 1
                val area = width * height
                
                
                if (area > maxValidArea) {
                    maxValidArea = area
                }
            }
        }
    }

    val result2 = maxValidArea
    println("Part #2 - largest valid area is: $result2")
    println()
}

// Solve with example first, then with real input
solve("./example.txt")
solve("./input.txt")