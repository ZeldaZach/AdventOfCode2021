import pathlib
from typing import List

import numpy


def read_inputs(input_file: str) -> List[int]:
    with pathlib.Path(input_file).open() as fp:
        line = fp.readline().split(",")

    return list(map(int, line))


def part1() -> int:
    # 5 minutes
    positions = read_inputs("input.txt")

    fiftieth_percentile = numpy.percentile(positions, 50)
    return int(sum(abs(x - fiftieth_percentile) for x in positions))


def part2() -> int:
    # 25 minutes
    positions = read_inputs("input.txt")

    return min(
        sum(
            # S = n(n+1)/2
            abs(test_position - crab_point) * (abs(test_position - crab_point) + 1) // 2
            for crab_point in positions
        )
        for test_position in range(min(positions), max(positions))
    )


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
