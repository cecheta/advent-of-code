from functools import reduce


def part_one(input: str):
    grid = input.splitlines()

    # Turn the strings of numbers into lists of integers
    num_grid = [[int(val) for val in row] for row in grid]

    # Calculate the height and width of the grid
    height, width = len(num_grid), len(num_grid[0])

    # All trees on the outer edge are visible by default
    # Remove 4 to not double-count
    outer_edge = 2 * (height + width) - 4
    total = outer_edge

    # Use a set to keep track of trees that have already been visited
    seen: set[tuple[int, int]] = set()

    def check_tree(i: int, j: int, tree: int, maximum: int) -> int:
        # If we haven't seen this tree before, and it is larger than the maximum we've seen so far,
        # then we need to count it
        if (i, j) not in seen and tree > maximum:
            # Add the co-ordinates to `seen` so we don't double-count it in a later iteration
            seen.add((i, j))
            return 1

        return 0

    # Iterate through each row
    # Ignore the outer edges as they have already been counted
    for i in range(1, height - 1):
        # Calculate the maximum at each end of the row
        maximum_left = num_grid[i][0]
        maximum_right = num_grid[i][-1]

        # Iterate forwards along the row
        for j in range(1, width - 1):
            tree = num_grid[i][j]

            # `check_tree()` will return `1` if the tree is larger than the current maximum
            # and we haven't counted the tree before, otherwise `0`
            total += check_tree(i, j, tree, maximum_left)

            # Update `maximum_left` to keep track of the largest tree we've seen so far (from the left)
            maximum_left = max(maximum_left, tree)

        # Iterate backwards along the row
        for j in range(width - 2, 0, -1):
            tree = num_grid[i][j]
            total += check_tree(i, j, tree, maximum_right)
            maximum_right = max(maximum_right, tree)

    # Iterate through each column
    for j in range(1, width - 1):
        maximum_top = num_grid[0][j]
        maximum_bottom = num_grid[-1][j]

        # Iterate down the column
        for i in range(1, height - 1):
            tree = num_grid[i][j]
            total += check_tree(i, j, tree, maximum_top)
            maximum_top = max(maximum_top, tree)

        # Iterate up the column
        for i in range(height - 2, 0, -1):
            tree = num_grid[i][j]
            total += check_tree(i, j, tree, maximum_bottom)
            maximum_bottom = max(maximum_bottom, tree)

    print(total)


def part_two(input: str):
    grid = input.splitlines()

    # Turn the strings of numbers into lists of integers
    num_grid = [[int(val) for val in row] for row in grid]

    # Calculate the height and width of the grid
    height, width = len(grid), len(grid[0])

    maximum = 0

    # Iterate through each tree
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            # `scores` will keep hold of the view in each direction
            scores: list[int] = []
            tree = num_grid[i][j]

            # Iterate along each direction (x or y, forwards or backwards)
            for x, y in (0, 1), (1, 0), (0, -1), (-1, 0):
                a, b = i, j

                while True:
                    # Move along the axis
                    a, b = a + x, b + y
                    next_tree = num_grid[a][b]

                    # Break from the loop if we are at the edge, or if the next tree is not smaller than the original tree
                    if not (0 < a < height - 1 and 0 < b < width - 1 and next_tree < tree):
                        break

                # The score is the absolute distance from where we started
                # The distance of one of the directions will always be 0
                scores.append(abs((a - i) + (b - j)))

            # Multiply the individual scores to obtain the overall score
            score = reduce(lambda x, y: x * y, scores)

            # Update the maximum value if `score` is larger than the current `maximum`
            maximum = max(maximum, score)

    print(maximum)


with open('input.txt') as f:
    input = f.read()

part_one(input)
part_two(input)
