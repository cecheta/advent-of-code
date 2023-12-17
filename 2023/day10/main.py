import os


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    start: tuple[int, int] | None = None

    # Find the coordinates of the starting point
    for i, line in enumerate(array):
        for j, char in enumerate(line):
            if char == "S":
                start = (i, j)

    assert start is not None

    # dict that contains the vectors to move in a particular direction
    directions: dict[str, tuple[int, int]] = {
        "right": (0, 1),
        "left": (0, -1),
        "up": (-1, 0),
        "down": (1, 0),
    }

    # A dict, where the key is the direction currently being moved in, and
    # the value is another dict where the key is the next pipe encountered,
    # and the value is the direction that we are now moving in after passing
    # through the pipe
    # For example, if we are moving right, and encounter a "7" pipe, then we
    # will now be moving down
    moves = {
        "right": {
            "-": "right",
            "7": "down",
            "J": "up",
        },
        "left": {
            "-": "left",
            "L": "up",
            "F": "down",
        },
        "up": {
            "|": "up",
            "7": "left",
            "F": "right",
        },
        "down": {
            "|": "down",
            "J": "left",
            "L": "right",
        },
    }

    # Posistions is a list that will initially contain the two valid points adjacent
    # to the starting point
    positions: list[tuple[int, int, str, int]] = []

    # Iterate in the four directions around the starting point
    for dir, (i, j) in directions.items():
        x, y = start[0] + i, start[1] + j

        # Check the adjacent square is within the array
        if 0 <= x < len(array) and 0 <= y < len(array[0]):
            char = array[x][y]

            # If True, then the adjacent square is a valid move from the starting point
            # For example, if we are moving to the right from the starting point, and we
            # encounter "|", this would not be a valid move, but "J" would be
            if char in moves[dir]:
                # x and y are the coordinates of the pipes
                # dir is the direction we are currently moving in
                # `1` is the number of moves we have made from the starting point
                positions.append((x, y, dir, 1))

    result = None

    while result is None:
        x, y, dir, num = positions.pop(0)
        char = array[x][y]

        # We can use the `moves` dict to quickly determine the new direction we are,
        # moving in, after going through the pipe
        next_dir = moves[dir][char]
        coords = directions[next_dir]

        # Get the new coordinates after moving through the pipe
        new_x, new_y = x + coords[0], y + coords[1]

        # Add the new position to the `positions` list, incrementing the number of
        # moves taken
        positions.append((new_x, new_y, next_dir, num + 1))

        # When we have manoeuvered around the whole loop, the coordinates of the
        # two points in the list will be identical (although different directions),
        # as well as the number of moves taken, therefore we can take the final
        # number of moves from either position
        if positions[0][:2] == positions[1][:2]:
            result = positions[0][3]

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    start: tuple[int, int] | None = None

    for i, line in enumerate(array):
        for j, char in enumerate(line):
            if char == "S":
                start = (i, j)

    assert start is not None

    directions: dict[str, tuple[int, int]] = {
        "right": (0, 1),
        "left": (0, -1),
        "up": (-1, 0),
        "down": (1, 0),
    }

    moves = {
        "right": {
            "-": "right",
            "7": "down",
            "J": "up",
        },
        "left": {
            "-": "left",
            "L": "up",
            "F": "down",
        },
        "up": {
            "|": "up",
            "7": "left",
            "F": "right",
        },
        "down": {
            "|": "down",
            "J": "left",
            "L": "right",
        },
    }

    # We no longer need to keep track of the number of moves taken
    positions: list[tuple[int, int, str]] = []

    for dir, (i, j) in directions.items():
        x, y = start[0] + i, start[1] + j

        if 0 <= x < len(array) and 0 <= y < len(array[0]):
            char = array[x][y]

            if char in moves[dir]:
                positions.append((x, y, dir))

    # A set containing the coordinates of all pipes in the loop
    loop: set[tuple[int, int]] = {start}

    while True:
        x, y, dir = positions.pop(0)

        # Iterate until we come across a point we have already seen
        if (x, y) in loop:
            break

        loop.add((x, y))

        char = array[x][y]

        next_dir = moves[dir][char]
        coords = directions[next_dir]
        new_x, new_y = x + coords[0], y + coords[1]

        positions.append((new_x, new_y, next_dir))

    # Before calculating the enclosed loop, we need to replace the starting character
    # with an appropriate pipe symbol. The following functions are used to determine
    # whether a symbol next to the starting character could be valid.
    # For example, left() returns True if the square to the left of the square
    # provided is within the grid, and the pipe to the left could be reached from
    # the square provided. For example, "L" is valid, but "J" is not.
    def left(x: int, y: int) -> bool:
        y -= 1
        if 0 <= y and (x, y) in loop:
            char = array[x][y]
            if char in moves["left"]:
                return True
        return False

    def right(x: int, y: int) -> bool:
        y += 1
        if y < len(array[0]) and (x, y) in loop:
            char = array[x][y]
            if char in moves["right"]:
                return True
        return False

    def up(x: int, y: int) -> bool:
        x -= 1
        if 0 <= x and (x, y) in loop:
            char = array[x][y]
            if char in moves["up"]:
                return True
        return False

    # The following code is used to replace the starting character "S" with the
    # appropriate pipe character. For example, if "S" has valid pipes to the right
    # and below, then it should be replaced with "F"
    if left(*start):
        if up(*start):
            array[start[0]] = array[start[0]].replace("S", "J")
        elif right(*start):
            array[start[0]] = array[start[0]].replace("S", "-")
        else:
            # We have checked all other directions, therefore it must be down
            # (assuming the puzzle input is valid)
            array[start[0]] = array[start[0]].replace("S", "7")
    elif right(*start):
        if up(*start):
            array[start[0]] = array[start[0]].replace("S", "L")
        else:
            # We do not need to check left here, as it was checked previously
            array[start[0]] = array[start[0]].replace("S", "F")
    else:
        # If we reach here, the valid pipes must be above and below
        array[start[0]] = array[start[0]].replace("S", "|")

    # To calculate the number of tiles in the inner loop, we will iterate from left
    # to right across each row. For each tile inside the loop, we increment the final result.
    # Note that whe moving from left to right, we can only first encounter "|", "L" or
    # "F".
    # "-", "J" and "7" can only be found after first encountering one of those three.
    # If we encounter "|", then we have crossed from inside to outside, or vice versa.
    # If we encounter "L" or "F", then whether we cross the boundary depends on the
    # value of the next non-horizontal pipe ("-") we find. If we encounter a "L",
    # followed by "J", then we have not crossed the boundary. However, if we
    # encounter "L", followed by "7", then we will cross the boundary, and move from
    # inside to outside, or vice versa. Similar can be said for "F", but reversed.
    # For example:
    #
    #   |
    # → L--7  In this scenario, we will cross the boundary when moving from left
    #      |  to right along the arrow
    #
    #   |  |  In this scenario, we will not cross the boundary when moving from
    # → L--J  left to right along the arrow, but remain either inside or outside

    # `pairs` is a dict to help know if we are crossing the boundary when encountering
    # either "L" or "F". For example, pairs["L"]["7"] is True, therefore if we
    # encounter a "L" followed by a "7", then we will cross the boundary.
    pairs = {
        "L": {
            "J": False,
            "7": True,
        },
        "F": {
            "J": True,
            "7": False,
        },
    }

    # Boolean to know whether we are currently inside of the loop or not
    inside = False

    result = 0
    x = 0

    # Loop through each tile in each row, one by one
    while x < len(array):
        y = 0

        while y < len(array[0]):
            char = array[x][y]

            # Here, we are on the loop boundary
            if (x, y) in loop:
                # If we encounter a "|", then we have crossed the boundary
                if char == "|":
                    inside = not inside
                # Here, we have encountered either "L" or "F"
                elif char in pairs:
                    y += 1
                    # Continue moving to the right until we have passed the
                    # horizontal pipes
                    while array[x][y] == "-":
                        y += 1

                    next_char = array[x][y]

                    # Use `pairs` to determine if we have crossed the boundary or not
                    if pairs[char][next_char]:
                        inside = not inside
            elif inside:
                # If we are inside the loop, then increment the final result
                result += 1

            y += 1
        x += 1

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()


part_one(puzzle_input)
part_two(puzzle_input)
