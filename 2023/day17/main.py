import heapq
import os


def part_one(puzzle_input: str) -> None:
    # Parse the puzzle input as a list of list of integers
    grid = puzzle_input.strip().splitlines()
    grid = [list(map(int, list(line))) for line in grid]

    # Dict where the key is the direction and the value is the coordinates
    # corresponding to the direction
    directions: dict[str, tuple[int, int]] = {
        "right": (0, 1),
        "left": (0, -1),
        "down": (1, 0),
        "up": (-1, 0),
    }

    # Dict where each key-value pair is a set of opposite directions
    opposites = {
        "right": "left",
        "left": "right",
        "down": "up",
        "up": "down",
    }

    # Queue that contains the points in the grid to iterate through
    # The queue will be a heap, so iteration will proceed in the order of the
    # point with the smallest accumulated heat loss so far
    # Tuple - (total_heat_loss, x_coordinate, y_coordinate, direction)
    # Iteration will start from the point (0, 0), the top-left corner
    queue: list[tuple[int, int, int, str]] = [(0, 0, 0, "")]

    # `visited` will contain the minimum heat loss accumulated at a particular
    # point in the grid and facing a particular direction
    # Key - (x_coordinate, y_coordinate, direction)
    # Value - Minimum heat loss at this point and direction
    visited: dict[tuple[int, int, str], int] = {}

    result = None

    height, width = len(grid), len(grid[0])

    while True:
        # Remove the item with the smallest heat loss
        total, x, y, dir = heapq.heappop(queue)

        # If we are at the bottom-right point in the grid, then the heat loss so
        # far must be the final result (because we are using a heap, sorted by
        # heat loss)
        if (x, y) == (height - 1, width - 1):
            result = total
            break

        # Iterate in all directions around the current point
        for new_dir, (X, Y) in directions.items():
            # After moving in one direction, we cannot take another step in the
            # same direction, or go back on ourself. If either of these are true,
            # continue to the next direction
            if new_dir in (dir, opposites.get(dir)):
                continue

            new_total = total

            # Instead of moving one step at a time, move either 1, 2 or 3 steps
            # in one direction. The next step will be either left or right (as
            # explained above).
            for i in range(1, 4):
                new_x, new_y = x + X * i, y + Y * i

                # Check the next space is within the grid
                if 0 <= new_x < height and 0 <= new_y < width:
                    # Add on the heat loss from the new square
                    new_total += grid[new_x][new_y]

                    # If we have been at this space before, facing the same
                    # direction, ane with a smaller heat loss than now, then
                    # there is no point in continuing to iterate
                    if visited.get((new_x, new_y, new_dir), float("inf")) > new_total:
                        # Save the accumulated heat loss to the `visited` dict
                        visited[(new_x, new_y, new_dir)] = new_total

                        # Add the next point, with the new heat loss and direction,
                        # to the heap
                        heapq.heappush(queue, (new_total, new_x, new_y, new_dir))
                else:
                    # If we are outside of the grid, there is no point taking
                    # any further steps
                    break

    print(result)


def part_two(puzzle_input: str) -> None:
    grid = puzzle_input.strip().splitlines()
    grid = [list(map(int, list(line))) for line in grid]

    directions: dict[str, tuple[int, int]] = {
        "right": (0, 1),
        "left": (0, -1),
        "down": (1, 0),
        "up": (-1, 0),
    }

    opposites = {
        "right": "left",
        "left": "right",
        "down": "up",
        "up": "down",
    }

    queue: list[tuple[int, int, int, str]] = [(0, 0, 0, "")]
    visited: dict[tuple[int, int, str], int] = {}
    result = None
    height, width = len(grid), len(grid[0])

    while True:
        total, x, y, dir = heapq.heappop(queue)

        if (x, y) == (height - 1, width - 1):
            result = total
            break

        for new_dir, (X, Y) in directions.items():
            if new_dir in (dir, opposites.get(dir)):
                continue

            new_total = total

            # We now take between 1 and 10 steps in each direction
            for i in range(1, 11):
                new_x, new_y = x + X * i, y + Y * i

                if 0 <= new_x < height and 0 <= new_y < width:
                    new_total += grid[new_x][new_y]

                    # We can only stop on a square if we have taken at least 4
                    # steps, therefore continue to the next step if we have taken
                    # fewer than 4 steps
                    if i < 4:
                        continue

                    if visited.get((new_x, new_y, new_dir), float("inf")) > new_total:
                        visited[(new_x, new_y, new_dir)] = new_total
                        heapq.heappush(queue, (new_total, new_x, new_y, new_dir))
                else:
                    break

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
