def part_one(input: str):
    moves = input.splitlines()

    # Initialise variables
    total = 0
    X = cycle = 1

    for move in moves:
        line = move.split(' ')
        op = line[0]

        # Increment the current cycle
        cycle += 1

        # If this is an "interesting cycle", calculate the signal strength and
        # add it to the running total
        if cycle % 40 == 20:
            total += cycle * X

        # If the operation is 'addx', then add the value to `X`, and increment
        # the current cycle
        if op == 'addx':
            cycle += 1
            X += int(line[1])

            # Check again for "interesting cycle"
            if cycle % 40 == 20:
                total += cycle * X

    print(total)


def part_two(input: str):
    def crt_print(position: int, X: int) -> int:
        """
        Function to print character on the screen depending on the position of
        the sprite
        """

        if X - 1 <= position <= X + 1:
            # If the position of the pixel is between the sprite, draw '#'
            print('#', end='')
        else:
            # Otherwise, draw '.'
            print('.', end='')

        # Move the pixel to the next position
        position += 1

        # If the pixel is out of bounds, reset to the start and draw a new line
        if position == 40:
            position = 0
            print()

        return position

    moves = input.splitlines()

    X = 1
    position = 0

    for move in moves:
        line = move.split(' ')
        op = line[0]

        position = crt_print(position, X)

        if op == 'addx':
            position = crt_print(position, X)
            X += int(line[1])


with open('input.txt') as f:
    input = f.read()

part_one(input)
print()
part_two(input)
