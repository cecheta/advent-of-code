import os
from collections import deque


def part_one(puzzle_input: str) -> None:
    directions: dict[str, tuple[int, int]] = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }

    # Dict containing directions and the slopes we cannot go in for that direction
    opposites: dict[str, str] = {
        "up": "v",
        "down": "^",
        "left": ">",
        "right": "<",
    }

    grid = puzzle_input.strip().splitlines()

    start = end = None

    # Find the start and end points
    for i, char in enumerate(grid[0]):
        if char == ".":
            start = (0, i)
            break

    for i, char in enumerate(grid[-1]):
        if char == ".":
            end = (len(grid) - 1, i)
            break

    assert start is not None and end is not None

    seen: set[tuple[int, int]] = {start}
    queue: deque[tuple[int, int, set[tuple[int, int]]]] = deque([(*start, seen)])

    result = 0

    while queue:
        x, y, seen = queue.popleft()

        # If we are at the end, then the length of the path will be the length
        # of all the squares traversed
        # Subtract 1 due to the start square which is not included in the length
        if (x, y) == end:
            result = max(result, len(seen) - 1)

        # List of tuples containing the next square to move to
        # (x, y, slope)
        # `slope` is the coordinates of a slope that we passed through
        # If `slope` is None then we did not pass through a slope
        next_moves: list[tuple[int, int, tuple[int, int] | None]] = []

        # Iterate in all directions
        for dir, (a, b) in directions.items():
            new_x, new_y = x + a, y + b

            # Check if we have been on this square before
            if (new_x, new_y) in seen:
                continue

            # Check if the square is within the grid
            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                char = grid[new_x][new_y]

                # Empty path, can move to square
                if char == ".":
                    next_moves.append((new_x, new_y, None))
                # Forest, cannot move to square
                elif char == "#":
                    continue
                # Can only move to this square if we are not going up a slope
                # Add both the coordinates of the slope we passed through snd
                # the coordinates of the square after the slope
                elif opposites[dir] != char:
                    next_moves.append((new_x + a, new_y + b, (new_x, new_y)))

        # Add each next move to the queue, copying the set containing visited squares
        for move in next_moves:
            # If there is only one move to make, then can use the same set
            if len(next_moves) == 1:
                seen_copy = seen
            else:
                seen_copy = seen.copy()

            # `move[:2]` are the (x, y) coordinates
            seen_copy.add(move[:2])

            # Also add the coordinates of the slope, if we passed through one
            if move[2]:
                seen_copy.add(move[2])

            queue.append((*move[:2], seen_copy))

    print(result)


def part_two(puzzle_input: str) -> None:
    directions: dict[str, tuple[int, int]] = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }

    opposites: dict[str, str] = {
        "up": "down",
        "down": "up",
        "left": "right",
        "right": "left",
    }

    grid = puzzle_input.strip().splitlines()
    grid = [list(line) for line in grid]

    start = end = None

    for i, char in enumerate(grid[0]):
        if char == ".":
            start = (0, i)
            break

    for i, char in enumerate(grid[-1]):
        if char == ".":
            end = (len(grid) - 1, i)
            break

    assert start is not None and end is not None

    def draw_graph(
        start: tuple[int, int],
        current: tuple[int, int],
        dir: str,
        graph: dict[tuple[int, int], dict[tuple[int, int], int]],
    ):
        """
        Function to create a graph of nodes from the puzzle input.
        A node is considered as a square in the graph where there is more than
        one direction to move in, i.e. a junction

        start - The node we are leaving, looking for adjacent nodes
        current - The coordinates directly next to the `start` node, which indicates
            where we are moving away from the start node
        dir - The current direction we are moving in
        graph - The graph we are populating
        """

        # We start by assuming we have taken one step
        steps = 1
        point = current

        # We mark each square with "#" as we move through the grid, therefore if
        # we find a "#" then we have already been here and can return
        if grid[current[0]][current[1]] == "#":
            return

        # Loop until we arrive at another node
        while True:
            next_moves: list[tuple[int, int, str]] = []

            # Mark this square as visited
            grid[point[0]][point[1]] = "#"

            # Iterate in all directions
            for new_dir, (a, b) in directions.items():
                new_x, new_y = point[0] + a, point[1] + b

                # We cannot move in the direction back to where we came from
                if dir == opposites[new_dir]:
                    continue

                if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                    # If the square is not a forest then it is a valid move, however
                    # it may be marked as "#" if it is actually a node we have
                    # already visited. In this case, it will be in `graph`
                    if grid[new_x][new_y] != "#" or (new_x, new_y) in graph:
                        next_moves.append((new_x, new_y, new_dir))

            # If there is only one move to make, then make the move
            if len(next_moves) == 1:
                point = next_moves[0][:2]
                dir = next_moves[0][2]
                steps += 1

                # If we are at a node (that we've already visited), then break
                if point in graph:
                    break

            # Otherwise, stop moving and break
            else:
                break

        # Add the distance between the two nodes to the graph, from both ends
        graph[start] = graph.get(start, {})
        graph[start][point] = steps

        graph[point] = graph.get(point, {})
        graph[point][start] = steps

        # Recurse through the next possible moves
        for move in next_moves:
            # `move[:2]` is the coordinates of the next point we will start
            # iterating from, which is directly next to `point`
            draw_graph(point, move[:2], move[2], graph)

    def recurse(
        node: tuple[int, int],
        visited: set[tuple[int, int]],
        total: int,
        graph: dict[tuple[int, int], dict[tuple[int, int], int]],
    ) -> int:
        """
        Function to perform DFS to find the maximum length path
        """
        # If we are at the end, the total path is `total`
        if node == end:
            return total

        result = 0

        connected = graph[node]

        # Iterate through the connected nodes
        for n, steps in connected.items():
            if n not in visited:
                # Add the connected node to the visited set, recurse, then backtrack
                visited.add(n)
                result = max(result, recurse(n, visited, total + steps, graph))
                visited.remove(n)

        return result

    # Create the graph of each node and its connected nodes
    # Each key is the coordinates of a node, and the value is another dict of
    # each connected node, and the distance to the node
    # Note that `current` is `start`, instead of the coordinates next to `start`,
    # however this will be offset by removing 1 from the final result
    graph: dict[tuple[int, int], dict[tuple[int, int], int]] = {}
    draw_graph(start, start, "down", graph)

    # Need to subtract 1 from the result, as the algorithm will include the
    # start node in the total distance travelled
    result = recurse(start, {start}, 0, graph) - 1

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
part_two(puzzle_input)
