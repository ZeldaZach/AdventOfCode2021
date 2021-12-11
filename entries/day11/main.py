import pathlib
from typing import List, Tuple


def read_inputs(input_file: str) -> List[List[int]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    return [[int(x) for x in line.strip()] for line in lines]


def part1() -> int:
    # 10 minutes
    lines = read_inputs("input.txt")

    total = 0
    for i in range(100):
        for x, line in enumerate(lines):
            for y, entry in enumerate(line):
                lines[x][y] += 1

        total += total_flashes_recursively(lines, [])

        for x, line in enumerate(lines):
            for y, entry in enumerate(line):
                if entry > 9:
                    lines[x][y] = 0

    return total


def part2() -> int:
    # 4 minutes
    lines = read_inputs("input.txt")

    counter = 1
    while True:
        for x, line in enumerate(lines):
            for y, entry in enumerate(line):
                lines[x][y] += 1

        total_flashes_recursively(lines, [])

        blackout_grid = True
        for x, line in enumerate(lines):
            for y, entry in enumerate(line):
                if entry > 9:
                    lines[x][y] = 0
                else:
                    blackout_grid = False

        if blackout_grid:
            return counter

        counter += 1


def total_flashes_recursively(
    lines: List[List[int]], visited: List[Tuple[int, int]]
) -> int:
    for x, line in enumerate(lines):
        for y, entry in enumerate(line):
            if (x, y) in visited:
                continue

            if entry > 9:
                visited.append((x, y))

                x_plus_in_bounds = x + 1 < len(lines)
                x_minus_in_bounds = x - 1 >= 0
                y_plus_in_bounds = y + 1 < len(lines[x])
                y_minus_in_bounds = y - 1 >= 0

                if x_plus_in_bounds:
                    lines[x + 1][y] += 1
                if x_minus_in_bounds:
                    lines[x - 1][y] += 1
                if y_plus_in_bounds:
                    lines[x][y + 1] += 1
                if y_minus_in_bounds:
                    lines[x][y - 1] += 1
                if x_plus_in_bounds and y_plus_in_bounds:
                    lines[x + 1][y + 1] += 1
                if x_plus_in_bounds and y_minus_in_bounds:
                    lines[x + 1][y - 1] += 1
                if x_minus_in_bounds and y_plus_in_bounds:
                    lines[x - 1][y + 1] += 1
                if x_minus_in_bounds and y_minus_in_bounds:
                    lines[x - 1][y - 1] += 1

                return 1 + total_flashes_recursively(lines, visited)

    return 0


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
