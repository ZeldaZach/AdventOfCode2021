import pathlib
from collections import defaultdict
from typing import List, Tuple

import re


def read_inputs(input_file: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    line_regex = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")

    return [
        (
            (int(match.group(1)), int(match.group(2))),
            (int(match.group(3)), int(match.group(4))),
        )
        for match in [line_regex.match(line.strip()) for line in lines]
    ]


def part1() -> int:
    # 15 minutes
    coord_pairs = read_inputs("input.txt")

    danger_coord = defaultdict(int)

    for coord_pair in coord_pairs:
        x1, y1 = coord_pair[0]
        x2, y2 = coord_pair[1]

        if x1 != x2 and y1 != y2:
            # Ignore Diagonals
            continue

        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                danger_coord[(x, y)] += 1

    total = sum(1 for value in danger_coord.values() if value >= 2)
    return total


def part2() -> int:
    # 22 minutes b/c reading is hard
    coord_pairs = read_inputs("input.txt")

    danger_coord = defaultdict(int)

    for coord_pair in coord_pairs:
        x1, y1 = coord_pair[0]
        x2, y2 = coord_pair[1]

        if x1 != x2 and y1 != y2:
            # 45 Degree Diagonals
            if x1 > x2:
                # Swap points to make logic easier below
                (x1, y1), (x2, y2) = (x2, y2), (x1, y1)

            while x1 <= x2:
                danger_coord[(x1, y1)] += 1
                x1 += 1
                y1 += 1 if y1 < y2 else -1
        else:
            # Vertical or Horizontal
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    danger_coord[(x, y)] += 1

    total = sum(1 for value in danger_coord.values() if value >= 2)
    return total


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
