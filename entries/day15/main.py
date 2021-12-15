import copy
import heapq
import pathlib
from collections import defaultdict
from typing import List, Tuple


def read_inputs(input_file: str) -> List[List[int]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    return [[int(x) for x in line.strip()] for line in lines]


def part1() -> int:
    # 49 minutes
    lines = read_inputs("input.txt")
    return dijkstra(lines, (0, 0), (len(lines) - 1, len(lines[-1]) - 1))


def part2() -> int:
    # 42 minutes
    lines = read_inputs("input.txt")

    new_lines = copy.deepcopy(lines)

    # Generate extra columns
    for i in range(1, 5):
        for row, columns in enumerate(lines):
            for value in columns:
                new_value = value + i - 9 if value + i > 9 else (value + i) % 10
                new_lines[row].append(new_value)

    # Generate extra rows after our extra columns were added, for simplicity
    additional_rows = []
    for i in range(1, 5):
        for row, columns in enumerate(new_lines):
            additional_row = []
            for value in columns:
                new_value = value + i - 9 if value + i > 9 else (value + i) % 10
                additional_row.append(new_value)

            additional_rows.append(additional_row)

    # Complete our new 5x5 sized grid, with special rules
    new_lines.extend(additional_rows)

    return dijkstra(new_lines, (0, 0), (len(new_lines) - 1, len(new_lines[-1]) - 1))


def dijkstra(
    lines: List[List[int]], start_node: Tuple[int, int], end_node: Tuple[int, int]
) -> int:
    visited_nodes = set()
    edge_costs = defaultdict(lambda: float("inf"))

    priority_queue = [(0, start_node)]
    while priority_queue:
        cumulative_cost, (node_x, node_y) = heapq.heappop(priority_queue)
        visited_nodes.add((node_x, node_y))

        if (node_x, node_y) == end_node:
            return cumulative_cost

        for (x, y) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = node_x + x, node_y + y

            if (
                0 <= new_x < len(lines)
                and 0 <= new_y < len(lines[node_x])
                and (new_x, new_y) not in visited_nodes
            ):
                cost = cumulative_cost + lines[new_x][new_y]
                if edge_costs[(new_x, new_y)] > cost:
                    edge_costs[(new_x, new_y)] = cost
                    heapq.heappush(priority_queue, (cost, (new_x, new_y)))


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
