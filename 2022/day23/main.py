def get_adjacents(x: int, y: int) -> list[tuple[int, int]]:
    """Function to return the coordinates of all squares adjacent to (x, y)"""
    return [
        (x + 1, y),
        (x + 1, y + 1),
        (x, y + 1),
        (x - 1, y + 1),
        (x - 1, y),
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
    ]


def part_one(input: str):
    elves: set[tuple[int, int]] = set()

    # Iterate through the grid input
    for i, row in enumerate(input.splitlines()):
        for j, col in enumerate(row):
            if col == '#':
                # Add the elf into the set
                # Coordinates: →x , ↑y
                elves.add((j, -i))

    # The directions to check
    # The first item in each sub-list is the direction to move if all spaces
    # are free (e.g. move N if N, NW and NE are all free)
    all_directions: list[list[tuple[int, int]]] = [
        [(0, 1), (-1, 1), (1, 1)],
        [(0, -1), (-1, -1), (1, -1)],
        [(-1, 0), (-1, 1), (-1, -1)],
        [(1, 0), (1, 1), (1, -1)]
    ]

    for _ in range(10):
        elves_to_move: list[tuple[int, int]] = []

        for elf in elves:
            # Get adjacent squares
            adjacents = get_adjacents(*elf)

            # If any adjacent square is occupied, then the elf can potentially move
            if any(square in elves for square in adjacents):
                elves_to_move.append(elf)

        # `moves` is a dict where each key is the coordinates of a square, and
        # the value is a list of elves that want to move into that square
        moves: dict[tuple[int, int], list[tuple[int, int]]] = {}

        for elf in elves_to_move:
            for directions in all_directions:
                # If all adjacent squares in `directions` are empty...
                if all((elf[0] + x, elf[1] + y) not in elves for x, y in directions):
                    # ...calculate the coordinates of the sequare to move to
                    new_point = (elf[0] + directions[0][0], elf[1] + directions[0][1])

                    # Add the elf to `moves`
                    moves.setdefault(new_point, []).append(elf)
                    break

        # Filter from `moves` the squares where more than one elf wants to move
        # to the same square
        moves = {k: v for k, v in moves.items() if len(v) == 1}

        # Move each elf to the new square
        for k, v in moves.items():
            # `v` will contain only one item
            elves.remove(v[0])
            elves.add(k)

        # Change the order of the directions
        all_directions = all_directions[1:] + all_directions[:1]

    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    # Work out the minimum and maximum coordinates of the elves
    for x, y in elves:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    # Calculate the total number of unoccupied squares within the rectangle
    total = (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)

    print(total)


def part_two(input: str):
    elves: set[tuple[int, int]] = set()

    # Iterate through the grid input
    for i, row in enumerate(input.splitlines()):
        for j, col in enumerate(row):
            if col == '#':
                # Add the elf into the set
                # Coordinates: →x , ↑y
                elves.add((j, -i))

    # The directions to check
    # The first item in each sub-list is the direction to move if all spaces
    # are free (e.g. move N if N, NW and NE are all free)
    all_directions: list[list[tuple[int, int]]] = [
        [(0, 1), (-1, 1), (1, 1)],
        [(0, -1), (-1, -1), (1, -1)],
        [(-1, 0), (-1, 1), (-1, -1)],
        [(1, 0), (1, 1), (1, -1)]
    ]

    total = 0

    while True:
        # Increment the counter on each loop
        total += 1

        elves_to_move: list[tuple[int, int]] = []

        for elf in elves:
            # Get adjacent squares
            adjacents = get_adjacents(*elf)

            # If any adjacent square is occupied, then the elf can potentially move
            if any(square in elves for square in adjacents):
                elves_to_move.append(elf)

        # `moves` is a dict where each key is the coordinates of a square, and
        # the value is a list of elves that want to move into that square
        moves: dict[tuple[int, int], list[tuple[int, int]]] = {}

        for elf in elves_to_move:
            for directions in all_directions:
                # If all adjacent squares in `directions` are empty...
                if all((elf[0] + x, elf[1] + y) not in elves for x, y in directions):
                    # ...calculate the coordinates of the sequare to move to
                    new_point = (elf[0] + directions[0][0], elf[1] + directions[0][1])

                    # Add the elf to `moves`
                    moves.setdefault(new_point, []).append(elf)
                    break

        # Filter from `moves` the squares where more than one elf wants to move
        # to the same square
        moves = {k: v for k, v in moves.items() if len(v) == 1}

        # If there are no elves to move, break from the loop
        if len(moves) == 0:
            break

        # Move each elf to the new square
        for k, v in moves.items():
            # `v` will contain only one item
            elves.remove(v[0])
            elves.add(k)

        # Change the order of the directions
        all_directions = all_directions[1:] + all_directions[:1]

    print(total)


with open('input.txt') as f:
    input = f.read()


part_one(input)
part_two(input)
