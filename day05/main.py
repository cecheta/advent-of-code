import re


def get_stacks(diagram: str) -> list[list[str]]:
    lines = diagram.splitlines()

    # We can get the number of stacks from the line length (due to trailing whitespace on each line)
    line_length = len(lines[0])
    num_of_stacks = (line_length + 1) // 4

    # Create empty stacks
    stacks: list[list[str]] = [[] for _ in range(num_of_stacks)]

    # Iterate from back to front so the top crate will be at the end of each stack
    lines.reverse()

    for line in lines:
        # This skips the line of stack indexes (the first line, after reversing)
        if not line.startswith('['):
            continue

        # The character can always be found at index 1, in groups of 4 (e.g. 1, 5, 9, ...)
        for i in range(1, line_length, 4):
            char = line[i]
            index = i // 4

            # Only add if the character isn't a space
            if not char.isspace():
                stacks[index].append(char)

    return stacks


def part_one(input: str):
    diagram, moves = input.strip('\n').split('\n\n')

    moves_list = moves.splitlines()

    stacks = get_stacks(diagram)

    for move in moves_list:
        # Parse the numbers as integers from the moves list
        matches = re.search(r'move (\d+) from (\d+) to (\d+)', move)
        assert matches is not None
        amount, from_index, to_index = map(int, matches.groups())

        # Moves list is 1-indexed, but `stacks` is 0-indexed
        from_stack, to_stack = stacks[from_index - 1], stacks[to_index - 1]

        for _ in range(amount):
            # Pop from `from_stack` and add to `to_stack`, `amount` number of times
            crate = from_stack.pop()
            to_stack.append(crate)

    # Iterate through the stacks and add the last crate from each stack to the result
    result = ''
    for stack in stacks:
        result += stack[-1]

    print(result)


def part_two(input: str):
    diagram, moves = input.strip('\n').split('\n\n')

    moves_list = moves.splitlines()

    stacks = get_stacks(diagram)

    for move in moves_list:
        # Parse the numbers as integers from the moves list
        matches = re.search(r'move (\d+) from (\d+) to (\d+)', move)
        assert matches is not None
        amount, from_index, to_index = map(int, matches.groups())

        # Moves list is 1-indexed, but `stacks` is 0-indexed
        from_stack, to_stack = stacks[from_index - 1], stacks[to_index - 1]

        # Find the index in `from_stack` from which every crate above the index will be moved (in one go)
        move_index = len(from_stack) - amount

        # List of crates to move
        crates_to_move = from_stack[move_index:]

        # Slice the `from_stack` list and put the sliced list inside `stacks` in the same index
        stacks[from_index - 1] = from_stack[:move_index]

        # Update `to_stack` in place
        to_stack.extend(crates_to_move)

    # Iterate through the stacks and add the last crate from each stack to the result
    result = ''
    for stack in stacks:
        result += stack[-1]

    print(result)


with open('input.txt') as f:
    input = f.read()

part_one(input)
part_two(input)
