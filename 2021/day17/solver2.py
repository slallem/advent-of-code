
# 2021 Day 17 part 2

# My puzzle
#target area: x=128..160, y=-142..-88
x_bounds = [128, 160]
y_bounds = [-142, -88]

# Example
#x_bounds = [20, 30]
#y_bounds = [-10, -5]

maxx = max(x_bounds)
miny = min(y_bounds)


def shoot(x, y):
    velx = x
    vely = y
    # The probe's x,y position starts at 0,0.
    px = 0
    py = 0
    y_max = 0
    while True:
        # ----- Advance by one step
        # The probe's x position increases by its x velocity.
        px += velx
        # The probe's y position increases by its y velocity.
        py += vely
        # Due to drag, the probe's x velocity changes by 1 toward the value 0;
        # that is, it decreases by 1 if it is greater than 0,
        # increases by 1 if it is less than 0, or does not change if it is already 0.
        if velx > 0:
            velx -= 1
        elif velx < 0:
            velx += 1
        # Due to gravity, the probe's y velocity decreases by 1.
        vely -= 1
        # ---- Debug trace
        #print(f"step x {px} y {py} ; velocity x {velx} y {vely} -- miny {miny}")
        # ---- Update ymax
        if py > y_max:
            y_max = py
        # ---- Target hit test & exit conditions:
        if py < miny and vely <= 0:  # Beyond maximum target y and no possible way to get up (no need to look further)
            return y_max, False
        elif x_bounds[0] <= px <= x_bounds[1] and y_bounds[0] <= py <= y_bounds[1]:  # Target reached (boom!)
            return y_max, True
        #-- TRICKY!
        #-- Velocity 0,0 is not a good stop condition
        #-- because non moving "bullet" can still fall on target due to gravity !!!
        #elif velx == 0 and vely == 0:  # No more velocity (splash!)
        #    return y_max, False


#print(shoot(6, 6))

counter = 0
for yv in range(miny-1, abs(miny)+1):
    for xv in range(-maxx-1, maxx+1):
        top, match = shoot(xv, yv)
        #print(f"testing {xv} {yv} = {top} {match}")
        if match:
            counter += 1
            #print(f"{xv},{yv}")
print(counter)
