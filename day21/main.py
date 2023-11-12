class Monkey:
    """Each monkey is a node in a binary tree"""

    def __init__(self, name: str, value: str) -> None:
        self.name = name

        if value.isnumeric():
            self.value = int(value)
            self.left = self.right = None
        else:
            left, operator, right = value.split(' ')
            self.value = operator
            self.left = left
            self.right = right


def part_one(input: str):
    # dict containing each monkey, by name
    monkeys: dict[str, Monkey] = {}

    # Create a monkey object for each line in the file
    for line in input.splitlines():
        name, job = line.split(': ')
        monkeys[name] = Monkey(name, job)

    def recurse(name: str) -> int:
        """Recursive function to calculate the binary tree"""

        monkey = monkeys[name]

        # If leaf node, return the value
        if isinstance(monkey.value, int):
            return monkey.value

        assert monkey.left and monkey.right

        # Otherwise, recurse on both sides and perform operation according to
        # the operator
        left, right, operator = monkey.left, monkey.right, monkey.value

        match operator:
            case '+':
                return recurse(left) + recurse(right)
            case '-':
                return recurse(left) - recurse(right)
            case '*':
                return recurse(left) * recurse(right)
            case '/':
                return recurse(left) // recurse(right)
            case _:
                raise Exception(f'Invalid operator: {operator}')

    # Recurse from the root of the tree
    result = recurse('root')

    print(result)


def part_two(input: str):
    # dict containing each monkey, by name
    monkeys: dict[str, Monkey] = {}

    # Create a monkey object for each line in the file
    for line in input.splitlines():
        name, job = line.split(': ')
        monkeys[name] = Monkey(name, job)

    # `path_to_humn` will be a set containing all nodes on the way to the
    # `humn` node
    path_to_humn: set[str] = set()

    # dict for each non-leaf node, where the value is a tuple of the left and
    # right operands
    values: dict[str, tuple[int, int]] = {}

    def calculate_values(name: str, path: set[str]) -> int:
        """
        Recursive function to:
          calculate the operands of each non-leaf node
          obtain the path from the root node to the `humn` node
        """
        nonlocal path_to_humn

        monkey = monkeys[name]

        # Add the current node to the path
        path.add(name)

        # If we are at the `humn` node, save the path
        if monkey.name == 'humn':
            path_to_humn = path

        if isinstance(monkey.value, int):
            return monkey.value

        assert monkey.left and monkey.right

        left, right, operator = monkey.left, monkey.right, monkey.value

        # Obtain the left and right operands recursively
        left_operand, right_operand = calculate_values(left, path.copy()), calculate_values(right, path.copy())

        # Save the operands in the `values` dict
        values[name] = (left_operand, right_operand)

        match operator:
            case '+':
                return left_operand + right_operand
            case '-':
                return left_operand - right_operand
            case '*':
                return left_operand * right_operand
            case '/':
                return left_operand // right_operand
            case _:
                raise Exception(f'Invalid operator: {operator}')

    # Call the `calculate_values` function to initialise the `path_to_humn` and
    # `values` variables correctly
    calculate_values('root', set())

    # `humn` will contain the correct value for the `humn` node
    humn = 0

    def find_humn(name: str, result) -> None:
        nonlocal humn

        monkey = monkeys[name]

        # If we have found the `humn` node, we can set `humn` and return
        if name == 'humn':
            humn = result
            return

        assert isinstance(monkey.value, str) and monkey.left and monkey.right

        left, right, operator = monkey.left, monkey.right, monkey.value
        left_operand, right_operand = values[name]

        # The operand of the side of the current node which contains `humn`
        # needs to equal `result` in order for both sides of the full tree
        # to have the same value
        match operator:
            case '+':
                # left_operand + right_operand = result
                if left in path_to_humn:
                    return find_humn(left, result - right_operand)

                return find_humn(right, result - left_operand)
            case '-':
                # left_operand - right_operand = result
                if left in path_to_humn:
                    return find_humn(left, result + right_operand)

                return find_humn(right, left_operand - result)
            case '*':
                # left_operand * right_operand = result
                if left in path_to_humn:
                    return find_humn(left, result // right_operand)

                return find_humn(right, result // left_operand)
            case '/':
                # left_operand / right_operand = result
                if left in path_to_humn:
                    return find_humn(left, result * right_operand)

                return find_humn(right, left_operand // result)
            case _:
                raise Exception(f'Invalid operator: {operator}')

    root_monkey = monkeys['root']

    assert root_monkey.left and root_monkey.right

    left_operand, right_operand = values['root']

    # If the left side of the tree contains `humn`, then the left side of the
    # tree needs to equal the right side (solve for `humn` on the left)
    if root_monkey.left in path_to_humn:
        find_humn(root_monkey.left, right_operand)
    else:
        # Otherwise, the right side needs to equal the left side (solve for
        # `humn` on the right)
        find_humn(root_monkey.right, left_operand)

    print(humn)


with open('input.txt') as f:
    input = f.read()


part_one(input)
part_two(input)
