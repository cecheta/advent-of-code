def get_priority(letter: str) -> int:
    """
    Function to obtain priority of a letter
    ord() is used to obtain ascii value

    a-z: 97 - 122
    A-Z: 65 - 90

    ascii values are converted to a priority

    a-z: 1 - 26
    A-Z: 27 - 52
    """

    if letter.islower():
        return ord(letter) - 96

    return ord(letter) - 38


def part_one(input: str):
    array = input.splitlines()

    total = 0

    for line in array:
        mid = len(line) // 2

        # Split each line into two halves
        left, right = line[:mid], line[mid:]

        # Turn the left string into a set, so characters can be found immediately
        left_set = set(list(left))

        for char in right:
            if char in left_set:
                # If the character from the right half is present in the left set, it is a duplicate
                duplicate = char
                break

        total += get_priority(duplicate)

    print(total)


def part_two(input: str):
    array = input.splitlines()

    total = 0

    # Iterate through the input in chunks of 3
    for i in range(0, len(array), 3):
        one, two, three = array[i], array[i + 1], array[i + 2]

        # Turn the second and third strings into sets, so characters can be found immediately
        set_two, set_three = set(two), set(three)

        for char in one:
            if char in set_two and char in set_three:
                # If the character is present in all three, add its priority
                total += get_priority(char)
                break

    print(total)


with open('input.txt') as f:
    input = f.read()

part_one(input)
part_two(input)
