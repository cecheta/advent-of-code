import ast
from functools import cmp_to_key
from typing import Union


Packet = list[Union[int, 'Packet']]


def compare(left_arr: Packet, right_arr: Packet) -> int:
    """Comparator function to determine order of packets"""
    i = 0

    while i < len(left_arr) and i < len(right_arr):
        # Iterate through both lists together
        left, right = left_arr[i], right_arr[i]

        # Iff both values are integers, compare them directly
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return -1
            if right < left:
                return 1
            # If `left` and `right` are the same, move on to the next items
        else:
            # Convert any integer into a list (both may already be lists)
            if isinstance(left, int):
                left = [left]
            if isinstance(right, int):
                right = [right]

            # Compare the two lists recursively
            check = compare(left, right)

            # If `check` is not 0, then the lists are not equal, therefore
            # return this value
            if check != 0:
                return check
            # If the lists are the same, move on to the next items

        i += 1

    # If we have reached here, then we have fully iterated through one (or
    # both) of the lists
    if len(left_arr) == len(right_arr):
        # If the lengths are the same, then the lists are equal
        return 0
    if i < len(right_arr):
        # If we haven't iterated fully through the right array, then the left
        # array is smaller and comes first
        return -1

    # Otherwise, the right array comes first
    return 1


def part_one(input: str):
    arr = input.strip().split('\n\n')

    result = 0

    for i, pair in enumerate(arr):
        left, right = pair.splitlines()

        # Evalue the pair of packets as string literals
        left_arr: Packet = ast.literal_eval(left)
        right_arr: Packet = ast.literal_eval(right)

        # If `left_arr` comes before `right_arr`, the `compare` function
        # will return -1
        if compare(left_arr, right_arr) == -1:
            # Add the index (1-based) to the result
            result += i + 1

    print(result)


def part_two(input: str):
    # Parse the string literal for each line in the input (that isn't blank)
    packets: list[Packet] = [ast.literal_eval(line) for line in input.splitlines() if line != '']

    # Add the divider packets
    packets.extend([[[2]], [[6]]])

    # Sort, using the custom `compare` function
    packets.sort(key=cmp_to_key(compare))

    result = 1

    for i, packet in enumerate(packets):
        # If we have a divider packet, multiply the index (1-based) to the result
        if packet == [[2]] or packet == [[6]]:
            result *= (i + 1)

    print(result)


with open('input.txt') as f:
    input = f.read()


part_one(input)
part_two(input)
