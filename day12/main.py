def find_letter(grid: list[list[str]], letter: str) -> tuple[int, int]:
    """
    Function to find the coordinates of a letter in the grid
    """
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == letter:
                return (i, j)

    raise Exception(f'{letter} not found')


def part_one(input: str):
    # Parse the grid
    grid = [list(row) for row in input.splitlines()]

    # Find the coordinates of the start and end points
    start = find_letter(grid, 'S')
    end = find_letter(grid, 'E')

    # Replace the start and end points with their heights
    grid[start[0]][start[1]] = 'a'
    grid[end[0]][end[1]] = 'z'

    # Breadth-first search
    # queue - list containing next squares to visit
    # seen - set of coordinates of squares that we've already visited, starting
    #   from the start square
    queue: list[tuple[int, int, int]] = [(start[0], start[1], 0)]
    seen = {start}

    result = -1

    while queue:
        new_queue: list[tuple[int, int, int]] = []

        # Obtain coordinates of current square, as well as iteration number
        for x, y, i in queue:
            # If we are at the end square, then return the iteration number
            if (x, y) == end:
                result = i
                break

            # Obtain the height (letter) of the current square
            height = grid[x][y]

            # Iterate in all adjacent directions
            for X, Y in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                a, b = x + X, y + Y

                # If the adjacent square is within the grid, and we haven't visited
                # this square before...
                if 0 <= a < len(grid) and 0 <= b < len(grid[0]) and (a, b) not in seen:
                    # ...then find the height of this adjacent square
                    next_height = grid[a][b]

                    # If the adjacent square is at most one level higher than the
                    # current square...
                    if ord(next_height) - ord(height) <= 1:
                        # ...then add the square into the `seen` set...
                        seen.add((a, b))

                        # ...and add it to the queue (to visit later), incrementing
                        # the iteration number
                        new_queue.append((a, b, i + 1))

        else:
            # If we didn't break out of the loop, then reset the queue
            # and continue
            queue = new_queue
            continue

        # Otherwise, we have found the result
        break

    print(result)


def part_two(input: str):
    # Parse the grid
    grid = [list(row) for row in input.splitlines()]

    # Find the coordinates of the start and end points
    start = find_letter(grid, 'S')
    end = find_letter(grid, 'E')

    # Replace the start and end points with their heights
    grid[start[0]][start[1]] = 'a'
    grid[end[0]][end[1]] = 'z'

    # Breadth-first search
    # queue - list containing next squares to visit
    # seen - set of coordinates of squares that we've already visited, starting
    #   from the end square
    queue: list[tuple[int, int, int]] = [(end[0], end[1], 0)]
    seen = {end}

    result = -1

    while queue:
        new_queue: list[tuple[int, int, int]] = []

        # Obtain coordinates of current square, as well as iteration number
        for x, y, i in queue:
            # Obtain the height of the current square
            height = grid[x][y]

            # If the height is 'a', then return the iteration number
            if height == 'a':
                result = i
                break

            # Iterate in all adjacent directions
            for X, Y in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                a, b = x + X, y + Y

                # If the adjacent square is within the grid, and we haven't visited
                # this square before...
                if 0 <= a < len(grid) and 0 <= b < len(grid[0]) and (a, b) not in seen:
                    # ...then find the height of this adjacent square
                    next_height = grid[a][b]

                    # If the current square is at most one level higher than the
                    # adjacent square...
                    if ord(height) - ord(next_height) <= 1:
                        # ...then add the square into the `seen` set...
                        seen.add((a, b))

                        # ...and add it to the queue (to visit later), incrementing
                        # the iteration number
                        new_queue.append((a, b, i + 1))

        else:
            # If we didn't break out of the loop, then reset the queue
            # and continue
            queue = new_queue
            continue

        # Otherwise, we have found the result
        break

    print(result)


with open('input.txt') as f:
    input = f.read()

part_one(input)
part_two(input)
