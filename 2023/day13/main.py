import os


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().split("\n\n")
    grids = [grid.splitlines() for grid in array]

    result = 0

    for grid in grids:
        # First, iterate through the spaces between the rows
        for i in range(1, len(grid)):
            # `i` represents the number of rows above the mirror line
            # `j` and `k` are the indexes of the rows to compare around the
            # mirror line
            j, k = i - 1, i

            # Check each row until we are outside of the grid
            while 0 <= j < len(grid) and 0 <= k < len(grid):
                row1, row2 = grid[j], grid[k]

                # If the rows are not the same, then we are not on the mirror line
                if row1 != row2:
                    break

                # Move the rows to compare away from the mirror line
                j -= 1
                k += 1
            else:
                # If we reach here, then every row that we compared was identical,
                # therefore `i` is the mirror line
                result += 100 * i
                break

        # If we reach the else block, then we iterated through all of the rows
        # without ever finding a mirror line, and never broke out of the loop.
        # This means we also need to iterate through the columns.
        else:
            # Now iterate through the spaces between the columns
            for i in range(1, len(grid[0])):
                # `i` represents the number of columns to the left of the mirror line
                j, k = i - 1, i

                while 0 <= j < len(grid[0]) and 0 <= k < len(grid[0]):
                    # Extract the rows from the grid
                    col1 = [row[j] for row in grid]
                    col2 = [row[k] for row in grid]

                    if col1 != col2:
                        break

                    j -= 1
                    k += 1
                else:
                    result += i
                    break

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().split("\n\n")
    grids = [grid.splitlines() for grid in array]

    result = 0

    def find_smudge(line1: list[str], line2: list[str]) -> bool:
        """
        This function returns True if two lines differ by exactly one character,
        and False if otherwise
        """

        smudge = False

        for num1, num2 in zip(line1, line2):
            if num1 != num2:
                if not smudge:
                    # This is the first difference found so far, so it could be
                    # a smudge
                    smudge = True
                else:
                    # We have already found one difference, therefore we have too
                    # many differences and it is not a smudge
                    smudge = False
                    break

        return smudge

    # In Part 2, the mirror line is where only one set of rows about the mirror
    # line differ by exactly one character, and the other rows are identical

    for grid in grids:
        for i in range(1, len(grid)):
            j, k = i - 1, i

            # `smudge` represents whether we have found two rows that differ by
            # one character
            smudge = False

            while 0 <= j < len(grid) and 0 <= k < len(grid):
                row1, row2 = grid[j], grid[k]

                if row1 != row2:
                    # We cannot have two sets of rows that differ, therefore if we
                    # have already found a smudge, then this cannot be the solution
                    if smudge:
                        break

                    # Check to see if it is possible that we have a smudge (the
                    # rows differ by only one character)
                    smudge = find_smudge(list(row1), list(row2))

                    # If do not have a smudge (the rows differ by more than one character),
                    # this cannot be the solution
                    if not smudge:
                        break

                j -= 1
                k += 1
            else:
                # If we reach here, and have found a smudge, then this is the mirror
                # line. If we reached here without finding a smudge, then this would be
                # the same line as in Part 1
                if smudge:
                    result += 100 * i
                    break

        else:
            for i in range(1, len(grid[0])):
                j, k = i - 1, i
                smudge = False

                while 0 <= j < len(grid[0]) and 0 <= k < len(grid[0]):
                    col1 = [row[j] for row in grid]
                    col2 = [row[k] for row in grid]

                    if col1 != col2:
                        if smudge:
                            break
                        smudge = find_smudge(col1, col2)
                        if not smudge:
                            break

                    j -= 1
                    k += 1
                else:
                    if smudge:
                        result += i
                        break

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
