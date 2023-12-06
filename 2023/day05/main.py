import os
import re
from textwrap import dedent


def part_one(puzzle_input: str) -> None:
    # This regex is used to extract the seeds and the almanac maps from the puzzle input
    pattern_raw = dedent(
        r"""
        ^seeds: (.*)

        seed-to-soil map:
        ((?:.|\n)*)

        soil-to-fertilizer map:
        ((?:.|\n)*)

        fertilizer-to-water map:
        ((?:.|\n)*)

        water-to-light map:
        ((?:.|\n)*)

        light-to-temperature map:
        ((?:.|\n)*)

        temperature-to-humidity map:
        ((?:.|\n)*)

        humidity-to-location map:
        ((?:.|\n)*)$
        """.strip(
            "\n"
        )
    )

    pattern = re.compile(pattern_raw, re.MULTILINE)
    match = re.search(pattern, puzzle_input.strip())
    assert match is not None

    # Extract all of the capture groups from the regex, splitting each new line
    groups: list[list[str]] = [group.split("\n") for group in match.groups()]

    # Take the seeds from the first group, as a list of integers
    seeds = map(int, groups[0][0].split(" "))

    # All other capture groups are the almanac maps
    almanac_maps = groups[1:]

    result = float("inf")

    for seed in seeds:
        # `current_value` is the value as it is mapped through each almanac map
        current_value = seed

        # Loop through each almanac map
        for almanac_map in almanac_maps:
            for line in almanac_map:
                # Extract the destination, source and range from each line in the map
                destination, source, range_length = map(int, line.split(" "))

                # If the current value falls within the range from the source, then map it to the destination
                if source <= current_value < source + range_length:
                    current_value = destination + (current_value - source)
                    break

                # Otherwise, move to the next line in the map

            # If none of the lines in the almanac map matched the current value, then the
            # value does not need to be transformed

        # Once the value has been transformed through each almanac map, keep track of the
        # lowest final value (location) so far
        result = min(result, current_value)

    print(result)


def part_two(puzzle_input: str) -> None:
    """
    The solution to Part 2 is similar to Part 1, with an added optimisation.

    We do not need to calculate the final location for every single seed, as in the vast
    majority of cases, increasing the seed number by 1 will also increase the final location
    by 1.

    We only need to re-calculate whenever we change the line we are using in one of the
    almanac maps.

    As we iterate through each almanac map for a particular seed, keep track of the number of
    points by which we would have to increase the current value before we would have to change
    the line we are using for that almanac map. The lowest of these values across all the maps
    gives us the value by which we can increase the seed number by, knowing that the final
    location of all the seeds we skipped will not be lower than the value we just calculated.
    """

    pattern_raw = dedent(
        r"""
        ^seeds: (.*)

        seed-to-soil map:
        ((?:.|\n)*)

        soil-to-fertilizer map:
        ((?:.|\n)*)

        fertilizer-to-water map:
        ((?:.|\n)*)

        water-to-light map:
        ((?:.|\n)*)

        light-to-temperature map:
        ((?:.|\n)*)

        temperature-to-humidity map:
        ((?:.|\n)*)

        humidity-to-location map:
        ((?:.|\n)*)$
        """.strip(
            "\n"
        )
    )

    pattern = re.compile(pattern_raw, re.MULTILINE)
    match = re.search(pattern, puzzle_input.strip())
    assert match is not None

    groups: list[list[str]] = [group.split("\n") for group in match.groups()]

    seeds = list(map(int, groups[0][0].split(" ")))
    almanac_maps = groups[1:]

    result = float("inf")

    # Iterate through each pair of values
    for i in range(0, len(seeds), 2):
        start, number_of_seeds = seeds[i], seeds[i + 1]
        seed = start

        while seed < start + number_of_seeds:
            current_value = seed

            # `lowest` will be the value by which we would have to increase `seed`
            # by before we use a different line in one of the almanac maps
            lowest = float("inf")

            for almanac_map in almanac_maps:
                for line in almanac_map:
                    destination, source, range_length = map(int, line.split(" "))

                    if source <= current_value < source + range_length:
                        # Work out the difference between the end of the range and the
                        # current value
                        # Update `lowest` if it is smaller than what we have seen so far
                        lowest = min(lowest, source + range_length - current_value)

                        current_value = destination + (current_value - source)
                        break

                    # If we do not use the line in the almanac map, work out how much
                    # we would have to increase the current value by until we would
                    # use that line
                    # Update `latest` if it is smaller than what we have seen so far
                    if source > current_value:
                        lowest = min(lowest, source - current_value)

            result = min(result, current_value)

            seed += lowest

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
