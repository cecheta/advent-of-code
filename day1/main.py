import heapq


def part_one(input: str):
    # Remove trailing whitespace from file, then split at each double new line
    array = input.strip('\n').split('\n\n')

    # `maximum` will hold the largest sub array total
    maximum = -1

    for item in array:
        # For each set of numbers in the array, find the total (as integers, not strings)
        sub_arr = item.split('\n')
        total = sum(int(i) for i in sub_arr)

        # if `total` is larger than the current `maximum`, then replace `maximum` with the new value
        maximum = max(maximum, total)

    print(maximum)


def part_two(input: str):
    # Remove trailing whitespace from file, then split at each double new line
    array = input.strip('\n').split('\n\n')

    # `totals` will hold the total of each sub array totals
    totals: list[int] = []

    for item in array:
        # For each set of numbers in the array, find the total (as integers, not strings)
        sub_arr = item.split('\n')
        total = sum(int(i) for i in sub_arr)

        totals.append(total)

    # Sort the `totals` array, largest first
    totals.sort(reverse=True)

    # `result` is the sum of the first three items in the array
    result = sum(totals[:3])

    print(result)


def part_twoHeap(input: str):
    # Remove trailing whitespace from file, then split at each double new line
    array = input.strip('\n').split('\n\n')

    # We can use `heap` to only hold the three largest subarrays
    heap: list[int] = []

    for item in array:
        # For each set of numbers in the array, find the total (as integers, not strings)
        sub_arr = item.split('\n')
        total = sum(int(i) for i in sub_arr)

        if len(heap) < 3:
            # If there are less than three items in the heap, just add the item to the heap
            heapq.heappush(heap, total)
        else:
            # Otherwise, add the total to the heap, and pop the smallest item
            heapq.heappushpop(heap, total)

    # `heap` now holds the three largest items, therefore the sum is the result
    result = sum(heap)

    print(result)


with open('input.txt') as f:
    input = f.read()

part_one(input)
part_two(input)
part_twoHeap(input)
