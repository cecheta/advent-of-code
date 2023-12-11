import os


def part_one(puzzle_input: str) -> None:
    def recurse(numbers: list[int]) -> int:
        """
        Recursive function to return the next value for a particular row
        """

        # Base case: The row is full of 0's therefore return 0
        if all(num == 0 for num in numbers):
            return 0

        next_numbers = []

        # Calculate the difference between each number and the number before,
        # add to `next_numbers` list
        for i in range(1, len(numbers)):
            next_numbers.append(numbers[i] - numbers[i - 1])

        # Call the function recursively with the next row of numbers
        value = recurse(next_numbers)

        # The value we receive is the difference that should be added to the
        # last value in the current row
        return numbers[-1] + value

    array = puzzle_input.strip().splitlines()

    result = 0

    # Iterate through the rows in the puzzle input
    for line in array:
        # Transform the string into a list of integers
        numbers = list(map(int, line.split(" ")))

        # Call the recursive function, add the return value to the final result
        result += recurse(numbers)

    print(result)


def part_two(puzzle_input: str) -> None:
    def recurse(numbers: list[int]) -> int:
        """
        The function is the same as in Part 1, except the value from the recursive
        function is now subtracted from the first value in the current row
        """

        if all(num == 0 for num in numbers):
            return 0

        next_numbers = []

        for i in range(1, len(numbers)):
            next_numbers.append(numbers[i] - numbers[i - 1])

        value = recurse(next_numbers)

        # Subtract the recursive function's return value from the first value in
        # the current row
        return numbers[0] - value

    array = puzzle_input.strip().splitlines()

    result = 0

    for line in array:
        numbers = list(map(int, line.split(" ")))

        result += recurse(numbers)

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
