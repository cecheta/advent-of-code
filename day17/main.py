def calculate(input: str, number: int) -> int:
    """
    Function to calculate the height of the tower after a certain number of
    rocks fall

    After a number of iterations, the height of the tower increases in a
    predictable cycle. We can determine when we are in a cycle based upon the
    current rock, wind, and the shape of the rocks in the tower.
    """
    input = input.strip()

    # List of the rocks, where each rock is a list of (x, y) coordinates
    rocks: list[list[tuple[int, int]]] = [
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (0, 1), (1, 0), (1, 1)]
    ]

    tower: set[tuple[int, int]] = set()

    height = 0
    wind_index = 0
    width = 7

    # `columns` contains the largest rock piece in each column
    columns = [0] * width

    # `seen` contains the hash of each iteration and the height of the tower
    # at that point
    seen: dict[str, tuple[int, int]] = {}

    i = 0
    extra = 0
    cycle = False

    while i < number:
        minimum = min(columns)

        # `profile` is a string of the relative heights of the columns in the
        # tower
        profile = ','.join([str(c - minimum) for c in columns])

        rock_index = i % len(rocks)

        # Create the string hash
        hash = f'{profile}|{rock_index}|{wind_index}'

        if hash in seen and not cycle:
            # If we have seen this hash before, then we have a cycle
            cycle = True

            # Calculate the number of iterations and the change in the height
            # of the tower since we saw this hash
            prev_index, prev_height = seen[hash]
            height_difference = height - prev_height
            index_difference = i - prev_index

            # Advance the index, and calculate the increase in height after
            # advancing the index
            x = (number - i) // index_difference

            i += index_difference * x
            extra = height_difference * x

            continue

        # Save the index number and current height into the dict
        seen[hash] = (i, height)

        rock = rocks[rock_index]

        # Starting position of the rock
        start = (2, height + 3)

        # Obtain the starting coordinates of the rock
        rock = [(x + start[0], y + start[1]) for x, y in rock]

        # Loop until the rock hits the floor or another rock
        while True:
            wind = input[wind_index]

            wind_index = (wind_index + 1) % len(input)

            # Obtain the coordinates of the rock after being moved by the wind
            rock_moved = [(x + (1 if wind == '>' else -1), y) for x, y in rock]

            # Only move the rock if it is within the bounds of the tower and
            # not occupied by another rock piece
            if all((x, y) not in tower and 0 <= x < width for x, y in rock_moved):
                rock = rock_moved

            # Obtain the coordinates of the rock after moving downwards
            rock_moved = [(x, y - 1) for x, y in rock]

            # If any of the rock pieces are already present in the tower, break
            if any((x, y) in tower or y < 0 for x, y in rock_moved):
                break

            # Otherwise, update the position of the rock
            rock = rock_moved

        for x, y in rock:
            # Add the rock pieces to the tower
            tower.add((x, y))

            # Update the height of the tower
            height = max(height, y + 1)

            # Update the height of each column
            columns[x] = max(columns[x], y + 1)

        i += 1

    return height + extra


def part_one(input: str):
    result = calculate(input, 2022)

    print(result)


def part_two(input: str):
    result = calculate(input, 1000000000000)

    print(result)


with open('input.txt') as f:
    input = f.read()


part_one(input)
part_two(input)
