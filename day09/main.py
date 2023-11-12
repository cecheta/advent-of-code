import math


def get_length(x: int, y: int) -> float:
    """Returns the length of a vector from the origin"""
    return math.sqrt(x ** 2 + y ** 2)


def make_moves(positions: list[tuple[int, int]], direction: str) -> list[tuple[int, int]]:
    # `positions` is a list of all the knots in the rope, with the head at the end
    head = positions[-1]

    # Move the head in the specified direction
    if direction == 'U':
        head = (head[0], head[1] + 1)
    elif direction == 'R':
        head = (head[0] + 1, head[1])
    elif direction == 'D':
        head = (head[0], head[1] - 1)
    elif direction == 'L':
        head = (head[0] - 1, head[1])
    else:
        raise Exception('Invalid direction')

    # Update the new head within the `positions` list
    positions[-1] = head

    # Iterate backwards through all other knots to see if they also need moving
    for i in range(len(positions) - 1, 0, -1):
        # `head` and `tail` are the next two adjacent knots
        head, tail = positions[i], positions[i - 1]

        # Calculate the vector between the two knots, and the vector's length
        vector = [head[0] - tail[0], head[1] - tail[1]]
        vector_length = get_length(vector[0], vector[1])

        # If the length is less than 2, then the knots are still touching,
        # therefore there are no more knots to move
        if vector_length < 2.0:
            break

        # The tail needs to move halfway in the direction of the vector
        if abs(vector[0]) == 2:
            vector[0] //= 2
        if abs(vector[1]) == 2:
            vector[1] //= 2

        # Move the tail in the direction of the new vector
        tail = (tail[0] + vector[0], tail[1] + vector[1])

        # Update the new tail inside the `positions` list
        positions[i - 1] = tail

    return positions


def calculate(moves: list[str], knots: int) -> int:
    # Each knot starts at (0, 0)
    positions: list[tuple[int, int]] = [(0, 0) for _ in range(knots)]

    # `seen` keeps track of where the tail has been
    seen: set[tuple[int, int]] = set()

    for move in moves:
        direction, steps = move.split(' ')

        for _ in range(int(steps)):
            positions = make_moves(positions, direction)

            # The tail is the first item in the list
            seen.add(positions[0])

    return len(seen)


def part_one(input: str):
    moves = input.splitlines()
    result = calculate(moves, 2)
    print(result)


def part_two(input: str):
    moves = input.splitlines()
    result = calculate(moves, 10)
    print(result)


with open('input.txt') as f:
    input = f.read()

part_one(input)
part_two(input)
