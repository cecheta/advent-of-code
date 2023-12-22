import os


def part_one(puzzle_input: str) -> None:
    # Parse the input as a list of list of strings
    array = puzzle_input.strip().splitlines()
    grid = [list(line) for line in array]

    start = None

    # Find the start point
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == "S":
                start = (i, j)
                break

    assert start is not None

    # The directions we can move in
    moves: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Set containing the plots we have seen so far
    seen: set[tuple[int, int]] = {start}

    # Queue of plots used for BFS
    queue: list[tuple[int, int]] = [start]

    def valid_point(x: int, y: int, grid: list[list[str]]) -> bool:
        """
        Function that returns true if (x, y) is within the grid, and is a garden plot
        """

        if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != "#":
            return True

        return False

    # Instead of moving one square at a time, we move two squares at once, and perform
    # half as many loops. This way, we do not have to navigate to squares we have
    # already visited.
    for _ in range(64 // 2):
        new_queue: list[tuple[int, int]] = []

        for x, y in queue:
            for a, b in moves:
                # Take one step from the current square, and check to see if
                # we are on a valid square
                x1, y1 = x + a, y + b

                if valid_point(x1, y1, grid):
                    # If so, take a second step and check to see if this step is
                    # also valid
                    for c, d in moves:
                        x2, y2 = x1 + c, y1 + d
                        new_point = (x2, y2)

                        if valid_point(x2, y2, grid) and new_point not in seen:
                            # Add the new square to the queue
                            seen.add(new_point)
                            new_queue.append(new_point)

        queue = new_queue

    # The final result will be the total number of squares we visited
    result = len(seen)

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()
    grid = [list(line) for line in array]

    start = None

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == "S":
                start = (i, j)
                break

    assert start is not None

    moves: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def valid_point(x: int, y: int, grid: list[list[str]]) -> bool:
        # Need to take the modulo of the coordinates, as the grid now repeats
        # This uses Python's wrap-around behaviour with lists
        # i.e. grid[-1] == grid[len(grid) - 1]
        x %= len(grid)
        y %= len(grid[0])

        if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != "#":
            return True

        return False

    total = 26501365

    # We would expect the sequence to loop on a cycle of len(grid) number of
    # iterations (note that the puzzle input is a square). We multiply this by
    # 2 because we are looping 2 iterations at a time.
    step = len(grid) * 2

    # Once we find the cycle in the sequence, we can skip forwards to the result.
    # To be able to skip forwards, we need to find the offset, so that:
    # offset + (step * n) == total, where n is an integer
    offset = total % step

    # Note that because the total number of steps is an odd number, we need to
    # perform one single step before looping in steps of 2
    seen: set[tuple[int, int]] = set()
    queue: list[tuple[int, int]] = []

    iteration = 1

    for a, b in moves:
        x, y = start[0] + a, start[1] + b

        if valid_point(x, y, grid):
            seen.add((x, y))
            queue.append((x, y))

    # From analysing the solution, after x amount of iterations, the sequence of
    # `step` iterations forms a quadratic sequence. `diff1` containa the difference
    # between two consecutive numbers, `diff2` contains the difference between
    # two consecutive numbers in `diff1`, and similar for `diff3`. For a
    # quadratic sequence, we would expect `diff3` to contain the same number
    # each time, therefore we iterate until two consecutive values in `diff3` are
    # the same.
    diff1 = []
    diff2 = []
    diff3 = []

    while len(diff3) < 2 or diff3[-1] != diff3[-2]:
        new_queue: list[tuple[int, int]] = []

        for x, y in queue:
            for a, b in moves:
                x1, y1 = x + a, y + b

                if valid_point(x1, y1, grid):
                    for c, d in moves:
                        x2, y2 = x1 + c, y1 + d
                        new_point = (x2, y2)

                        if valid_point(x2, y2, grid) and new_point not in seen:
                            seen.add(new_point)
                            new_queue.append(new_point)

        queue = new_queue

        iteration += 2

        # We save the values every `step` number of iterations, from `offset`
        if (iteration - offset) % step == 0:
            diff1.append(len(seen))

            if len(diff1) > 1:
                diff2.append(diff1[-1] - diff1[-2])

            if len(diff2) > 1:
                diff3.append(diff2[-1] - diff2[-2])

    # `steps` is how much we need to move forwards from the number of iterations
    # we performed to the final number of iterations, `total`
    steps = ((total - iteration) // step) + 2

    # Once we have reached here, we have enough values to find the final result,
    # essentially by calculating the sum of an arithmetic sequence.
    constant = diff3[-1]
    result = int(diff1[-3] + (steps / 2) * (2 * diff2[-2] + (steps - 1) * constant))

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
