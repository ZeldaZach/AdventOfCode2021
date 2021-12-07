import pathlib
from typing import List, Tuple


def read_inputs(input_file: str) -> List[Tuple[str, int]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    return [
        (vector, int(magnitude))
        for vector, magnitude in [line.split(" ") for line in lines]
    ]


def part1() -> int:
    # 5 minutes
    lines = read_inputs("input.txt")

    horizontal = 0
    depth = 0

    for line in lines:
        if line[0] == "forward":
            horizontal += line[1]
        elif line[0] == "down":
            depth += line[1]
        elif line[0] == "up":
            depth -= line[1]
        else:
            print("Unknown action", line[0])
            exit(1)

    return horizontal * depth


def part2() -> int:
    # 1 minute
    lines = read_inputs("input.txt")

    horizontal = 0
    depth = 0
    aim = 0

    for line in lines:
        if line[0] == "forward":
            horizontal += line[1]
            depth += aim * line[1]
        elif line[0] == "down":
            aim += line[1]
        elif line[0] == "up":
            aim -= line[1]
        else:
            print("Unknown action", line[0])
            exit(1)

    return horizontal * depth


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
