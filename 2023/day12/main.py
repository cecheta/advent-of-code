import os


def part_one(puzzle_input: str) -> None:
    def recurse(
        row: str, groups: list[int], cache: dict[tuple[int, int], int] = {}
    ) -> int:
        """
        Recursive function that is used to return the number of valid arrangements
        of springs, given a character sequence of springs and list of groups.
        The solution will contain overlapping subproblems, therefore use a
        cache to reduce the number of computations
        """

        # The cache key will be a tuple of the number of remaining characters
        # in the row, and the number of groups remaining
        key = (len(row), len(groups))

        # If we have seen this subproblem before, return the cached solution
        if key in cache:
            return cache[key]

        # This will be the default return value, indicating that the sequence is invalid
        total = 0

        # Use a loop here, so we can quickly break out of the loop if the sequence
        # is invalid
        for _ in range(1):
            # We have no more groups to find
            if not groups:
                # If there are no more damaged springs, then the sequence is valid
                # Assume that any "?" will be "."
                if all(char != "#" for char in row):
                    total = 1
                # Otherwise, it is invalid
                break

            # Skip through any operational springs
            i = 0
            while i < len(row) and row[i] == ".":
                i += 1

            # We have reached the end, yet still have groups to find, therefore it is invalid
            if i == len(row):
                break

            # `groups[0]` is the next group that needs to be found
            group_length = groups[0]

            # Create a substring of length `group_length`
            segment = row[i : i + group_length]

            # There isn't enough of the row remaining to make the required group length,
            # therefore the sequence is invalid
            if len(segment) != group_length:
                break

            # If True, then the segment is only comprised of "#" and "?", therefore it
            # could be valid if all "?" are "#"
            if "." not in segment:
                # In this case, the end of the segment is also the end of the sequence
                if i + group_length == len(row):
                    # Recurse, advancing the sequence to after the segment (which is also
                    # the end of the string), and removing a group from `groups`
                    total += recurse(row[i + group_length :], groups[1:], cache)

                # In this case, the next character after the segment cannot be "#",
                # otherwise the segment length would not be `group_length`. The subsequent
                # character must be ".", or "?" which we assume to be "."
                elif row[i + group_length] != "#":
                    # Recurse, advancing the sequence to after the segment "plus 1", and
                    # removing a group from `groups`
                    total += recurse(row[i + group_length + 1 :], groups[1:], cache)

            # If the next character in the sequence is "?", recurse to consider the case where
            # "?" is changed to ".", and the number of groups is left unchanged
            if row[i] == "?":
                total += recurse(row[i + 1 :], groups, cache)

        # Save the value to the cache before returning
        cache[key] = total

        return total

    array = puzzle_input.strip().splitlines()

    result = 0

    for line in array:
        # Obtain the row of characters and the groups from the puzzle input
        row, group_string = line.split(" ")

        # Transform the groups from a string to a list of integers
        groups = list(map(int, group_string.split(",")))

        result += recurse(row, groups, {})

    print(result)


def part_two(puzzle_input: str) -> None:
    def recurse(
        row: str, groups: list[int], cache: dict[tuple[int, int], int] = {}
    ) -> int:
        """
        The function is identical to Part 1
        """

        key = (len(row), len(groups))
        if key in cache:
            return cache[key]

        total = 0

        for _ in range(1):
            if not groups:
                if all(char != "#" for char in row):
                    total = 1
                break

            i = 0
            while i < len(row) and row[i] == ".":
                i += 1

            if i == len(row):
                break

            group_length = groups[0]
            segment = row[i : i + group_length]

            if len(segment) != group_length:
                break

            if "." not in segment:
                if i + group_length == len(row):
                    total += recurse(row[i + group_length :], groups[1:], cache)
                elif row[i + group_length] != "#":
                    total += recurse(row[i + group_length + 1 :], groups[1:], cache)

            if row[i] == "?":
                total += recurse(row[i + 1 :], groups, cache)

        cache[key] = total

        return total

    array = puzzle_input.strip().splitlines()

    result = 0

    for line in array:
        row, group_string = line.split(" ")
        groups = list(map(int, group_string.split(",")))

        # Increase the row and groups by a factor of 5, according to the
        # criteria given in the problem
        row = "?".join([row] * 5)
        groups *= 5

        result += recurse(row, groups, {})

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()


part_one(puzzle_input)
part_two(puzzle_input)
