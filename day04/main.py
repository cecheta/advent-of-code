def part_one(input: str):
    array = input.splitlines()

    total = 0

    for line in array:
        # Find the two intervals
        interval1, interval2 = line.split(',')

        # Find the left and right values of each interval
        left1, right1 = interval1.split('-')
        left2, right2 = interval2.split('-')

        # There are two scenarios to consider:
        #
        # 1  -----------           -----
        # 2    --------         -----------
        if (int(left1) <= int(left2) <= int(right2) <= int(right1)) or (int(left2) <= int(left1) <= int(right1) <= int(right2)):
            total += 1

    print(total)


def part_two(input: str):
    array = input.splitlines()

    total = 0

    for line in array:
        # Find the two intervals
        interval1, interval2 = line.split(',')

        # Find the left and right values of each interval
        left1, right1 = interval1.split('-')
        left2, right2 = interval2.split('-')

        # There are two scenarios to consider:
        #
        # 1  -----------                  -----
        # 2        --------       -----------
        if (int(left1) <= int(left2) <= int(right1)) or (int(left2) <= int(left1) <= int(right2)):
            total += 1

    print(total)


with open('input.txt') as f:
    input = f.read()

part_one(input)
part_two(input)
