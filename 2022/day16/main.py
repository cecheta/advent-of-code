import heapq
import re
from functools import cache


class Valve:
    def __init__(self, name: str, rate: int, tunnels: list[str]) -> None:
        self.name = name
        self.rate = rate
        self.tunnels = tunnels


class Graph:
    def __init__(self) -> None:
        self.adjacencyList: dict[str, list[str]] = {}

    def add_valve(self, valve: Valve):
        self.adjacencyList[valve.name] = valve.tunnels

    # Cache the results from this function so the distances do not need to be
    # calculated multiple times
    @cache
    def dijkstra(self, valve: Valve) -> dict[str, int]:
        # Dijkstra's algorithm to find the shortest distance from one valve to
        # all the other valves
        distances: dict[str, int] = {}
        queue: list[tuple[int, str]] = []

        for node in self.adjacencyList:
            if node == valve.name:
                distances[node] = 0
                heapq.heappush(queue, (0, node))
            else:
                distances[node] = 1000000
                heapq.heappush(queue, (1000000, node))

        while queue:
            _, vertex = heapq.heappop(queue)

            for node in self.adjacencyList[vertex]:
                # The distance between each valve is 1
                new_distance = distances[vertex] + 1

                if distances[node] > new_distance:
                    distances[node] = new_distance
                    heapq.heappush(queue, (new_distance, node))

        # Delete the start valve from the results
        del distances[valve.name]

        return distances


def calculate(input: str, time: int) -> dict[str, int]:
    input_array = input.splitlines()

    all_valves: dict[str, Valve] = {}
    flowing_valves: set[str] = set()

    for line in input_array:
        # Parse the values from the text
        match = re.search(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)', line)
        assert match
        groups = match.groups()

        name = groups[0]
        rate = int(groups[1])
        tunnels = groups[2].split(', ')

        # Keep track of the valves that are flowing
        if rate > 0:
            flowing_valves.add(name)

        valve = Valve(name, rate, tunnels)

        # `all_valves` is a dict containing all the valves
        all_valves[name] = valve

    # Create the graph
    graph = Graph()

    for valve in all_valves.values():
        graph.add_valve(valve)

    # `best` is a dict where the key is the valves visited and the value is
    # the maximum pressure released from that path
    best: dict[str, int] = {}

    def recurse(start: str, remaining_valves: set[str], running_total: int, pressure: int, time_remaining: int):
        """
        Recursive function to iterate through all possible paths within the cave
        """

        # `visited_valves` is a set of the valves that have been turned off
        visited_valves = flowing_valves - remaining_valves

        # hash the visited valves into a string
        hash = ','.join(sorted(list(visited_valves)))

        # Calculate the total pressure released if no other valves are opened
        total_pressure = running_total + (pressure * time_remaining)

        # Update the maximum total pressure released for this path
        best[hash] = max(best.get(hash, 0), total_pressure)

        # Find the shorted path to all other valves
        nodes = graph.dijkstra(all_valves[start])

        # Filter the valves to only include the valves which haven't been
        # opened yet
        valves = {k: v for k, v in nodes.items() if k in remaining_valves}

        # Iterate through all the remaining valves
        for valve, distance in valves.items():
            # Remove from the set the valve that is about to be visited
            new_flowing_valves = remaining_valves.copy()
            new_flowing_valves.discard(valve)

            # Calculate the new time remaining after moving to the next valve
            new_time_remaining = time_remaining - (distance + 1)

            # If there is not enough time to visit the next valve, then continue
            if new_time_remaining <= 0:
                continue

            # Calculate the new total pressure released and new pressure rate
            new_running_total = running_total + pressure * (distance + 1)
            new_pressure = pressure + all_valves[valve].rate

            # Call function recursively
            recurse(valve, new_flowing_valves, new_running_total, new_pressure, new_time_remaining)

    # Recurse from the starting valve 'AA'
    recurse('AA', flowing_valves, 0, 0, time)

    return best


def part_one(input: str):
    # `results` is a dict where the key is the valves visited and the value is
    # the maximum pressure released from that path
    results = calculate(input, 30)

    # The solution is the maximum pressure released across all paths
    result = max(results.values())

    print(result)


def part_two(input: str):
    # `results` is a dict where the key is the valves visited and the value is
    # the maximum pressure released from that path
    results = calculate(input, 26)

    # Parse the results into a list of tuples, where each tuple is a set of the
    # valves visited, and the maximum pressure released for that path
    results_list: list[tuple[set[str], int]] = [(set(k.split(',')), v) for k, v in results.items()]

    # The result will be the maximum pressure released for a pair of paths
    # which do not share any common valves
    result = -1

    for i in range(len(results_list)):
        valves1, pressure1 = results_list[i]

        for j in range(i + 1, len(results_list)):
            valves2, pressure2 = results_list[j]

            # If there are no common valves between the two paths, then update
            # the result
            if valves1.isdisjoint(valves2):
                result = max(result, pressure1 + pressure2)

    print(result)


with open('input.txt') as f:
    input = f.read()


part_one(input)
part_two(input)
