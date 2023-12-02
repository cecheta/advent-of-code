def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    result = 0

    for line in array:
        num1 = num2 = None

        for char in line:
            # Look for the first digit in the sequence
            if char.isdigit():
                num1 = char
                break

        for char in line[::-1]:
            # Reverse the string, then look for the first digit in the sequence
            if char.isdigit():
                num2 = char
                break

        if num1 is None or num2 is None:
            raise Exception

        result += int(num1 + num2)

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    numbers = {
        'zero': '0',
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }

    result = 0

    for line in array:
        num1 = num2 = None

        for i, char in enumerate(line):
            # Check to see if the character is a digit
            if char.isdigit():
                num1 = char
                break

            # If not, check to see whether a 3, 4 or 5-letter word spells a number,
            # by checking for the word in the `numbers` dict
            for n in range(3, 6):
                word = line[i:i + n]

                if word in numbers:
                    # Get the value of the number from the dict
                    num1 = numbers[word]
                    break
            else:
                # This code only runs if we did not break out of the loop, meaning
                # that `num1` has not been found yet and we should continue to the next character
                continue

            # If we have broken out of the inner loop, then we have found `num1` and should
            # also break out of the outer loop
            break

        # Loop through the sequence in reverse
        for i, char in enumerate(line[::-1]):
            if char.isdigit():
                num2 = char
                break

            for n in range(3, 6):
                # Take `word` from the original character sequence `line`, which
                # is in the correct order
                word = line[len(line) - i - n:len(line) - i]

                if word in numbers:
                    num2 = numbers[word]
                    break
            else:
                continue

            break

        if num1 is None or num2 is None:
            raise Exception

        result += int(num1 + num2)

    print(result)

with open('input.txt') as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
