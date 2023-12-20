import math
import os


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    # The list of destination modules from the broadcaster
    broadcaster: list[str] = []

    # Dicts of flip-flop and conjuction modules, where the key is the module name
    # and the value is a list of destination modules
    flip_flops: dict[str, list[str]] = {}
    conjunctions: dict[str, list[str]] = {}

    # Dict for flip-flop modules where the key is the module name and the value is
    # the module's current state (False - off, True - on)
    states: dict[str, bool] = {}

    # Dict for conjuction modules where the key is the module name and the value is
    # a dict containing all input modules that point to this conjuction module. The key
    # is the name of the module and the value is the last known state of the input
    # module
    memory: dict[str, dict[str, bool]] = {}

    for line in array:
        # Parse the module's name and destination modules from the puzzle input
        name, destinations = line.split(" -> ")
        destinations = destinations.split(", ")

        if name == "broadcaster":
            # Save the broadcaster destintaion modules separately
            broadcaster = destinations
        else:
            # The first character is the prefix
            prefix, name = name[0], name[1:]

            if prefix == "%":
                # Flip-flop module
                flip_flops[name] = destinations

                # All flip-flop modules start in the off state
                states[name] = False
            elif prefix == "&":
                # Conjuction module
                conjunctions[name] = destinations
            else:
                raise Exception

    # We now need to find all modules that link to the conjuction modules
    for line in array:
        name, destinations = line.split(" -> ")
        destinations = destinations.split(", ")

        # Remove the prefix character, if it is not the broadcaster
        if name != "broadcaster":
            name = name[1:]

        # Check this module's destinations to see if any of them point to a
        # conjuction module
        for destination in destinations:
            if destination in conjunctions:
                # If so, save it to the dict for this conjuction module
                memory[destination] = memory.get(destination, {})
                memory[destination][name] = False

    # Initial number of low and high pulses
    low = high = 0

    # Loop 1000 times
    for _ in range(1000):
        # We use BFS to simulate each button press, using a list of tuples
        # (start-module, pulse, destination-module)
        # For the pulse, False - low, True - high
        queue: list[tuple[str, bool, str]] = [("button", False, "broadcaster")]

        while queue:
            start, pulse, end = queue.pop(0)

            # Update the counters for the different pulses, depending on whether
            # the pulse is high (True) or low (False)
            if pulse:
                high += 1
            else:
                low += 1

            # The broadcaster module is the only one that doesn't use a dict
            if end == "broadcaster":
                # Add the destination modules to the queue
                for dest in broadcaster:
                    queue.append((end, pulse, dest))
            elif end in flip_flops:
                # Flip-flop modules only do something if the pulse is low
                if not pulse:
                    # Flip the state of the module
                    states[end] = not states[end]

                    # Add the destination modules to the queue
                    for dest in flip_flops[end]:
                        queue.append((end, states[end], dest))
            elif end in conjunctions:
                # Update the memory for the module that is sending this pulse
                memory[end][start] = pulse

                # If all input modules sent a high pulse (True), then the conjunction
                # module will send a low pulse (False), and vice versa
                next_pulse = not all(memory[end].values())

                # Add the destination modules to the queue
                for dest in conjunctions[end]:
                    queue.append((end, next_pulse, dest))

    # The final result is the product of the total number of high and low pulses
    result = low * high

    print(result)


def part_two(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    broadcaster: list[str] = []
    flip_flops: dict[str, list[str]] = {}
    conjunctions: dict[str, list[str]] = {}

    states: dict[str, bool] = {}
    memory: dict[str, dict[str, bool]] = {}

    for line in array:
        name, destinations = line.split(" -> ")
        destinations = destinations.split(", ")

        if name == "broadcaster":
            broadcaster = destinations
        else:
            prefix, name = name[0], name[1:]

            if prefix == "%":
                flip_flops[name] = destinations
                states[name] = False
            elif prefix == "&":
                conjunctions[name] = destinations
            else:
                raise Exception

    for line in array:
        name, destinations = line.split(" -> ")
        destinations = destinations.split(", ")

        if name != "broadcaster":
            name = name[1:]

        for destination in destinations:
            if destination in conjunctions:
                memory[destination] = memory.get(destination, {})
                memory[destination][name] = False

    # Analysing the puzzle input, there is one conjuction module that feeds rx,
    # and four conjunction modules feed this. For rx to have a low pulse, the four
    # modules must all have a high pulse. Analysing a number of iterations,
    # each of the four modules produce a high pulse on a regular cycle. Therefore,
    # the final result will be the lowest common multiple of the number of
    # button presses required to produce a high pulse in each of the four
    # conjunction modules.

    # First, find the conjuction module that feeds rx (find the 'parent' module)
    parent = None
    for name, destinations in conjunctions.items():
        if destinations == ["rx"]:
            parent = name
            break

    assert parent is not None

    # Find the four modules that send a pulse to the rx 'parent' module
    modules = [
        name for name, destinations in conjunctions.items() if parent in destinations
    ]

    assert len(modules) == 4

    # `cycles` will contain the number of iterations required for each module in
    # `modules` to cycle (loop)
    cycles: list[int] = []

    # Number of button presses
    counter = 0

    # Continue looping until we have found all four cycles
    while len(cycles) < 4:
        queue: list[tuple[str, bool, str]] = [("button", False, "broadcaster")]

        # Increment the counter
        counter += 1

        while queue:
            start, pulse, end = queue.pop(0)

            # If one of the modules in `modules` is sending a high pulse, then
            # we have found a cycle
            if pulse and (start in modules):
                cycles.append(counter)

            if end == "broadcaster":
                for dest in broadcaster:
                    queue.append((end, pulse, dest))
            elif end in flip_flops:
                if not pulse:
                    states[end] = not states[end]

                    for dest in flip_flops[end]:
                        queue.append((end, states[end], dest))
            elif end in conjunctions:
                memory[end][start] = pulse

                next_pulse = not all(memory[end].values())

                for dest in conjunctions[end]:
                    queue.append((end, next_pulse, dest))

    # The final result is the LCM of the four cycles
    result = math.lcm(*cycles)

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
