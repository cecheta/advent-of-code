import os
import re


def change_direction(direction: str, turn: str) -> str:
    """Function to return the new direction after turning"""
    match direction:
        case 'R':
            return 'D' if turn == 'R' else 'U'
        case 'D':
            return 'L' if turn == 'R' else 'R'
        case 'L':
            return 'U' if turn == 'R' else 'D'
        case 'U':
            return 'R' if turn == 'R' else 'L'
        case _:
            raise Exception(f'Invalid direction: {direction}')


def get_coordinates(direction: str) -> tuple[int, int]:
    """Function to convert a direction string into coordinates"""
    match direction:
        case 'R':
            return (0, 1)
        case 'D':
            return (1, 0)
        case 'L':
            return (0, -1)
        case 'U':
            return (-1, 0)
        case _:
            raise Exception(f'Invalid direction: {direction}')


def get_direction_score(direction: str) -> int:
    """Function to return a score for facing a certain direction"""
    match direction:
        case 'R':
            return 0
        case 'D':
            return 1
        case 'L':
            return 2
        case 'U':
            return 3
        case _:
            raise Exception(f'Invalid direction: {direction}')


def part_one(input: str):
    def move(position: tuple[int, int], board: list[list[str]], moves: int, direction: str) -> tuple[int, int]:
        """Function to make a number of moves in a certain direction"""
        height, width = len(board), len(board[0])

        coordinates = get_coordinates(direction)

        for _ in range(moves):
            # Save the current position in case we are blocked
            current_position = position

            # Obtain the new coordinates, wrapping around the board
            position = ((position[0] + coordinates[0]) % height, (position[1] + coordinates[1]) % width)

            # If the square does not have '.', then...
            while board[position[0]][position[1]] != '.':
                # ...either we are blocked, in which case we stop moving...
                if board[position[0]][position[1]] == '#':
                    return current_position

                # ...orr we are outside of the board (but still within the
                # array), in which case we keep moving until we are back on
                # the board
                position = ((position[0] + coordinates[0]) % height, (position[1] + coordinates[1]) % width)

        # Return after making all the moves (unless we returned early due to
        # being blocked)
        return position

    board_string, path = input.strip('\n').split('\n\n')

    board = [list(line) for line in board_string.splitlines()]

    width = max(len(row) for row in board)

    # Ensure each row in the array is the same length, by filling with ' '
    for row in board:
        row += [' '] * (width - len(row))

    instructions: list[str] = re.findall(r'(\d+|\w)', path)

    # The starting position is the first '.' in the first row of the board
    position = (0, board[0].index('.'))

    # We start facing to the right
    direction = 'R'

    for instruction in instructions:
        # Each instruction is either a number of steps to make, or a rotation
        if instruction.isnumeric():
            # Obtain the new position after moving
            position = move(position, board, int(instruction), direction)
        else:
            # Change the direction being faced
            direction = change_direction(direction, instruction)

    # Obtain the final row, column, and points for the direction being faced
    row, column, facing = position[0] + 1, position[1] + 1, get_direction_score(direction)

    # Calculate the password
    password = (1000 * row) + (4 * column) + facing

    print(password)


def part_two(input: str):
    def move(position: tuple[int, int], board: list[list[str]], moves: int, direction: str) -> tuple[tuple[int, int], str]:
        """Function to make a number of moves in a certain direction"""
        for _ in range(moves):
            current_position, current_direction = position, direction

            # Save the current position in case we are blocked
            coordinates = get_coordinates(direction)

            x, y = ((position[0] + coordinates[0]), (position[1] + coordinates[1]))

            # The following is hard-coded logic to determing the position and
            # direction after walking across an edge of the cube. This logic is
            # specific to the puzzle input that was provided.
            if x == -1 and 50 <= y < 100:
                x, y, direction = y + 100, 0, 'R'
            elif x == -1 and 100 <= y < 150:
                x, y, direction = 199, y - 100, 'U'
            elif 0 <= x < 50 and y == 150:
                x, y, direction = 149 - x, 99, 'L'
            elif x == 50 and 100 <= y < 150 and direction == 'D':
                x, y, direction = y - 50, 99, 'L'
            elif 50 <= x < 100 and y == 100 and direction == 'R':
                x, y, direction = 49, x + 50, 'U'
            elif 100 <= x < 150 and y == 100:
                x, y, direction = 149 - x, 149, 'L'
            elif x == 150 and 50 <= y < 100 and direction == 'D':
                x, y, direction = y + 100, 49, 'L'
            elif 150 <= x < 200 and y == 50 and direction == 'R':
                x, y, direction = 149, x - 100, 'U'
            elif x == 200 and 0 <= y < 50:
                x, y, direction = 0, y + 100, 'D'
            elif 150 <= x < 200 and y == -1:
                x, y, direction = 0, x - 100, 'D'
            elif 100 <= x < 150 and y == -1:
                x, y, direction = 149 - x, 50, 'R'
            elif x == 99 and 0 <= y < 50 and direction == 'U':
                x, y, direction = y + 50, 50, 'R'
            elif 50 <= x < 100 and y == 49 and direction == 'L':
                x, y, direction = 100, x - 50, 'D'
            elif 0 <= x < 50 and y == 49:
                x, y, direction = 149 - x, 0, 'R'

            # If we are blocked then stop moving
            if board[x][y] == '#':
                return current_position, current_direction

            position = (x, y)

        # Return after making all the moves (unless we returned early due to
        # being blocked)
        return position, direction

    board_string, path = input.strip('\n').split('\n\n')

    board = [list(line) for line in board_string.splitlines()]

    width = max(len(row) for row in board)

    # Ensure each row in the array is the same length, by filling with ' '
    for row in board:
        row += [' '] * (width - len(row))

    instructions: list[str] = re.findall(r'(\d+|\w)', path)

    # The starting position is the first '.' in the first row of the board
    position = (0, board[0].index('.'))

    # We start facing to the right
    direction = 'R'

    for instruction in instructions:
        # Each instruction is either a number of steps to make, or a rotation
        if instruction.isnumeric():
            # Obtain the new position and direction after moving
            position, direction = move(position, board, int(instruction), direction)
        else:
            # Change the direction being faced
            direction = change_direction(direction, instruction)

    # Obtain the final row, column, and points for the direction being faced
    row, column, facing = position[0] + 1, position[1] + 1, get_direction_score(direction)

    # Calculate the password
    password = (1000 * row) + (4 * column) + facing

    print(password)


with open('input.txt') as f:
    input = f.read()


part_one(input)
part_two(input)
