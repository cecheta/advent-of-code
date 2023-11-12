def draw_grid(input: str, extra=0) -> tuple[list[list[str]], int]:
    """Function to create initial grid of rocks and air"""
    input_array = input.splitlines()

    height = 0

    # Find the largest y coordinate of the rocks
    for line in input_array:
        points = line.split(' -> ')

        for point in points:
            y = int(point.split(',')[1])
            height = max(height, y)

    # Add on extra height (required for part 2)
    height += extra

    # The width will be at-most double the height
    width = 2 * height

    # Create the grid according to the height and width, full of air
    grid = [['.' for _ in range(height + 1)] for _ in range(width + 1)]

    # All coordinates will be shifted to the left by `offset`
    offset = 500 - width // 2

    # Add the rocks into the grid
    for line in input_array:
        points = line.split(' -> ')

        for i in range(1, len(points)):
            point1, point2 = points[i - 1], points[i]
            x1, y1 = map(int, point1.split(','))
            x2, y2 = map(int, point2.split(','))

            # Add rocks from (x1, y1) to (x2, y1)
            for j in range(min(x1, x2), max(x1, x2) + 1):
                grid[j - offset][y1] = '#'

            # Add rocks from (x1, y1) to (x1, y2)
            for j in range(min(y1, y2), max(y1, y2) + 1):
                grid[x1 - offset][j] = '#'

    return (grid, offset)


def part_one(input: str):
    # Create the grid
    grid, offset = draw_grid(input)

    # Obtain the coordinate of the sand entry point
    start = (500 - offset, 0)

    count = 0
    result = None

    # Continue looping until we have a result
    while result is None:
        # i, j represent the coordinates of the current sand grain
        i, j = start

        while True:
            # If the sand grain is at the bottom of the grid, then it would
            # flow out of the bottom, therefore we have the result
            if j == len(grid[0]) - 1:
                result = count
                break

            # Check the three directions below the sand grain
            for a, b in ((i, j + 1), (i - 1, j + 1), (i + 1, j + 1)):
                # If the space below is empty, then move the sand grain into
                # the space
                if grid[a][b] == '.':
                    i, j = a, b
                    break
            else:
                # If we have reached here, then the sand grain cannot move
                # down, therefore it settles here
                grid[i][j] = 'o'
                break

        # Increment the counter
        count += 1

    print(result)


def part_two(input: str):
    # Add two extra rows when drawing the grid
    grid, offset = draw_grid(input, extra=2)

    # Fill the bottom row with rocks
    for row in grid:
        row[-1] = '#'

    # Obtain the coordinate of the sand entry point
    start = (500 - offset, 0)

    result = 0

    # Continue looping until a sand grain has settled at the entry point
    while grid[start[0]][start[1]] != 'o':
        # i, j represent the coordinates of the current sand grain
        i, j = start

        while True:
            # Check the three directions below the sand grain
            for a, b in ((i, j + 1), (i - 1, j + 1), (i + 1, j + 1)):
                # If the space below is empty, then move the sand grain into
                # the space
                if grid[a][b] == '.':
                    i, j = a, b
                    break
            else:
                # If we have reached here, then the sand grain cannot move
                # down, therefore it settles here
                grid[i][j] = 'o'
                break

        # Increment the counter
        result += 1

    print(result)


with open('input.txt') as f:
    input = f.read()


part_one(input)
part_two(input)
