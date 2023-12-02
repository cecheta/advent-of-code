import re


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    amounts = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    result = 0

    for line in array:
        # Extract the game ID and the game results
        match = re.search(r"^Game (\d+): (.*)$", line)
        id = int(match.group(1))
        game = match.group(2)

        for draw in game.split('; '):
            for cubes in draw.split(', '):
                # Get the colour and number of the cubes
                number, colour = cubes.split(' ')

                # If there are too many cubes, the game is invalid, therefore break
                if int(number) > amounts[colour]:
                    break
            else:
                # If we reach here, the draw is valid, therefore move on to the next draw
                continue

            # If we reach here, the draw was invalid, therefore break out of the loop
            # and move on to the next game
            break
        else:
            # If we reach here, each draw was valid, therefore add the ID
            result += id

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    result = 0

    for line in array:
        match = re.search(r"^Game (\d+): (.*)$", line)
        id = int(match.group(1))
        game = match.group(2)

        # Initialise the number of cubes seen for each colour
        minimums = {
            'red': 0,
            'green': 0,
            'blue': 0,
        }

        for draw in game.split('; '):
            for cubes in draw.split(', '):
                number, colour = cubes.split(' ')

                # Set the new value if the number of cubes is larger
                # than what we have seen so far
                minimums[colour] = max(minimums[colour], int(number))

        # Multiply the number of cubes together to calculate the power
        power = minimums['red'] * minimums['green'] * minimums['blue']

        # Add the power to the result
        result += power

    print(result)


with open('input.txt') as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
