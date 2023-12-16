import os
from collections import deque


def part_one(puzzle_input: str) -> None:
    grid = puzzle_input.strip().splitlines()

    # Dict where the key is the vector of the direction we are travelling in, and
    # the value is the name of the direction
    directions: dict[tuple[int, int], str] = {
        (0, 1): "right",
        (0, -1): "left",
        (1, 0): "down",
        (-1, 0): "up",
    }

    # Dict to help determine the direction the light will travel in after hitting an
    # object. The key is the direction the beam is currently travelling in, and the
    # value is another dict where the key is the symbol of the object the beam hits,
    # and the value is a list of vectors that the beam is now travelling in. For
    # example, if the beam is travelling right, and hits "\", it will now be travelling
    # in the direction (1, 0), which is down.
    moves: dict[str, dict[str, list[tuple[int, int]]]] = {
        "right": {
            ".": [(0, 1)],
            "-": [(0, 1)],
            "|": [(-1, 0), (1, 0)],
            "/": [(-1, 0)],
            "\\": [(1, 0)],
        },
        "left": {
            ".": [(0, -1)],
            "-": [(0, -1)],
            "|": [(-1, 0), (1, 0)],
            "/": [(1, 0)],
            "\\": [(-1, 0)],
        },
        "down": {
            ".": [(1, 0)],
            "-": [(0, -1), (0, 1)],
            "|": [(1, 0)],
            "/": [(0, -1)],
            "\\": [(0, 1)],
        },
        "up": {
            ".": [(-1, 0)],
            "-": [(0, -1), (0, 1)],
            "|": [(-1, 0)],
            "/": [(0, 1)],
            "\\": [(0, -1)],
        },
    }

    # The starting point is in the top-left of the grid, travelling to the right
    start = (0, 0, "right")

    # Set of squares the beam has travelled through, including its direction
    visited: set[tuple[int, int, str]] = {start}

    # Set of coordinates the beam has travelled through
    energized: set[tuple[int, int]] = {(start[0], start[1])}

    # Queue which will be used to perform BFS through the grid
    # Optional: Use a deque to efficiently pop from the front of the queue
    queue: deque[tuple[int, int, str]] = deque([start])

    # Continue looping until the queue is empty
    while queue:
        x, y, dir = queue.popleft()

        # Get the character of the current square
        char = grid[x][y]

        # Get the direction(s) the beam will now be moving in
        new_moves = moves[dir][char]

        for move in new_moves:
            # Get the new coordinates of the beam after passing through the square
            new_x, new_y = x + move[0], y + move[1]
            new_dir = directions[move]
            point = (new_x, new_y, new_dir)

            # Check that the beam is within the grid, and we have not already
            # visited this square in the same direction
            if (
                0 <= new_x < len(grid)
                and 0 <= new_y < len(grid[0])
                and point not in visited
            ):
                # This square is now energized, therefore add it to the set
                energized.add((new_x, new_y))

                # Add the new point to the end of the queue, keeping track of
                # which squares we have visited, and in which direction
                queue.append(point)
                visited.add(point)

    # The final result is the number of squares that were energized (visited in
    # at least one direction)
    result = len(energized)

    print(result)


def part_two(puzzle_input: str) -> None:
    grid = puzzle_input.strip().splitlines()

    directions: dict[tuple[int, int], str] = {
        (0, 1): "right",
        (0, -1): "left",
        (1, 0): "down",
        (-1, 0): "up",
    }

    moves: dict[str, dict[str, list[tuple[int, int]]]] = {
        "right": {
            ".": [(0, 1)],
            "-": [(0, 1)],
            "|": [(-1, 0), (1, 0)],
            "/": [(-1, 0)],
            "\\": [(1, 0)],
        },
        "left": {
            ".": [(0, -1)],
            "-": [(0, -1)],
            "|": [(-1, 0), (1, 0)],
            "/": [(1, 0)],
            "\\": [(-1, 0)],
        },
        "down": {
            ".": [(1, 0)],
            "-": [(0, -1), (0, 1)],
            "|": [(1, 0)],
            "/": [(0, -1)],
            "\\": [(0, 1)],
        },
        "up": {
            ".": [(-1, 0)],
            "-": [(0, -1), (0, 1)],
            "|": [(-1, 0)],
            "/": [(0, 1)],
            "\\": [(0, -1)],
        },
    }

    # The solution is the same as in Part 1, however we now perform the calculation
    # for every starting point of the edge of the grid, in each direction
    starting_points: list[tuple[int, int, str]] = []

    for i in range(len(grid)):
        starting_points.append((i, 0, "right"))
        starting_points.append((i, len(grid[0]) - 1, "left"))

    for i in range(len(grid[0])):
        starting_points.append((0, i, "down"))
        starting_points.append((len(grid) - 1, i, "up"))

    result = 0

    for start in starting_points:
        visited: set[tuple[int, int, str]] = {start}
        energized: set[tuple[int, int]] = {(start[0], start[1])}
        queue: deque[tuple[int, int, str]] = deque([start])

        while queue:
            x, y, dir = queue.popleft()

            char = grid[x][y]

            new_moves = moves[dir][char]

            for move in new_moves:
                new_x, new_y = x + move[0], y + move[1]
                new_dir = directions[move]
                point = (new_x, new_y, new_dir)

                if (
                    0 <= new_x < len(grid)
                    and 0 <= new_y < len(grid[0])
                    and point not in visited
                ):
                    energized.add((new_x, new_y))
                    queue.append(point)
                    visited.add(point)

        # Update the final result if it is bigger than what we have seen so far
        result = max(result, len(energized))

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
