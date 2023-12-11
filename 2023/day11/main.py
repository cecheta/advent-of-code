import os


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    # `EXPANSION` is a constant that represents how much bigger the empty
    # rows and columns need to be
    EXPANSION = 2

    # These will contain the indexes of the empty rows and columns
    empty_rows: set[int] = set()
    empty_cols: set[int] = set()

    # Find the empty rows
    for i, row in enumerate(array):
        if all(char == "." for char in row):
            empty_rows.add(i)

    # Find the empty columns
    for i in range(len(array[0])):
        col = [line[i] for line in array]

        if all(char == "." for char in col):
            empty_cols.add(i)

    galaxies: list[tuple[int, int]] = []

    # Find all the galaxies in the array
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == "#":
                galaxies.append((i, j))

    result = 0

    # The shortest path between any two galaxies will be the sum of the horizontal
    # and vertical distances

    # Loop through each pair of galaxies
    for i in range(len(galaxies)):
        g1 = galaxies[i]

        for j in range(i + 1, len(galaxies)):
            g2 = galaxies[j]

            # (x1, y1) - coordinates of the first galaxy
            # (x2, y2) - coordinates of the second galaxy
            x1, y1, x2, y2 = g1 + g2

            # Swap the values if required so that x1 <= x2 and y1 <= y2
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1

            # Loop through every row between the two galaxies.
            # If it is an empty row, add on the expansion factor
            # Otherwise, increment by 1
            for k in range(x1 + 1, x2 + 1):
                if k in empty_rows:
                    result += EXPANSION
                else:
                    result += 1

            # Repeat for vertical distance, using empty columns
            for k in range(y1 + 1, y2 + 1):
                if k in empty_cols:
                    result += EXPANSION
                else:
                    result += 1

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    # Solution is identical to Part 1, except `EXPANSION` is now 1,000,000
    EXPANSION = 1000000

    empty_rows: set[int] = set()
    empty_cols: set[int] = set()

    for i, row in enumerate(array):
        if all(char == "." for char in row):
            empty_rows.add(i)

    for i in range(len(array[0])):
        col = [line[i] for line in array]

        if all(char == "." for char in col):
            empty_cols.add(i)

    galaxies: list[tuple[int, int]] = []

    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == "#":
                galaxies.append((i, j))

    result = 0

    for i in range(len(galaxies)):
        g1 = galaxies[i]

        for j in range(i + 1, len(galaxies)):
            g2 = galaxies[j]

            x1, y1, x2, y2 = g1 + g2

            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1

            for k in range(x1 + 1, x2 + 1):
                if k in empty_rows:
                    result += EXPANSION
                else:
                    result += 1

            for k in range(y1 + 1, y2 + 1):
                if k in empty_cols:
                    result += EXPANSION
                else:
                    result += 1

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()


part_one(puzzle_input)
part_two(puzzle_input)
