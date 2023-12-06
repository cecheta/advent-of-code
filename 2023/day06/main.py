import math
import os
import re


def part_one(puzzle_input: str) -> None:
    """
    We can write the distance travelled by the boat, d, as a function of the time
    the button is held for, t:

    d = t(T - t)

    where T is the total time of the race.

    This is a quadratic equation. If d is set to the record distance, t will be the
    range of times (exclusive) that the button should be held for to break the record.

        T ± √(T^2 - 4d)
    t = ---------------
               2

    The solution will be any integer between t1 and t2, where t1 and t2 are the two
    solutions to the equation, and t1 < t2.
    """

    # Extract the times and distances from the puzzle input
    time_string, distance_string = puzzle_input.strip().split("\n")

    times: list[str] = re.findall(r"(\d+)", time_string)
    distances: list[str] = re.findall(r"(\d+)", distance_string)

    # Zip together each time with the record distance
    records: zip[tuple[str, str]] = zip(times, distances)

    # This will be the final result
    result = 1

    for time, distance in records:
        time = int(time)
        distance = int(distance)

        # Solve the quadratic equation
        # Note that instead of rounding up, we add one and round down, in case one
        # of the solutions to the equation is already an integer (and the reverse
        # for the other solution)
        time1 = math.floor(((time - math.sqrt(time**2 - 4 * distance)) / 2) + 1)
        time2 = math.ceil(((time + math.sqrt(time**2 - 4 * distance)) / 2) - 1)

        if time1 < time2:
            # Multiply the result by the number of solutions found
            result *= time2 - time1 + 1

    print(result)


def part_two(puzzle_input: str) -> None:
    time_string, distance_string = puzzle_input.strip().split("\n")

    # This time, extract one single time and one single distance
    time = int("".join(re.findall(r"\d", time_string)))
    distance = int("".join(re.findall(r"\d", distance_string)))

    time1 = math.floor(((time - math.sqrt(time**2 - 4 * distance)) / 2) + 1)
    time2 = math.ceil(((time + math.sqrt(time**2 - 4 * distance)) / 2) - 1)

    result = time2 - time1 + 1

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
