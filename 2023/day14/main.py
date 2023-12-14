import os


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    # Parse the grid as a list of list of strings
    grid = [list(line) for line in array]

    height, width = len(grid), len(grid[0])

    # Iterate through each column
    for i in range(width):
        # `j` will represent the index of the next free space (".")
        j = 0

        while j < height:
            # Keep moving `j` until we find a free space
            while j < height and grid[j][i] != ".":
                j += 1

            # `k` will be the index of the next non-free space ("O"/"#")
            k = j + 1

            # Increase `k` from `j` until we find a non-free space
            while k < height and grid[k][i] == ".":
                k += 1

            # If we are out of bounds, then there are no more rounded rocks in the column
            if k >= height:
                break

            # If `k` is at a rounded rock, then move the rock to index `j`
            if grid[k][i] == "O":
                grid[j][i] = "O"
                grid[k][i] = "."
                j += 1
            else:
                # Otherwise, `k` is a cube-shaped rock and cannot be moved, therefore
                # increase `j` to the next space below the rock and loop again
                j = k + 1

    result = 0

    # The load from each row is equal to the height minus the row index
    for i, line in enumerate(grid):
        load = height - i

        # For every "O" in the row, add on the load of the rock
        for char in line:
            if char == "O":
                result += load

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()
    grid = [list(line) for line in array]
    height, width = len(grid), len(grid[0])

    # Instead of tilting the board in four directions `n` times, we can consider it
    # as always tilting the board north, then rotating the board clockwise, `4n` times
    CYCLES = 1000000000
    total_cycles = 4 * CYCLES

    # After a certain number of iterations, the sequence of board patterns will
    # repeat. To identify when this occurs, use a cache, where the key is a string
    # representation of the board pattern, and the value is the number of iterations
    # to reach that pattern
    cache: dict[str, int] = {}

    # Whether the sequence has looped yet or not
    loop = False

    # 1-based index for number of iterations may be more intuitive
    iteration = 1

    while iteration < total_cycles + 1:
        for i in range(width):
            j = 0

            while j < height:
                while j < height and grid[j][i] != ".":
                    j += 1

                k = j + 1

                while k < height and grid[k][i] == ".":
                    k += 1

                if k >= height:
                    break

                if grid[k][i] == "O":
                    grid[j][i] = "O"
                    grid[k][i] = "."
                    j += 1
                else:
                    j = k + 1

        # `new_grid` represents the grid after the board has been 'rotated'
        new_grid: list[list[str]] = []

        # Loop through each column in the grid
        for i in range(width):
            # Extract the column from the grid
            col = [row[i] for row in grid]

            # Reverse the column and add it to the new grid
            new_grid.append(col[::-1])

        # `grid` now becomes the rotated grid
        grid = new_grid

        # The cache key will be the string representation of the rotated board
        key = str(grid)

        # If True, the sequence has begun to repeat
        if key in cache and not loop:
            loop = True

            # The number of iterations when we last saw this board pattern
            prev_iterations = cache[key]

            # The number of iterations required for the sequence to loop
            difference = iteration - prev_iterations

            # Essentially, we want to increase `iteration` by the largest multiple
            # of `difference`, while still remaining under `total_cycles`
            # The following equation calculates this in one step
            iteration = prev_iterations + difference * (
                (total_cycles - prev_iterations) // difference
            )
        else:
            # Save the number of iterations to the cache
            cache[key] = iteration

        iteration += 1

    result = 0

    for i, line in enumerate(grid):
        load = height - i

        for char in line:
            if char == "O":
                result += load

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
