import os


def part_one(puzzle_input: str) -> None:
    array = puzzle_input.strip().splitlines()

    # Graph to represent the nodes, the key is the node and the value is a set
    # containing the connected nodes
    graph: dict[str, set[str]] = {}

    for line in array:
        # Parse the node and adjacent nodes
        node, adjacents = line.split(": ")
        adjacents = adjacents.split(" ")

        if node not in graph:
            graph[node] = set()

        for adjacent in adjacents:
            if adjacent not in graph:
                graph[adjacent] = set()

            # Add the nodes into the graph, from both ends
            graph[node].add(adjacent)
            graph[adjacent].add(node)

    def bfs_find_path(
        start: str, end: str, visited: set[tuple[str, ...]]
    ) -> list[str] | None:
        """
        This function uses BFS to find a path between two nodes: `start` and `end`.
        `visited` is a set that contains the edges that we cannot use, as they
        have already been traversed.
        """

        # The queue will contain lists of nodes that we have traversed so far
        queue: list[list[str]] = [[start]]

        # Create a local copy within the function for BFS
        visited = visited.copy()

        while queue:
            nodes = queue.pop(0)

            # Take the last node from the list, which is the last node in the path
            node = nodes[-1]

            for adjacent in graph[node]:
                # The edge is represented as a tuple from `node` to the adjacent
                # node. The edge must be sorted so the order of the two nodes
                # in the edge is always the same.
                edge = tuple(sorted([node, adjacent]))

                # Add the adjacent node into the path
                new_nodes = nodes.copy()
                new_nodes.append(adjacent)

                # Only continue if we haven't used this edge yet
                if edge not in visited:
                    # If we are at the end node, then return the path (the list
                    # of nodes)
                    if adjacent == end:
                        return new_nodes

                    # Otherwise, add the edge into the visited set, and add the
                    # new path to the queue
                    visited.add(edge)
                    queue.append(new_nodes)

        # If we reach here, then it was not possible to make a path from `start`
        # to `end`
        return None

    # This list will contain the three edges we are looking to remove
    edges: list[tuple[str, str]] = []

    for line in array:
        node, adjacents = line.split(": ")
        adjacents = adjacents.split(" ")

        # Loop through each edge in the graph
        for adjacent in adjacents:
            visited: set[tuple[str, ...]] = set()

            result = 0

            # We use the function to find out how many unique shortest-length
            # paths we can make between the two nodes, without sharing any edges.
            # This number will tell us how many edges, including this one, would
            # have to be disconnected in order to create two separate groups of
            # nodes. If we find only 3 unique paths, then this is one of the
            # edges we are looking for.
            while nodes := bfs_find_path(node, adjacent, visited):
                # If we find a path, add the edges into the `visited` set, then
                # loop again with the updated set of nodes.
                for i in range(1, len(nodes)):
                    edge = tuple(sorted([nodes[i], nodes[i - 1]]))
                    visited.add(edge)

                # Increment the number of paths found
                result += 1

                # If we've found more than 3 paths, then move on to the next edge
                if result > 3:
                    break
            else:
                # Otherwise, this is one of the edges to disconnect
                edges.append((node, adjacent))

            # If we've found all three, we can break early
            if len(edges) == 3:
                break
        else:
            continue

        break

    assert len(edges) == 3

    # Remove the three edges from the graph. We should now have two disconnected,
    # separate graphs.
    for node1, node2 in edges:
        graph[node1].remove(node2)
        graph[node2].remove(node1)

    def bfs(start: str) -> int:
        """
        Function to perform BFS on a graph, and return the number of nodes
        in the graph.
        """
        visited: set[str] = {start}
        queue = [start]

        while queue:
            node = queue.pop(0)

            for adjacent in graph[node]:
                if adjacent not in visited:
                    visited.add(adjacent)
                    queue.append(adjacent)

        # The result is the number of nodes iterated through
        return len(visited)

    # Perform BFS on two nodes of one of the disconnected edges, and multiply
    # the values together to get the final result
    result = bfs(edges[0][0]) * bfs(edges[0][1])

    print(result)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    puzzle_input = f.read()

part_one(puzzle_input)
