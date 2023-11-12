def part_one(input: str):
    total = 0

    for line in input.splitlines():
        for i, char in enumerate(line[::-1]):
            match char:
                case '=':
                    val = -2
                case '-':
                    val = -1
                case _:
                    val = int(char)

            total += (5 ** i) * val

    def recurse(total: int, snafu: str, i: int) -> str:
        if i == 0:
            return snafu

        difference = (5 ** (i - 1)) // 2

        if -2 * (5 ** (i - 1)) - difference <= total <= -2 * (5 ** (i - 1)) + difference:
            return recurse(total + 2 * (5 ** (i - 1)), f'{snafu}=', i - 1)
        if -(5 ** (i - 1)) - difference <= total <= -(5 ** (i - 1)) + difference:
            return recurse(total + (5 ** (i - 1)), f'{snafu}-', i - 1)
        if -difference <= total <= difference:
            return recurse(total, f'{snafu}0', i - 1)
        if (5 ** (i - 1)) - difference <= total <= (5 ** (i - 1)) + difference:
            return recurse(total - (5 ** (i - 1)), f'{snafu}1', i - 1)
        if 2 * (5 ** (i - 1)) - difference <= total <= 2 * (5 ** (i - 1)) + difference:
            return recurse(total - 2 * (5 ** (i - 1)), f'{snafu}2', i - 1)

        raise Exception('Invalid calculation')

    i = 1

    while not -((5 ** i) // 2) <= total <= (5 ** i) // 2:
        i += 1

    result = recurse(total, '', i)

    print(result)


def part_two(input: str):
    pass


with open('input.txt') as f:
    input = f.read()

part_one(input)
part_two(input)
