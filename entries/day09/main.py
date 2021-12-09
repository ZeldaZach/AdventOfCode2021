import math
import pathlib
from typing import List


def read_inputs(input_file: str) -> List[List[int]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    return [[int(x) for x in line.strip()] for line in lines]


def part1() -> int:
    # 25 minutes
    lines = read_inputs("input.txt")

    total_risk = 0
    for x, entries in enumerate(lines):
        for y, entry in enumerate(entries):
            left = lines[x + 1][y] > entry if x + 1 < len(lines) else True
            right = lines[x - 1][y] > entry if x - 1 >= 0 else True
            up = lines[x][y + 1] > entry if y + 1 < len(lines[x]) else True
            down = lines[x][y - 1] > entry if y - 1 >= 0 else True

            if left and right and up and down:
                total_risk += 1 + entry

    return total_risk


def part2() -> int:
    # 8 minutes
    lines = read_inputs("input.txt")

    all_basin_sizes = []
    for x, entries in enumerate(lines):
        for y, entry in enumerate(entries):
            left = lines[x + 1][y] > entry if x + 1 < len(lines) else True
            right = lines[x - 1][y] > entry if x - 1 >= 0 else True
            up = lines[x][y + 1] > entry if y + 1 < len(lines[x]) else True
            down = lines[x][y - 1] > entry if y - 1 >= 0 else True

            if left and right and up and down:
                basin_count = find_all_in_basin_recursive(lines, x, y)
                all_basin_sizes.append(basin_count)

    return math.prod(sorted(all_basin_sizes)[-3:])


def find_all_in_basin_recursive(lines, x, y):
    if not (0 <= x < len(lines)) or not (0 <= y < len(lines[x])) or lines[x][y] == 9:
        return 0

    lines[x][y] = 9

    return (
        1
        + find_all_in_basin_recursive(lines, x - 1, y)
        + find_all_in_basin_recursive(lines, x + 1, y)
        + find_all_in_basin_recursive(lines, x, y - 1)
        + find_all_in_basin_recursive(lines, x, y + 1)
    )


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
