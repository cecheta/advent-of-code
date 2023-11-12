def find_marker(input: str, length: int) -> int:
    result = -1

    # `seen` is a dict containing each character that has been seen and the index where it was seen
    seen: dict[str, int] = {}

    # Iterate through the string
    for i, char in enumerate(input):
        # If the character has been seen before...
        if char in seen:
            prev_index = seen[char]

            # ...remove every character before it from `seen`
            for key, value in list(seen.items()):
                if value < prev_index:
                    del seen[key]

        # Add the character into `seen` at its index
        seen[char] = i

        # If we've seen enough characters, return the result
        if len(seen) == length:
            result = i + 1
            break

    return result


def part_one(input: str):
    result = find_marker(input, 4)
    print(result)


def part_two(input: str):
    result = find_marker(input, 14)
    print(result)


with open('input.txt') as f:
    input = f.read()

part_one(input)
part_two(input)
