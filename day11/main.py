import re
from functools import reduce
from typing import Optional


class Monkey:
    inspects: int
    number: int
    items: list[int]
    operation: str
    test: int
    true: int
    false: int

    def __init__(self, text: str):
        """Extract all values from the input, and set the instance variables"""
        match = re.search(r'''^Monkey (\d+):
  Starting items: (.*)
  Operation: new = (.*)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)$''', text, re.DOTALL)

        assert match is not None

        groups = match.groups()

        # The number of times the monkey has inspected an item
        self.inspects = 0

        # The index of the monkey
        self.number = int(groups[0])

        # A list of the items the monkey currently has
        self.items = list(map(int, groups[1].split(', ')))

        # A string of the monkey operation
        self.operation = groups[2]

        # The number to check if the worry is divisible by
        self.test = int(groups[3])

        # The index of the monkey to pass to if the test passes
        self.true = int(groups[4])

        # The index of the monkey to pass to if the test fails
        self.false = int(groups[5])

    def add_item(self, item: int):
        """Add an item to the monkey's list of items"""
        self.items.append(item)

    def reset_items(self):
        """Remove all the items from the monkey"""
        self.items.clear()

    def next(self, worry: int, mod: Optional[int] = None, relief: Optional[int] = None) -> tuple[int, int]:
        # Increment whenever a monkey inspects a new item
        self.inspects += 1

        # UNSAFE - Evaluate the expression (e.g. 'old * 19'), setting `old` to
        # the value of `worry`
        new_worry = eval(self.operation, {'__builtins__': None}, {'old': worry})

        # For part 1, divide the new worry by the 'relief factor'
        if relief is not None:
            new_worry //= relief

        # For part 2, obtain the modulo of the worry, to prevent the worry from
        # becoming excessively large
        if mod is not None:
            new_worry %= mod

        # If the worry is divisible by the test, then return the 'true' monkey
        # index, along with the new worry value
        if new_worry % self.test == 0:
            return (self.true, new_worry)

        # Otherwise, return the 'false' monkey index, along with the new
        # worry value
        return (self.false, new_worry)


def part_one(input: str):
    # Split the input text at each double new line
    input_arr = input.strip('\n').split('\n\n')

    # Create the Monkey objects
    monkeys = [Monkey(text) for text in input_arr]

    # Loop n times
    for _ in range(20):
        # Loop for each monkey in order
        for monkey in monkeys:
            # Loop through all the items the monkey currently has
            for item in monkey.items:
                # Calculate the next monkey to pass to, as well as the new
                # worry value after the monkey has inspected it
                next_monkey, worry = monkey.next(item, relief=3)

                # Add the item to the next monkey's list
                monkeys[next_monkey].add_item(worry)

            # After processing all the items the monkey has, reset to
            # an empty list
            monkey.reset_items()

    # Sort the monkeys by how many times each monkey processed an
    # item, largest first
    sorted_monkeys = sorted(monkeys, key=lambda x: x.inspects, reverse=True)

    # Multiply the number of inspects of the first two monkeys
    result = sorted_monkeys[0].inspects * sorted_monkeys[1].inspects

    print(result)


def part_two(input: str):
    # Split the input text at each double new line
    monkey_input = input.strip('\n').split('\n\n')

    # Create the Monkey objects
    monkeys = [Monkey(monkey) for monkey in monkey_input]

    # To prevent the worry levels from becoming too large, we can find the
    # common denominator of all the monkeys' test values, by multiplying all
    # the values together.
    # When calculating the next worry value, we can use the remainder after
    # dividing the value by the common denominator (modulo operation).
    mod = reduce(lambda x, y: x * y.test, monkeys, 1)

    # Loop n times
    for _ in range(10000):
        # Loop for each monkey in order
        for monkey in monkeys:
            # Loop through all the items the monkey currently has
            for item in monkey.items:
                # Calculate the next monkey to pass to, as well as the new
                # worry value after the monkey has inspected it
                next_monkey, worry = monkey.next(item, mod=mod)

                # Add the item to the next monkey's list
                monkeys[next_monkey].add_item(worry)

            # After processing all the items the monkey has, reset to
            # an empty list
            monkey.reset_items()

    # Sort the monkeys by how many times each monkey processed an
    # item, largest first
    sorted_monkeys = sorted(monkeys, key=lambda x: x.inspects, reverse=True)

    # Multiply the number of inspects of the first two monkeys
    result = sorted_monkeys[0].inspects * sorted_monkeys[1].inspects

    print(result)


with open('input.txt') as f:
    input = f.read()

part_one(input)
part_two(input)
