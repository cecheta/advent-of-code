from collections import deque


def part_one(input: str):
    shape: set[tuple[int, int, int]] = set()

    surface_area = 0

    # Iterate through the cubes in lava droplet
    for line in input.splitlines():
        # Add the surface area of the current cube
        surface_area += 6

        x, y, z = map(int, line.split(','))

        # Check the six directions adjacent to the current cube
        for a, b, c in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            X, Y, Z = x + a, y + b, z + c

            # If an adjacent space already has a cube, then two cubes are
            # touching, therefore subtract the two touching faces
            if (X, Y, Z) in shape:
                surface_area -= 2

        # Keep track of the cubes we have seen so far
        shape.add((x, y, z))

    print(surface_area)


def part_two(input: str):
    shape: set[tuple[int, int, int]] = set()

    # Find the minumum and maximum coordinates of the cubes in the lava droplet
    # Initialise the values to very large/small numbers
    min_x = min_y = min_z = 10000
    max_x = max_y = max_z = -10000

    # Iterate through the cubes in the lava droplet
    for line in input.splitlines():
        x, y, z = map(int, line.split(','))

        # Find the outer boundaries
        min_x = min(min_x, x - 1)
        min_y = min(min_y, y - 1)
        min_z = min(min_z, z - 1)
        max_x = max(max_x, x + 1)
        max_y = max(max_y, y + 1)
        max_z = max(max_z, z + 1)

        # Keep track of all the cubes
        shape.add((x, y, z))

    surface_area = 0

    start = (min_x, min_y, min_z)

    queue = deque([start])

    seen = {start}

    # BFS to iterate through all cubes outside of the lava droplet
    while queue:
        x, y, z = queue.popleft()

        # Check the six directions adjacent to the current cube
        for a, b, c in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            X, Y, Z = x + a, y + b, z + c

            # If the adjacent space is within range...
            if min_x <= X <= max_x and min_y <= Y <= max_y and min_z <= Z <= max_z:
                # ...and is within the lava droplet, then increase the surface
                # area by one
                if (X, Y, Z) in shape:
                    surface_area += 1
                # Otherwise, if the adjacent space has not been seen before,
                # add it to the queue to visit later
                elif (X, Y, Z) not in seen:
                    seen.add((X, Y, Z))
                    queue.append((X, Y, Z))

    print(surface_area)


with open('input.txt') as f:
    input = f.read()


part_one(input)
part_two(input)
