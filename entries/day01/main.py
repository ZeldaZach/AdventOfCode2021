import pathlib
from typing import List


def read_inputs(input_file: str) -> List[int]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    return list(map(int, lines))


def part1() -> int:
    # 5 minutes
    lines = read_inputs("input.txt")
    total_increasing = sum(
        [1 for index, line in enumerate(lines) if line > lines[index - 1]]
    )
    return total_increasing


def part2() -> int:
    # 8 minutes
    lines = read_inputs("input.txt")

    count = 0
    for i in range(0, len(lines) - 3):
        range_a = lines[i : i + 3]
        range_b = lines[i + 1 : i + 4]

        count += sum(range_b) > sum(range_a)

    return count


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
