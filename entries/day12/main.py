import pathlib
from collections import defaultdict
from typing import List, Tuple, Set, Dict


def read_inputs(input_file: str) -> List[List[str]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    return [[x.strip() for x in line.split("-")] for line in lines]


# I don't like this, but I forget how to handle Graphs... will do some more studying
part1_total_paths: int = 0
part2_unique_paths: Set[Tuple[str, ...]] = set()


def part1() -> int:
    # 49 minutes
    lines = read_inputs("input.txt")

    graph = defaultdict(set)
    for start_pos, end_pos in lines:
        graph[start_pos].add(end_pos)
        graph[end_pos].add(start_pos)

    find_paths(graph, "start", "end", [])
    return part1_total_paths


def part2() -> int:
    # 10 minutes

    # Reset globals
    global part1_total_paths, part2_unique_paths
    part1_total_paths = 0
    part2_unique_paths = set()

    lines = read_inputs("input.txt")

    graph = defaultdict(set)
    for start_pos, end_pos in lines:
        graph[start_pos].add(end_pos)
        graph[end_pos].add(start_pos)

    for double_entry in graph:
        if double_entry.islower():
            find_paths(graph, "start", "end", [], double_entry)

    return len(part2_unique_paths)


def find_paths(
    graph: Dict[str, Set[str]],
    node: str,
    end_node: str,
    path: List[str],
    allowed_twice: str = "",
) -> None:
    global part1_total_paths, part2_unique_paths

    if node == end_node:
        part1_total_paths += 1
        if path.count("start") == 1 and end_node not in path:
            part2_unique_paths.add(tuple(path))
        return

    for neighbor in graph[node]:
        if (
            (neighbor not in path)
            or neighbor.isupper()
            or (neighbor == allowed_twice and path.count(allowed_twice) < 2)
        ):
            find_paths(graph, neighbor, end_node, path + [node], allowed_twice)

    return


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
