import heapq
import os


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    # Parse the puzzle input as a list of bricks
    # Each brick is a list of two tuples (x, y, z), the start and end point
    bricks = [
        [tuple(map(int, brick.split(","))) for brick in line.split("~")]
        for line in array
    ]

    # Sort each individual brick according to the z-coordinate, so the first point
    # is below or level with the second point
    for brick in bricks:
        brick.sort(key=lambda x: x[2])

    # Sort the whole list of bricks so the lowest brick is first
    bricks.sort(key=lambda x: x[0][2])

    def valid(
        brick: list[tuple[int, ...]], coordinates: dict[tuple[int, int, int], int]
    ) -> list[tuple[int, ...]] | None:
        """
        Function which returns True if the brick can move one space down, otherwise
        return False.
        """

        # Move the brick one space downwards
        new_brick = [
            (brick[0][0], brick[0][1], brick[0][2] - 1),
            (brick[1][0], brick[1][1], brick[1][2] - 1),
        ]

        # Loop through every point in the brick
        for x in range(new_brick[0][0], new_brick[1][0] + 1):
            for y in range(new_brick[0][1], new_brick[1][1] + 1):
                for z in range(new_brick[0][2], new_brick[1][2] + 1):
                    # If the point is in the coordinates dict, then the space
                    # is occupied
                    if (x, y, z) in coordinates:
                        return None

        # The brick is valid, therefore return it
        return new_brick

    # A dict where the key is the coordinate and the value is the ID of the brick
    # in that space
    coordinates: dict[tuple[int, int, int], int] = {}

    # A dict where the key is the brick ID, and the value is a list of the coordinates
    # in the brick
    shapes: dict[int, list[tuple[int, int, int]]] = {}

    # Having two dicts means that a coordinate can be mapped to a shape, and a shape
    # can me mapped to a list of coordinates for that brick

    # Loop through each brick
    for i, brick in enumerate(bricks):
        start, end = brick
        z = start[2]

        # Attempt to move the shape down one space at a time, as long as the
        # space below is free, and we are not at the ground (z = 1)
        while z > 1 and (new_brick := valid(brick, coordinates)):
            brick = new_brick
            bricks[i] = brick
            z -= 1

        start, end = brick

        # Once the shape cannot move down any more, it has now settled since the
        # list of bricks is sorted by height.
        for x in range(start[0], end[0] + 1):
            for y in range(start[1], end[1] + 1):
                for z in range(start[2], end[2] + 1):
                    # Add the brick ID to the coordinates dict
                    coordinates[(x, y, z)] = i

                    # Also add the coordinate to the shapes dict
                    shapes[i] = shapes.get(i, [])
                    shapes[i].append((x, y, z))

    def connected(
        main: int,
        check: int,
        coordinates: dict[tuple[int, int, int], int],
        shapes: dict[int, list[tuple[int, int, int]]],
    ) -> bool:
        """
        Function that returns True if a brick (check) is connected to another
        brick below, which is not `main`, otherwise return False.
        """

        for x, y, z in shapes[check]:
            point = (x, y, z - 1)

            if (
                point in coordinates
                and point not in shapes[main]
                and point not in shapes[check]
            ):
                return True

        return False

    result = 0

    # Loop through each brick again
    for i, points in shapes.items():
        # Set of shapes that are adjacent (above) this current shape
        adjacent_shapes: set[int] = set()

        # Loop through each coordinate in the brick
        for x, y, z in points:
            # Coordinates of the space above
            above = (x, y, z + 1)

            # If the space above is occupied by a shape, and it is not this
            # shape, then there must be another shape above
            if above in coordinates and above not in shapes[i]:
                adjacent_shapes.add(coordinates[above])

        # If the brick can be safely disintegrated, then all adjacent bricks must
        # be connected to at least one other brick
        for shape in adjacent_shapes:
            # If we find an adjacent brick that is not connected to any other bricks,
            # then it is not safe to remove, therefore break
            if not connected(i, shape, coordinates, shapes):
                break
        else:
            # If we reach here, it is safe to remove this brick, therefore add
            # to the result
            result += 1

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    bricks = [
        [tuple(map(int, brick.split(","))) for brick in line.split("~")]
        for line in array
    ]

    for brick in bricks:
        brick.sort(key=lambda x: x[2])

    bricks.sort(key=lambda x: x[0][2])

    def valid(
        brick: list[tuple[int, ...]], coordinates: dict[tuple[int, int, int], int]
    ) -> list[tuple[int, ...]] | None:
        new_brick = [
            (brick[0][0], brick[0][1], brick[0][2] - 1),
            (brick[1][0], brick[1][1], brick[1][2] - 1),
        ]

        for x in range(new_brick[0][0], new_brick[1][0] + 1):
            for y in range(new_brick[0][1], new_brick[1][1] + 1):
                for z in range(new_brick[0][2], new_brick[1][2] + 1):
                    if (x, y, z) in coordinates:
                        return None

        return new_brick

    coordinates: dict[tuple[int, int, int], int] = {}
    shapes: dict[int, list[tuple[int, int, int]]] = {}

    for i, brick in enumerate(bricks):
        start, end = brick
        z = start[2]

        while z > 1 and (new_brick := valid(brick, coordinates)):
            brick = new_brick
            bricks[i] = brick
            z -= 1

        start, end = brick

        for x in range(start[0], end[0] + 1):
            for y in range(start[1], end[1] + 1):
                for z in range(start[2], end[2] + 1):
                    coordinates[(x, y, z)] = i

                    shapes[i] = shapes.get(i, [])
                    shapes[i].append((x, y, z))

    # Dict where the key is the brick ID, and the value is a set of bricks
    # that are below
    below_shapes: dict[int, set[int]] = {}

    # The same as `below_shapes`, but contains the bricks that are above.
    above_shapes: dict[int, set[int]] = {}

    # Loop through all the bricks to populate the above and below bricks
    for i, points in shapes.items():
        above_shapes[i] = set()
        below_shapes[i] = set()

        for x, y, z in points:
            below = (x, y, z - 1)

            # Check if the space below belongs to a brick which is not this brick
            if below in coordinates and below not in shapes[i]:
                below_shape = coordinates[below]

                below_shapes[i].add(below_shape)
                above_shapes[below_shape].add(i)

    result = 0

    # Loop through each brick to see how many other bricks will fall if this
    # brick removed
    for i, points in shapes.items():
        # Start iterating with the bricks above the current brick
        queue = list(above_shapes[i])
        seen = set()
        fallen = {i}

        while queue:
            # Need to use a heap, so that the brick with the lowest ID (and
            # therefore the lowest z-coordinate) is picked first
            shape = heapq.heappop(queue)

            # Get the bricks below this brick
            below = below_shapes[shape]

            # This brick will only fall if every brick below it has also fallen
            if all(brick in fallen for brick in below):
                # If True, then this brick will also fall
                fallen.add(shape)

                # Add all bricks above this brick to the heap, to check whether
                # they also will fall
                for brick in above_shapes[shape]:
                    if brick not in seen:
                        seen.add(brick)
                        heapq.heappush(queue, brick)

        # Add the total number of fallen bricks to the final result, exlcuding
        # the disintegrated brick itself
        result += len(fallen) - 1

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
