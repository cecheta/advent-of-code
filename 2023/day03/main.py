def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    # A list of directions adjacent to a square
    directions: list[tuple[int, int]] = [
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
    ]

    result = 0
    i = 0

    # Loop through every character in the grid
    while i < len(array):
        row = array[i]
        j = 0

        while j < len(row):
            # If the character is a number...
            if row[j].isdigit():
                start = j

                # Find the end character of the number
                while j < len(row) and row[j].isdigit():
                    j += 1

                end = j

                # Iterate through all characters in the number
                for k in range(start, end):
                    # Iterate in all directions around the character
                    for X, Y in directions:
                        x, y = i + X, k + Y

                        # Check if the adjacent character is a symbol (not a number or a `.`)
                        if (
                            0 <= x < len(array)
                            and 0 <= y < len(row)
                            and array[x][y] != "."
                            and not array[x][y].isdigit()
                        ):
                            # Since we have found a symbol, add the value of the number to the final result, and break
                            result += int(row[start:end])
                            break
                    else:
                        # Otherwise, continue to the next direction
                        continue

                    # If we reach here, we have found an adjacent symbol, therefore break
                    break
            else:
                j += 1

        i += 1

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    directions: list[tuple[int, int]] = [
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
    ]

    result = 0
    i = 0

    # Gears is a dict that will contain the co-ordinates of each gear, and a list
    # of numbers that are adjacent to each gear
    gears: dict[tuple[int, int], list[int]] = {}

    while i < len(array):
        row = array[i]
        j = 0

        while j < len(row):
            if row[j].isdigit():
                start = j

                while j < len(row) and row[j].isdigit():
                    j += 1

                end = j

                for k in range(start, end):
                    for X, Y in directions:
                        x, y = i + X, k + Y

                        # Check to see if we are at a gear
                        if (
                            0 <= x < len(array)
                            and 0 <= y < len(row)
                            and array[x][y] == "*"
                        ):
                            number = int(row[start:end])

                            # Add the number to the `gears` dict
                            if (x, y) not in gears:
                                gears[(x, y)] = []
                            gears[(x, y)].append(number)

                            break
                    else:
                        continue

                    break
            else:
                j += 1

        i += 1

    # Loop through each gear that was found
    for numbers in gears.values():
        # If there are exactly two numbers adjacent to this gear, add the
        # gear ratio to the final result
        if len(numbers) == 2:
            result += numbers[0] * numbers[1]

    print(result)


with open("input.txt") as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
