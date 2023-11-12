# Node within doubly-linked list
class Node():
    left: 'Node'
    right: 'Node'

    def __init__(self, val: int) -> None:
        self.val = val


def calculate(input: str, *, decryption_key=1, mixes=1):
    # Parse input into a list of nodes
    nodes = list(map(lambda x: Node(int(x) * decryption_key), input.splitlines()))

    n = len(nodes)

    zero_index = -1

    # Create circular doubly-linked list of nodes
    for i, node in enumerate(nodes):
        node.left = nodes[i - 1]
        node.right = nodes[(i + 1) % n]

        # Keep track of the index of the node with a value of 0
        if node.val == 0:
            zero_index = i

    for _ in range(mixes):
        # Loop through the nodes in the original order
        for node in nodes:
            # Remove the node from its current position
            node.left.right = node.right
            node.right.left = node.left

            # Work out how many spaces the node needs to move forwards or backwards
            moves = (abs(node.val) % (len(nodes) - 1)) * (node.val // abs(node.val)) if node.val != 0 else 0

            # `anchor` will be the node to the left of where `node` will be re-inserted
            anchor = node.left

            while moves != 0:
                if moves > 0:
                    anchor = anchor.right
                else:
                    anchor = anchor.left

                moves -= (1 if moves > 0 else -1)

            # Insert the node to the right of `anchor`
            anchor.right.left = node
            node.right = anchor.right
            anchor.right = node
            node.left = anchor

    total = 0

    # Start from the node with a value of 0
    node = nodes[zero_index]

    for i in range(1, 3001):
        node = node.right

        # Add the grove coordinates
        if i % 1000 == 0:
            total += node.val

    return total


def part_one(input: str):
    result = calculate(input)

    print(result)


def part_two(input: str):
    result = calculate(input, decryption_key=811589153, mixes=10)

    print(result)


with open('input.txt') as f:
    input = f.read()


part_one(input)
part_two(input)
