import json
import math
import re
from typing import Literal

Material = Literal['ore', 'clay', 'obsidian', 'geode']


def calculate(line: str, time: int) -> int:
    maximum_geodes = 0
    cache: dict[str, int] = {}

    def recurse(costs: dict[Material, tuple[int, int, int]], robots: dict[Material, int], resources: dict[Material, int], time_left: int):
        nonlocal maximum_geodes

        if time_left < 0:
            return

        # The current state can be determined by the current number of robots
        # and resources
        hash = json.dumps((robots, resources))

        # If we have seen this state before, and there is less time remaining
        # than last time, then return early
        if hash in cache and cache[hash] >= time_left:
            return

        cache[hash] = time_left

        # Calculate the absolute maximum number of geodes if we created a new
        # geode robot each remaining minute
        geodes_limit = resources['geode'] + robots['geode'] * time_left + (time_left) * (time_left - 1) // 2

        # If the absolute maximum is smaller than the maximum we have seen so
        # far, return early
        if geodes_limit < maximum_geodes:
            return

        # Calculate the number of geodes we would create if we did not create
        # any more geode robots, and update `maximum_geodes`
        maximum_geodes = max(maximum_geodes, resources['geode'] + robots['geode'] * time_left)

        # Check recursively to create either a geode, obsidian, clay or ore
        # robot

        # Geode robot
        # Can only create a geode robot if we have at least one obsidian robot
        if robots['obsidian'] > 0:
            new_resources, new_robots = resources.copy(), robots.copy()

            # Work out how much time it would take to have enough resources
            # to create a geode robot
            time = max(
                math.ceil((costs['geode'][0] - new_resources['ore']) / new_robots['ore']),
                math.ceil((costs['geode'][2] - new_resources['obsidian']) / new_robots['obsidian']),
                0
            )

            # Add the resources created by the existing robots in the time elapsed
            for resource_type in new_resources:
                new_resources[resource_type] += new_robots[resource_type] * time

            # Subtract the cost of creating the new robot
            new_resources['ore'] -= costs['geode'][0]
            new_resources['obsidian'] -= costs['geode'][2]

            # Add the resources created in the minute while creaing the new robot
            for resource_type in new_resources:
                new_resources[resource_type] += new_robots[resource_type]

            # Add the new robot
            new_robots['geode'] += 1

            # Recurse, reducing the time appropriately
            recurse(costs, new_robots, new_resources, time_left - time - 1)

        # Obsidian robot
        # Can only create an obsidian robot if we have at least one clay robot
        # Also, there is no point creating a new obsidian robot if the current
        #   number of obsidian robots is greater than the obsidian cost to
        #   create a new geode robot
        if robots['clay'] > 0 and robots['obsidian'] < costs['geode'][2]:
            new_resources, new_robots = resources.copy(), robots.copy()

            time = max(
                math.ceil((costs['obsidian'][0] - new_resources['ore']) / new_robots['ore']),
                math.ceil((costs['obsidian'][1] - new_resources['clay']) / new_robots['clay']),
                0
            )

            for resource_type in new_resources:
                new_resources[resource_type] += new_robots[resource_type] * time

            new_resources['ore'] -= costs['obsidian'][0]
            new_resources['clay'] -= costs['obsidian'][1]

            for resource_type in new_resources:
                new_resources[resource_type] += new_robots[resource_type]

            new_robots['obsidian'] += 1

            recurse(costs, new_robots, new_resources, time_left - time - 1)

        # Clay robot
        # There is no point creating a new clay robot if the current
        #   number of clay robots is greater than the clay cost to
        #   create a new obsidian robot
        if robots['clay'] < costs['obsidian'][1]:
            new_resources, new_robots = resources.copy(), robots.copy()

            time = max(math.ceil((costs['clay'][0] - new_resources['ore']) / new_robots['ore']), 0)

            for resource_type in new_resources:
                new_resources[resource_type] += new_robots[resource_type] * time

            new_resources['ore'] -= costs['clay'][0]

            for resource_type in new_resources:
                new_resources[resource_type] += new_robots[resource_type]

            new_robots['clay'] += 1

            recurse(costs, new_robots, new_resources, time_left - time - 1)

        # Ore robot
        # There is no point creating a new ore robot if the current number
        # of ore robots is greater than the maximum ore cost to create a new
        # robot
        max_ore_cost = max(i[0] for i in costs.values())

        if robots['ore'] < max_ore_cost:
            new_resources, new_robots = resources.copy(), robots.copy()

            time = max(math.ceil((costs['ore'][0] - new_resources['ore']) / new_robots['ore']), 0)

            for resource_type in new_resources:
                new_resources[resource_type] += new_robots[resource_type] * time

            new_resources['ore'] -= costs['ore'][0]

            for resource_type in new_resources:
                new_resources[resource_type] += new_robots[resource_type]

            new_robots['ore'] += 1

            recurse(costs, new_robots, new_resources, time_left - time - 1)

    # Parse the numbers from the line
    matches = list(map(int, re.findall(r'(\d+)', line)))

    # The cost to create a robot of each type, [ore, clay, obsidian]
    costs: dict[Material, tuple[int, int, int]] = {
        'geode': (matches[5], 0, matches[6]),
        'obsidian': (matches[3], matches[4], 0),
        'clay': (matches[2], 0, 0),
        'ore': (matches[1], 0, 0)
    }

    # The initial number of robots
    robots: dict[Material, int] = {
        'geode': 0,
        'obsidian': 0,
        'clay': 0,
        'ore': 1
    }

    # The initial number of resources
    resources: dict[Material, int] = {
        'geode': 0,
        'obsidian': 0,
        'clay': 0,
        'ore': 0
    }

    recurse(costs, robots, resources, time)

    return maximum_geodes


def part_one(input: str):
    count = 0

    for i, line in enumerate(input.splitlines()):
        geodes = calculate(line, 24)

        # The blueprint ID number is the line index plus one
        count += geodes * (i + 1)

    print(count)


def part_two(input: str):
    result = 1

    # Iterate over the first three lines
    for line in input.splitlines()[:3]:
        result *= calculate(line, 32)

    print(result)


with open('input.txt') as f:
    input = f.read()


part_one(input)
part_two(input)
