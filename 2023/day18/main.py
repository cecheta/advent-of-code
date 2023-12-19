import os


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    # Dict where the key is the direction to move in and the value is the
    # coordinates corresponding to the direction
    directions: dict[str, tuple[int, int]] = {
        "R": (0, 1),
        "D": (1, 0),
        "L": (0, -1),
        "U": (-1, 0),
    }

    # Start from (0, 0)
    point: tuple[int, int] = (0, 0)

    # `loop` contains the coordinates of all the vertices in the loop of trench
    loop: list[tuple[int, int]] = []

    for line in array:
        # Ignore the hex colour from the puzzle input
        dir, moves, _ = line.split(" ")

        moves = int(moves)
        x, y = directions[dir]

        # Take `moves` number of steps in the correct direction away from `point`
        new_x, new_y = point[0] + x * moves, point[1] + y * moves

        # (new_x, new_y) is the new `point`, which will be used in the next iteration
        point = (new_x, new_y)

        # Add the new point to the list
        loop.append(point)

    # Sort the points in the loop, by x-coordinate, then y-coordinate
    loop.sort()

    def contains_interval(
        intervals: set[tuple[int, int]],
        next_interval: tuple[int, int],
    ) -> bool:
        """
        If we are already tracking this interval, then remove it from the set
        as it is the end of the interval within the shape.

        ______________
                      |
                      |
        ______________|
        """

        if next_interval in intervals:
            intervals.remove(next_interval)
            return True

        return False

    def in_between_interval(
        intervals: set[tuple[int, int]],
        next_interval: tuple[int, int],
    ) -> bool:
        """
        If the next interval exists within an existing interval, then split
        the interval into two smaller intervals.

        _______________
                    ___
                   |
                   |
                   |
                   |___

        _______________
        """

        for a, b in intervals:
            if a < next_interval[0] < next_interval[1] < b:
                intervals.remove((a, b))
                intervals.add((a, next_interval[0]))
                intervals.add((next_interval[1], b))
                return True

        return False

    def joined_to_two_intervals(
        intervals: set[tuple[int, int]],
        next_interval: tuple[int, int],
    ) -> bool:
        """
        If the next interval is joined to two existing interavls, then combine
        the two to make one larger interval. Add the length of the new
        interval to the area.

        ________________
        ____________
                    |
                    |
        ____________|

        ________________
        """

        nonlocal result

        interval1 = interval2 = None

        for a, b in intervals:
            if a == next_interval[1]:
                interval1 = (a, b)
                break

        for a, b in intervals:
            if b == next_interval[0]:
                interval2 = (a, b)
                break

        if interval1 != interval2 and interval1 is not None and interval2 is not None:
            result += next_interval[1] - next_interval[0] - 1
            intervals.remove(interval1)
            intervals.remove(interval2)
            intervals.add((interval2[0], interval1[1]))
            return True

        return False

    def joined_to_one_interval(
        intervals: set[tuple[int, int]],
        next_interval: tuple[int, int],
    ) -> bool:
        """
        If the next interval is joined to one existing interavls, then adjust the
        length of the existing interval. If the interval gets larger, add the new
        length to the area.

                     ____       ____________
                    |                       |
        ____________|       OR              |____

        _________________       _________________
        """

        nonlocal result

        for a, b in intervals:
            if b == next_interval[0]:
                result += next_interval[1] - next_interval[0]
                intervals.add((a, next_interval[1]))
                break
            if b == next_interval[1]:
                intervals.add((a, next_interval[0]))
                break
            if a == next_interval[1]:
                result += next_interval[1] - next_interval[0]
                intervals.add((next_interval[0], b))
                break
            if a == next_interval[0]:
                intervals.add((next_interval[1], b))
                break
        else:
            return False

        intervals.remove((a, b))
        return True

    def add_interval(
        intervals: set[tuple[int, int]],
        next_interval: tuple[int, int],
    ) -> None:
        """
        This is a new interval, therefore add it to the set of intervals, and
        add its length to the area.

        _____________

        _____________

                 ____
                |
                |____

        """

        nonlocal result

        intervals.add(next_interval)
        result += next_interval[1] - next_interval[0] + 1

    pass

    # To find the area of the shape, we move through the shape from left to right,
    # with a vertical line. The area of the shape will be the area that the
    # vertical line passes through as it moves through the shape.
    # Note: The x-axis is to the right, and the y-axis is up.
    #
    # The vertical line will be a set of intervals within the shape. Each time
    # the line reaches a vertex in the shape, the intervals will updated as
    # appropriate.

    # `intervals` is the set of intervals ww are tracking within the shape
    intervals: set[tuple[int, int]] = set()

    # Start from the x-coordinate furthest to the left
    pointer = loop[0][0]

    result = 0

    # We want to find the next intervals in the loop, therefore loop two points
    # at a time. Both points will have the same x-coordinate but different
    # y-coordinates, corresponding to the next interval in the shape.
    # For two points, (x1, y1) and (x2, y2):
    # x1 == x2
    # y1 < y2 (because `loop` is sorted)
    for i in range(0, len(loop), 2):
        # `next_pointer` is the x-coordinate of the next point we want to move to,
        # which is the x-coordinate of the next interval in the shape
        next_pointer = loop[i][0]

        # The y-coordinates of the next interval in the shape
        next_interval = (loop[i][1], loop[i + 1][1])

        # For each interval in the shape, calculate the area covered when moving
        # from `pointer` to `next_pointer`. Add this to the final result.
        for a, b in intervals:
            result += (b - a + 1) * (next_pointer - pointer)

        # Update the pointer
        pointer = next_pointer

        # We now need to update the intervals we are tracking in the shape
        # Each function will update `intervals` and `result`, and return True
        # if it modified the interval, meaning that subsequent code in the
        # if-statement will not run. Each function explains what it is
        # checking for.
        if contains_interval(intervals, next_interval):
            continue
        elif in_between_interval(intervals, next_interval):
            continue
        elif joined_to_two_intervals(intervals, next_interval):
            continue
        elif joined_to_one_interval(intervals, next_interval):
            continue
        else:
            # If none of the above are true, then this is a new interval
            # that should now be tracked
            add_interval(intervals, next_interval)

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    # We now use numbers to correspond to the directions
    directions: dict[str, tuple[int, int]] = {
        "0": (0, 1),
        "1": (1, 0),
        "2": (0, -1),
        "3": (-1, 0),
    }

    point: tuple[int, int] = (0, 0)
    loop: list[tuple[int, int]] = []

    for line in array:
        # Extract the 6 characters from the hex colour (remove '#' and brackets)
        hex_colour = line.split(" ")[2][2:-1]

        # The last character is the direction, the others are the number of moves
        number, dir = hex_colour[:-1], hex_colour[-1]

        moves = int(number, 16)
        x, y = directions[dir]

        new_x, new_y = point[0] + x * moves, point[1] + y * moves

        point = (new_x, new_y)
        loop.append(point)

    loop.sort()

    def contains_interval(
        intervals: set[tuple[int, int]],
        next_interval: tuple[int, int],
    ) -> bool:
        if next_interval in intervals:
            intervals.remove(next_interval)
            return True

        return False

    def in_between_interval(
        intervals: set[tuple[int, int]],
        next_interval: tuple[int, int],
    ) -> bool:
        for a, b in intervals:
            if a < next_interval[0] < next_interval[1] < b:
                intervals.remove((a, b))
                intervals.add((a, next_interval[0]))
                intervals.add((next_interval[1], b))
                return True

        return False

    def joined_to_two_intervals(
        intervals: set[tuple[int, int]],
        next_interval: tuple[int, int],
    ) -> bool:
        nonlocal result

        interval1 = interval2 = None

        for a, b in intervals:
            if a == next_interval[1]:
                interval1 = (a, b)
                break

        for a, b in intervals:
            if b == next_interval[0]:
                interval2 = (a, b)
                break

        if interval1 != interval2 and interval1 is not None and interval2 is not None:
            result += next_interval[1] - next_interval[0] - 1
            intervals.remove(interval1)
            intervals.remove(interval2)
            intervals.add((interval2[0], interval1[1]))
            return True

        return False

    def joined_to_one_interval(
        intervals: set[tuple[int, int]],
        next_interval: tuple[int, int],
    ) -> bool:
        nonlocal result

        for a, b in intervals:
            if b == next_interval[0]:
                result += next_interval[1] - next_interval[0]
                intervals.add((a, next_interval[1]))
                break
            if b == next_interval[1]:
                intervals.add((a, next_interval[0]))
                break
            if a == next_interval[1]:
                result += next_interval[1] - next_interval[0]
                intervals.add((next_interval[0], b))
                break
            if a == next_interval[0]:
                intervals.add((next_interval[1], b))
                break
        else:
            return False

        intervals.remove((a, b))
        return True

    def add_interval(
        intervals: set[tuple[int, int]],
        next_interval: tuple[int, int],
    ) -> None:
        nonlocal result

        intervals.add(next_interval)
        result += next_interval[1] - next_interval[0] + 1

    intervals: set[tuple[int, int]] = set()
    pointer = loop[0][0]
    result = 0

    for i in range(0, len(loop), 2):
        next_pointer = loop[i][0]
        next_interval = (loop[i][1], loop[i + 1][1])

        for a, b in intervals:
            result += (b - a + 1) * (next_pointer - pointer)

        pointer = next_pointer

        if contains_interval(intervals, next_interval):
            continue
        elif in_between_interval(intervals, next_interval):
            continue
        elif joined_to_two_intervals(intervals, next_interval):
            continue
        elif joined_to_one_interval(intervals, next_interval):
            continue
        else:
            add_interval(intervals, next_interval)

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
