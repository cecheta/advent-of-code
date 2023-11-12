import re
from typing import Optional


def part_one(input: str):
    input_array = input.splitlines()

    HEIGHT = 2000000

    intervals: list[tuple[int, int]] = []

    beacons: set[int] = set()

    for line in input_array:
        match = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)
        assert match

        # Obtain the coordinates of the sensor and the beacon
        x1, y1, x2, y2 = map(int, match.groups())

        # Calculate the distance between the two
        distance = abs(x2 - x1) + abs(y2 - y1)

        # If the line `HEIGHT` is within the sensor's area...
        if y1 - distance <= HEIGHT <= y1 + distance:
            # ...calculate the x position of the two points of intersection
            # between the sensor circumference and the `HEIGHT` line
            a1 = x1 - (distance - abs(HEIGHT - y1))
            a2 = x1 + distance - abs(HEIGHT - y1)

            # The interval is the space between the two points of intersection
            intervals.append((a1, a2))

            # Keep track of each beacon on the `HEIGHT` line
            if y2 == HEIGHT:
                beacons.add(x2)

    # Sort the intervals by the left point
    intervals.sort(key=lambda x: x[0])

    # `count` is the running total of the overlapping widths of all the
    # intervals, starting with the width of the first interval
    count = intervals[0][1] - intervals[0][0] + 1

    # `last` is the right-most point we have seen so far
    last = intervals[0][1]

    # Loop through the intervals, starting from the second
    for i in range(1, len(intervals)):
        x1, x2 = intervals[i]

        # If this interval end is to the right of the right-most we've seen...
        if x2 > last:
            # ...update the running total, depending on whether this interval
            # overlaps with previous intervals...
            count += x2 - max(x1 - 1, last)

            # ...and update the right-most point
            last = x2

    # Subtract all the beacons on the `HEIGHT` line
    count -= len(beacons)

    print(count)


def part_two(input: str):
    input_array = input.splitlines()

    LIMIT = 4000000

    sensors: list[tuple[int, int, int]] = []

    for line in input_array:
        match = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)
        assert match

        # Obtain the coordinates of the sensor and the beacon
        x1, y1, x2, y2 = map(int, match.groups())

        # Calculate the distance between the two
        distance = abs(x2 - x1) + abs(y2 - y1)

        # Keep track of all the sensors and the distance to the nearest beacon
        sensors.append((x1, y1, distance))

    coordinates: Optional[tuple[int, int]] = None

    # Loop through each y height, until we have the solution
    for y in range(LIMIT + 1):
        # If we have found the free point, then break
        if coordinates:
            break

        intervals: list[tuple[int, int]] = []

        # Loop through each sensor
        for x1, y1, distance in sensors:
            # If the line `y` is within the sensor's area...
            if y1 - distance <= y <= y1 + distance:
                # ...calculate the x position of the two points of intersection
                # between the sensor circumference and the `y` line
                a1 = x1 - (distance - abs(y - y1))
                a2 = x1 + distance - abs(y - y1)

                # The interval is the space between the two points of
                # intersection
                intervals.append((a1, a2))

        # Sort the intervals by the left point
        intervals.sort(key=lambda x: x[0])

        # `last` is the right-most point we have seen so far
        last = intervals[0][1]

        # Loop through the intervals, starting from the second
        for i in range(1, len(intervals)):
            x1, x2 = intervals[i]

            # If the start of this interval does not overlap with any previous
            # interval...
            if x1 > last:
                # ...then the free space must be one space to the left, at the
                # same height (assuming there is only one free space)
                coordinates = (x1 - 1, y)
                break

            # Otherwise, update the right-most point
            last = max(last, x2)

    assert coordinates

    # Calculate the tuning frequency
    result = coordinates[0] * 4000000 + coordinates[1]

    print(result)


def part_two_optimised(input: str):
    """
    This solution runs significantly faster than `part_two()`, by keeping track
    of each diagonal line 1 space away from a sensor's circumference (top-left,
    top-right, bottom-left, bottom-right), and looks for an intersection point
    of two perpendicular lines which is one space away from a (different)
    sensor's circumference in the four diagonal directions.
    """
    input_array = input.splitlines()

    LIMIT = 4000000

    negatives_top: dict[int, list[tuple[tuple[int, int], tuple[int, int]]]] = {}
    positives_top: dict[int, list[tuple[tuple[int, int], tuple[int, int]]]] = {}
    negatives_bottom: dict[int, list[tuple[tuple[int, int], tuple[int, int]]]] = {}
    positives_bottom: dict[int, list[tuple[tuple[int, int], tuple[int, int]]]] = {}

    for line in input_array:
        match = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)
        assert match

        x1, y1, x2, y2 = map(int, match.groups())

        distance = abs(x2 - x1) + abs(y2 - y1)

        l, r, t, b = (x1 - distance, y1), (x1 + distance, y1), (x1, y1 + distance), (x1, y1 - distance)

        negatives_top.setdefault(t[0] + t[1] + 1, []).append(((t[0] + 1, t[1]), (r[0], r[1] + 1)))
        negatives_bottom.setdefault(b[0] + b[1] - 1, []).append(((l[0], l[1] - 1), (b[0] - 1, b[1])))
        positives_top.setdefault(t[1] - t[0] + 1, []).append(((l[0], l[1] + 1), (t[0] - 1, t[1])))
        positives_bottom.setdefault(b[1] - b[0] - 1, []).append(((b[0] + 1, b[1]), (r[0], r[1] - 1)))

    negatives_top = {k: v for k, v in negatives_top.items() if k in negatives_bottom}
    positives_top = {k: v for k, v in positives_top.items() if k in positives_bottom}
    negatives_bottom = {k: v for k, v in negatives_bottom.items() if k in negatives_top}
    positives_bottom = {k: v for k, v in positives_bottom.items() if k in positives_top}

    coordinates: Optional[tuple[int, int]] = None

    for c1 in negatives_top:
        if coordinates:
            break

        for c2 in positives_top:
            intersection = (c1 - c2) // 2, (c1 + c2) // 2

            if not (0 <= intersection[0] <= LIMIT and 0 <= intersection[1] <= LIMIT):
                continue

            for interval in negatives_top[c1]:
                if interval[0][0] <= intersection[0] <= interval[1][0] and interval[0][1] >= intersection[1] >= interval[1][1]:
                    break
            else:
                continue

            for interval in negatives_bottom[c1]:
                if interval[0][0] <= intersection[0] <= interval[1][0] and interval[0][1] >= intersection[1] >= interval[1][1]:
                    break
            else:
                continue

            for interval in positives_top[c2]:
                if interval[0][0] <= intersection[0] <= interval[1][0] and interval[0][1] <= intersection[1] <= interval[1][1]:
                    break
            else:
                continue

            for interval in positives_bottom[c2]:
                if interval[0][0] <= intersection[0] <= interval[1][0] and interval[0][1] <= intersection[1] <= interval[1][1]:
                    break
            else:
                continue

            coordinates = intersection
            break

    assert coordinates

    result = coordinates[0] * 4000000 + coordinates[1]
    print(result)


with open('input.txt') as f:
    input = f.read()


part_one(input)
# part_two(input)
part_two_optimised(input)
