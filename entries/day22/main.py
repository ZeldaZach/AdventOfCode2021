import pathlib
import re
from typing import Tuple, List


def read_inputs(input_file: str) -> List[Tuple[str, ...]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    regex = re.compile(
        r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"
    )
    return [tuple(regex.match(line).groups()) for line in lines]


def part1() -> int:
    # 7 minutes
    lines = read_inputs("input.txt")

    on_bits = set()

    for line in lines:
        turn_on = line[0] == "on"
        min_x, max_x, min_y, max_y, min_z, max_z = list(map(int, line[1:]))

        for x in range(max(-50, min_x), min(50, max_x) + 1):
            for y in range(max(-50, min_y), min(50, max_y) + 1):
                for z in range(max(-50, min_z), min(50, max_z) + 1):
                    point = (x, y, z)
                    if turn_on:
                        on_bits.add(point)
                    elif point in on_bits:
                        on_bits.remove(point)

    return len(on_bits)


def part2() -> int:
    # 1 hour 6 minutes put in already
    lines = read_inputs("test.txt")

    for line in lines:
        turn_on = line[0] == "on"
        min_x, max_x, min_y, max_y, min_z, max_z = list(map(int, line[1:]))


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
