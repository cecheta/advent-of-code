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


with open('input.txt') as f:
    input = f.read()


part_one(input)
part_two(input)
