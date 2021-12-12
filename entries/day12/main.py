import pathlib
from collections import defaultdict
from typing import List, Tuple, Set, Dict


def read_inputs(input_file: str) -> List[List[str]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    return [[x.strip() for x in line.split("-")] for line in lines]


def part1() -> int:
    # 49 minutes
    lines = read_inputs("input.txt")

    graph = defaultdict(set)
    for start_pos, end_pos in lines:
        graph[start_pos].add(end_pos)
        graph[end_pos].add(start_pos)

    return find_paths(graph, "start", "end", [], set())


def part2() -> int:
    # 10 minutes
    lines = read_inputs("input.txt")

    graph = defaultdict(set)
    for start_pos, end_pos in lines:
        graph[start_pos].add(end_pos)
        graph[end_pos].add(start_pos)

    part2_unique_paths = set()
    for double_entry in graph:
        if double_entry.islower():
            find_paths(graph, "start", "end", [], part2_unique_paths, double_entry)

    return len(part2_unique_paths)


def find_paths(
    graph: Dict[str, Set[str]],
    node: str,
    end_node: str,
    path: List[str],
    unique_found_paths: Set[Tuple[str, ...]],
    allowed_twice: str = "",
) -> int:
    """
    DFS Find all paths from start to end
    :param graph: Adjacency List Graph
    :param node:  Current Node
    :param end_node: Node to stop execution on
    :param path: Current path taken
    :param unique_found_paths: All uniquely found paths so far
    :param allowed_twice: What lower case node, if any, can be found multiple times
    :return: How many paths were found (pt1)
    """
    if node == end_node:
        if path.count("start") == 1 and end_node not in path:
            unique_found_paths.add(tuple(path))
        return 1

    total_paths = 0
    for neighbor in graph[node]:
        if (
            neighbor not in path
            or neighbor.isupper()
            or (neighbor == allowed_twice and path.count(allowed_twice) < 2)
        ):
            total_paths += find_paths(
                graph,
                neighbor,
                end_node,
                path + [node],
                unique_found_paths,
                allowed_twice,
            )

    return total_paths


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
