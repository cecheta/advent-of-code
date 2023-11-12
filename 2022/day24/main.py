def move_blizzards(blizzards: set[tuple[int, int, int, int]], height: int, width: int) -> tuple[set[tuple[int, int, int, int]], set[tuple[int, int]]]:
    new_blizzards: set[tuple[int, int, int, int]] = set()
    occupied: set[tuple[int, int]] = set()

    for blizzard in blizzards:
        new_blizzards.add(((blizzard[0] + blizzard[2]) % height, (blizzard[1] + blizzard[3]) % width, blizzard[2], blizzard[3]))
        occupied.add(((blizzard[0] + blizzard[2]) % height, (blizzard[1] + blizzard[3]) % width))

    return new_blizzards, occupied


def part_one(input: str):
    board = input.splitlines()

    # Get the height and width of the inner board (excluding the border)
    height, width = len(board) - 2, len(board[0]) - 2

    blizzards: set[tuple[int, int, int, int]] = set()

    for i in range(1, height + 1):
        for j in range(1, width + 1):
            square = board[i][j]

            # Add the blizards into the set (shifting the origin of the grid)
            # Also add the coordinates in which the blizzard moves
            match square:
                case '>':
                    blizzards.add((i - 1, j - 1, 0, 1))
                case '<':
                    blizzards.add((i - 1, j - 1, 0, -1))
                case '^':
                    blizzards.add((i - 1, j - 1, -1, 0))
                case 'v':
                    blizzards.add((i - 1, j - 1, 1, 0))
                case '.':
                    pass
                case _:
                    raise Exception(f'Unexpected symbol: {square}')

    # After a certain number of steps, the blizzards will cycle round
    # We can calculate this by placing two blizzards at (0, 0), one moving
    # down, the other moving right, and calculate the number of steps until
    # the blizzards overlap again
    l, r = [0, 1], [1, 0]
    cycle = 1

    while l != r:
        cycle += 1
        l[1] = (l[1] + 1) % width
        r[0] = (r[0] + 1) % height

    # The start point is (-1, 0)
    queue: list[tuple[int, int]] = [(-1, 0)]

    steps = 0

    seen: set[tuple[int, int, int]] = set()

    result = None

    while not result and queue:
        steps += 1

        new_queue: list[tuple[int, int]] = []

        # Move all the blizzards one step
        # Also obtain all the squares where a blizzard is present
        blizzards, occupied = move_blizzards(blizzards, height, width)

        for x, y in queue:
            # Check moving in all directions, including standing still
            for a, b in ((0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)):
                X, Y = x + a, y + b

                # If we are at the end, set the result to the number of steps
                # travelled
                if (X, Y) == (height, width - 1):
                    result = steps
                    break

                # To move into the new space, the following must be true:
                #   The space is within the grid
                #     or, the space must be the start point (-1, 0)
                #   The space should not have a blizzard
                #   We have not stepped here before (on the same blizzard cycle)
                if ((0 <= X < height and 0 <= Y < width) or (X, Y) == (-1, 0)) and (X, Y) not in occupied and (X, Y, steps % cycle) not in seen:
                    # Add the space into `seen`, including the blizzard cycle
                    seen.add((X, Y, steps % cycle))

                    # Add the space into the queue to iterate on the next loop
                    new_queue.append((X, Y))

            # If we have the result, break
            if result:
                break

        # Reset the queue for the next loop
        queue = new_queue

    print(result)


def part_two(input: str):
    board = input.splitlines()

    # Get the height and width of the inner board (excluding the border)
    height, width = len(board) - 2, len(board[0]) - 2

    blizzards: set[tuple[int, int, int, int]] = set()

    for i in range(1, height + 1):
        for j in range(1, width + 1):
            square = board[i][j]

            # Add the blizards into the set (shifting the origin of the grid)
            # Also add the coordinates in which the blizzard moves
            match square:
                case '>':
                    blizzards.add((i - 1, j - 1, 0, 1))
                case '<':
                    blizzards.add((i - 1, j - 1, 0, -1))
                case '^':
                    blizzards.add((i - 1, j - 1, -1, 0))
                case 'v':
                    blizzards.add((i - 1, j - 1, 1, 0))
                case '.':
                    pass
                case _:
                    raise Exception(f'Unexpected symbol: {square}')

    # After a certain number of steps, the blizzards will cycle round
    # We can calculate this by placing two blizzards at (0, 0), one moving
    # down, the other moving right, and calculate the number of steps until
    # the blizzards overlap again
    l, r = [0, 1], [1, 0]
    cycle = 1

    while l != r:
        cycle += 1
        l[1] = (l[1] + 1) % width
        r[0] = (r[0] + 1) % height

    # The start point is (-1, 0)
    # We start on trip 1
    queue: list[tuple[int, int, int]] = [(-1, 0, 1)]

    steps = 0

    seen: set[tuple[int, int, int, int]] = set()

    result = None

    while not result and queue:
        steps += 1

        new_queue: list[tuple[int, int, int]] = []

        # Move all the blizzards one step
        # Also obtain all the squares where a blizzard is present
        blizzards, occupied = move_blizzards(blizzards, height, width)

        for x, y, trip in queue:
            # Check moving in all directions, including standing still
            for a, b in ((0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)):
                X, Y = x + a, y + b

                # Check if we are at the end point
                if (X, Y) == (height, width - 1):
                    # If we are on the first trip, add the new space, and
                    # increment the trip number
                    if trip == 1:
                        seen.add((X, Y, trip + 1, steps % cycle))
                        new_queue.append((X, Y, trip + 1))
                        continue
                    # If we are on the third trip, we have the result
                    if trip == 3:
                        result = steps
                        break

                # If we are at the start point, and on the second trip, add the
                # space and increment the trip number
                if (X, Y) == (-1, 0) and trip == 2:
                    seen.add((X, Y, trip + 1, steps % cycle))
                    new_queue.append((X, Y, trip + 1))
                    continue

                # Otherwise, to move into the new space, the following must be true:
                #   The space is within the grid
                #     or, the space must be either the start or end point
                #   The space should not have a blizzard
                #   We have not stepped here before (on the same blizzard cycle)
                if ((0 <= X < height and 0 <= Y < width) or (X, Y) in ((-1, 0), (height, width - 1))) and (X, Y) not in occupied and (X, Y, trip, steps % cycle) not in seen:
                    seen.add((X, Y, trip, steps % cycle))
                    new_queue.append((X, Y, trip))

            # If we have the result, break
            if result:
                break

        # Reset the queue for the next loop
        queue = new_queue

    print(result)


with open('input.txt') as f:
    input = f.read()


part_one(input)
part_two(input)
