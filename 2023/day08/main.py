import re
import os


def part_one(puzzle_input: str) -> None:
    # Extract the instructions and the set of nodes from the puzzle input
    instructions, nodes_string = puzzle_input.strip().split("\n\n")

    # `nodes` will be a dict where each key is the node ID, and the value will be
    # another dict with two keys, "L" and "R", and the values of the left and
    # right nodes, respectively
    nodes: dict[str, dict[str, str]] = {}

    for line in nodes_string.splitlines():
        # Extract the node ID and the left and right nodes from the line
        match = re.match(r"(\w{3}) = \((\w{3}), (\w{3})\)", line)
        assert match is not None

        node, left, right = match.groups()

        # Add the left and right nodes to the dict
        nodes[node] = {}
        nodes[node]["L"] = left
        nodes[node]["R"] = right

    # Start from node "AAA"
    node = "AAA"
    count = 0

    # We finish looping once we have found node "ZZZ"
    while node != "ZZZ":
        # Take the next instruction, using modulo to "wrap round" if we reach the end
        # of the instruction set
        step = instructions[count % len(instructions)]

        # Take the next node from the dict
        node = nodes[node][step]

        # Increment the counter
        count += 1

    # The final result is equal to the number of iterations spent in the loop
    print(count)


def part_two(puzzle_input: str) -> None:
    instructions, nodes_string = puzzle_input.strip().split("\n\n")

    nodes: dict[str, dict[str, str]] = {}

    # `starting_nodes` will be a list of all the starting nodes (those ending in "A")
    starting_nodes: list[str] = []

    for line in nodes_string.splitlines():
        match = re.match(r"(\w{3}) = \((\w{3}), (\w{3})\)", line)
        assert match is not None

        node, left, right = match.groups()

        nodes[node] = {}
        nodes[node]["L"] = left
        nodes[node]["R"] = right

        if node.endswith("A"):
            # We have found a starting node, therefore add it to the list
            starting_nodes.append(node)

    # `iterations` will be a list of the number of iterations required to reach an end
    # node (one that ends in "Z")
    iterations: list[int] = []

    # Loop through each node
    for node in starting_nodes:
        count = 0

        # This time, loop until we find a node that ends in "Z"
        while not node.endswith("Z"):
            step = instructions[count % len(instructions)]
            node = nodes[node][step]
            count += 1

        # Add the result to the `iterations` list
        iterations.append(count)

    # The final answer is the lowest common multiple of all the values in the `iterations`
    # list. We could find this value using `math.lcm()`, however I have implemented
    # two functions to perform the calculation, so the solution can be more easily
    # translated into other programming languages.

    def gcd(a: int, b: int) -> int:
        if b == 0:
            return a

        return gcd(b, a % b)

    def lcm(numbers: list[int]) -> int:
        result = numbers[0]

        for num in numbers[1:]:
            result *= num // gcd(result, num)

        return result

    result = lcm(iterations)

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
