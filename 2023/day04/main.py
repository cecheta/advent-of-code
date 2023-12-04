import os
import re


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    result = 0

    for line in array:
        match = re.search(r"^.*:(.*)\|(.*)$", line)
        assert match is not None

        winning_numbers = set(match.group(1).split())
        my_numbers = match.group(2).split()

        score = 0

        for number in my_numbers:
            if number in winning_numbers:
                if score == 0:
                    score = 1
                else:
                    score *= 2

        result += score

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    cards: dict[int, int] = {}

    for line in array:
        match = re.search(r"^.*?(\d+):(.*)\|(.*)$", line)
        assert match is not None

        id = int(match.group(1))
        winning_numbers = set(match.group(2).split())
        my_numbers = list(match.group(3).split())

        cards[id] = cards.get(id, 0) + 1

        i = 1

        for number in my_numbers:
            if number in winning_numbers:
                cards[id + i] = cards.get(id + i, 0) + cards[id]
                i += 1

    result = sum(cards.values())
    print(result)

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
