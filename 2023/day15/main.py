import os
import re


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().split(",")

    result = 0

    for step in array:
        total = 0

        for char in step:
            # ord() gives the ASCII value for a character
            ascii = ord(char)

            total += ascii
            total *= 17
            total %= 256

        result += total

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().split(",")

    def hash(chars: str) -> int:
        """
        Function to calculate hash of string.
        Same calculation as in Part 1, but now moved to its own function.
        """

        total = 0

        for char in chars:
            ascii = ord(char)

            total += ascii
            total *= 17
            total %= 256

        return total

    # A dict where the key is the box number and the value is a list of the lenses
    # in the box. Each lens is a tuple of the lens label and focal length
    boxes: dict[int, list[tuple[str, int]]] = {}

    for step in array:
        # Extract the information from the step
        match = re.match(r"^(\w+)([=-])(\d*)$", step)
        assert match is not None

        label, operation, focal_length = match.groups()

        # Hash the label to find the correct box number
        box = hash(label)

        # If we have not seen this box before, add it to the dict
        if box not in boxes:
            boxes[box] = []

        # Get the list of slots from the box
        slots = boxes[box]

        if operation == "-":
            for i, (slot_label, _) in enumerate(slots):
                # If we find a lens with the same label, remove it from the list
                # All other lenses after the removed lens will be shifted up
                # one space
                if slot_label == label:
                    del slots[i]
                    break
        else:
            focal_length = int(focal_length)

            for i, (slot_label, _) in enumerate(slots):
                # If a lens with the same label is already present in the box,
                # replace it with the new lens
                if slot_label == label:
                    slots[i] = (label, focal_length)
                    break
            else:
                # If we reach here, we did not find any lens in the box with the
                # same label, therefore add the new lens to the end of the list
                slots.append((label, focal_length))

    result = 0

    for number, slots in boxes.items():
        for i, (_, focal_length) in enumerate(slots):
            # Calculate the focusing power of each lens
            result += (number + 1) * (i + 1) * focal_length

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
