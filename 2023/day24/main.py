import os
import sympy as sym


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    # List of the hailstones, [(x, y, z), (u, v, w)]
    # x, y and z are the position, u, v, w are the velocities in the respective
    # directions
    hail: list[tuple[list[int], list[int]]] = []

    for line in array:
        # Parse each hailstone
        point, speed = line.split(" @ ")
        point = list(map(int, point.split(", ")))
        speed = list(map(int, speed.split(", ")))
        hail.append((point, speed))

    result = 0

    # The position of the hailstone (x, y) can be written in terms of time (t),
    # the initial position (x0, y0) and the velocities (u, v):
    # x = x0 + ut, y = y0 + vt
    # For two hailstones to intersect, we obtain the following simultaneous equations:
    # x1 + u1*t1 = x2 + u2*t2
    # y1 + v1*t1 = y2 + v2*t2
    # This can be rearranged to obtain t1:
    #
    # v2(x1 - x2) - u2(y1 - y2)
    # -------------------------
    #        u2v1 - u1v2

    # Loop through each pair of hailstones
    for i in range(len(hail)):
        hail1 = hail[i]

        for j in range(i + 1, len(hail)):
            hail2 = hail[j]

            # Ignore the z coordinates and velocities
            ((x1, y1, _), (u1, v1, _)) = hail1
            ((x2, y2, _), (u2, v2, _)) = hail2

            # If the two hailstones are moving at the same speed, then there
            # is no solution. This check prevents dividing by 0
            if u1 * v2 == u2 * v1:
                continue

            # Solve for t1 according to the equation above
            t1 = (v2 * (x1 - x2) - u2 * (y1 - y2)) / (u2 * v1 - u1 * v2)

            # Find the other values
            x = x1 + t1 * u1
            y = y1 + t1 * v1
            t2 = (x - x2) / u2

            # Ignore the solution if either hailstone crossed in the past
            if t1 < 0 or t2 < 0:
                continue

            # Increment the result if the cross point is within the test area
            if 2e14 <= x <= 4e14 and 2e14 <= y <= 4e14:
                result += 1

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    hail: list[tuple[list[int], list[int]]] = []

    # There are 6 unknown variables for the rock: [(x, y, z), (u, v, w)]
    # Each hailstone we consider introduces one new unknown variable: the time
    # when the stone hits the hailstone. Each hailstone provides three equations;
    # (xn, yn, zn) of the point of intersection. Therefore, we only need to consider
    # 3 hailstones to obtain 9 equations with 9 unknown variables that can be
    # solved simultaneously by finding the point of intersection:
    # x + u * t1 = x1 + u1 * t1
    # x + u * t2 = x2 + u2 * t2
    # x + u * t3 = x3 + u3 * t3
    # y + v * t1 = y1 + v1 * t1
    # z + w * t1 = z1 + w1 * t1
    # ...

    # This time, we only need three hailstones
    for line in array[:3]:
        point, speed = line.split(" @ ")
        point = list(map(int, point.split(", ")))
        speed = list(map(int, speed.split(", ")))
        hail.append((point, speed))

    # Obtain the position and velocity values from the hailstones
    ((x1, y1, z1), (u1, v1, w1)) = hail[0]
    ((x2, y2, z2), (u2, v2, w2)) = hail[1]
    ((x3, y3, z3), (u3, v3, w3)) = hail[2]

    # Use sympy to solve the equations simultaneously
    x, y, z, u, v, w, t1, t2, t3 = sym.symbols("x,y,z,u,v,w,t1,t2,t3")

    eq1 = sym.Eq(x + u * t1, x1 + u1 * t1)
    eq2 = sym.Eq(y + v * t1, y1 + v1 * t1)
    eq3 = sym.Eq(z + w * t1, z1 + w1 * t1)
    eq4 = sym.Eq(x + u * t2, x2 + u2 * t2)
    eq6 = sym.Eq(y + v * t2, y2 + v2 * t2)
    eq8 = sym.Eq(z + w * t2, z2 + w2 * t2)
    eq5 = sym.Eq(x + u * t3, x3 + u3 * t3)
    eq7 = sym.Eq(y + v * t3, y3 + v3 * t3)
    eq9 = sym.Eq(z + w * t3, z3 + w3 * t3)

    solution = sym.solve(
        [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9], (x, y, z, u, v, w, t1, t2, t3)
    )

    # The first three values in `solution[0]` will be x, y and z, therefore add them
    result = sum(solution[0][:3])

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
