import os
import re
from typing import TypedDict


class Workflow(TypedDict):
    instructions: list[str]
    final: str


def part_one(puzzle_input: str) -> None:
    workflows_string, ratings_string = puzzle_input.strip().split("\n\n")

    workflows_list = workflows_string.splitlines()
    ratings = ratings_string.splitlines()

    # Each workflow will be represented in this dict, where the key is the name,
    # and the value is a dict of type `Workflow`
    workflows: dict[str, Workflow] = {}

    for line in workflows_list:
        match = re.match(r"(\w+){(.+),(\w+)}", line)
        assert match is not None

        name, instructions, final = match.groups()

        workflows[name] = {
            # The instructions in the workflow, e.g. "x>10:one"
            "instructions": instructions.split(","),
            "final": final,  # The name of the workflow to move to if all the instructions are not true
        }

        # For example:
        # "ex{x>10:one,m<20:two,a>30:R,A}"
        #
        # {
        #   "ex": {
        #     "instructions": ["x>10:one", "m<20:two", "a>30:R"]
        #     "final": "A"
        #   }
        # }

    result = 0

    # Loop through each rating in turn
    for line in ratings:
        # Remove the brackets
        categories = line[1:-1].split(",")

        # Extract the numbers from the line (each line is always in 'xmas' order)
        x, m, a, s = (int(cat.split("=")[1]) for cat in categories)

        # The starting workflow
        name = "in"

        # Continue looping until we reach "A" or "R"
        while name not in ("A", "R"):
            workflow = workflows[name]
            instructions = workflow["instructions"]

            for instruction in instructions:
                # Extract the expression and the associated workflow name
                test, next_name = instruction.split(":")

                # UNSAFE - Use eval to determine whether the expression is true
                if eval(test):
                    # If true, then move to the next workflow
                    name = next_name
                    break
            else:
                # If we have tried all instructions unsuccessfully, then move to `final`
                name = workflow["final"]

        # If it is accepted, add the individual ratings
        if name == "A":
            result += x + m + a + s

    print(result)


def part_two(puzzle_input: str) -> None:
    workflows_string = puzzle_input.strip().split("\n\n")[0]
    workflows_list = workflows_string.splitlines()

    workflows: dict[str, Workflow] = {}

    for line in workflows_list:
        match = re.match(r"(\w+){(.+),(\w+)}", line)
        assert match is not None

        name, instructions, final = match.groups()

        workflows[name] = {
            "instructions": instructions.split(","),
            "final": final,
        }

    def calculate(ratings: dict[str, tuple[int, int]]) -> int:
        """
        Calculate the distinct combinations for this range of ratings
        """

        result = 1

        for low, high in ratings.values():
            result *= high - low + 1

        return result

    # We will use a queue to perform BFS
    # Each item in the queue contains the range of values for each rating
    # i.e. { "x": (1, 4000) } means that "x" could range from 1 to 4000
    # Each item in the queue also contains the current workflow
    # We start from "ie", with each rating ranging from 1 to 4000
    # Each time we move to a new workflow, add a new item to the queue
    queue: list[tuple[dict[str, tuple[int, int]], str]] = [
        (
            {
                "x": (1, 4000),
                "m": (1, 4000),
                "a": (1, 4000),
                "s": (1, 4000),
            },
            "in",
        )
    ]

    result = 0

    while queue:
        ratings, name = queue.pop(0)

        # If this is rejected, then continue
        if name == "R":
            continue

        # If it is accepted, calculate the distinct combinations for the range of values
        if name == "A":
            result += calculate(ratings)
            continue

        workflow = workflows[name]
        instructions = workflow["instructions"]

        # Evaluate the expression in relation to the range in the ratings
        # For example, x: (1, 4000), and x > 3000
        for instruction in instructions:
            test, next_name = instruction.split(":")

            match = re.match(r"([xmas])([<>])(\d+)", test)
            assert match is not None

            # Extract the rating, operation (< or >), and threshold
            rating, op, threshold = match.groups()
            threshold = int(threshold)

            lower, upper = ratings[rating]

            if op == ">":
                if lower > threshold:
                    # The full range complies with the expression, therefore
                    # move to the next workflow
                    queue.append((ratings, next_name))
                    break
                elif upper < threshold:
                    # The full range is outside of the expression, therefore
                    # continue to the next instruction
                    continue
                else:
                    # The expression splits the range of ratings, therefore
                    # we need to split the ratings into two
                    # For example, if x: (1, 4000), and x > 2000, then split
                    # into (1, 2000) and (2001, 4000)
                    new_ratings = ratings.copy()
                    new_upper = threshold + 1

                    # In this half, the expression is true, therefore move
                    # to the next workflow
                    new_ratings[rating] = (new_upper, upper)
                    queue.append((new_ratings, next_name))

                    # In this half, the expression is false, therefore move
                    # to the next instruction
                    ratings[rating] = (lower, threshold)

            # This is the same as above, but the reverse (<)
            else:
                if upper < threshold:
                    queue.append((ratings, next_name))
                    break
                elif lower > threshold:
                    continue
                else:
                    new_ratings = ratings.copy()
                    new_upper = threshold - 1

                    new_ratings[rating] = (lower, new_upper)
                    queue.append((new_ratings, next_name))

                    ratings[rating] = (threshold, upper)

        else:
            # If we have gone through all the instructions, then move to the
            # final workflow
            queue.append((ratings, workflow["final"]))

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
