import pathlib
from collections import defaultdict
from typing import List


def read_inputs(input_file: str) -> List[int]:
    with pathlib.Path(input_file).open() as fp:
        line = fp.readline().split(",")

    return list(map(int, line))


def part1() -> int:
    # 11 minutes
    fish_ages = read_inputs("input.txt")

    for day in range(0, 80):
        for index in range(len(fish_ages)):
            if fish_ages[index] == 0:
                fish_ages[index] = 7
                fish_ages.append(8)
            fish_ages[index] -= 1

    return len(fish_ages)


def part2() -> int:
    # 34 minutes
    fish_ages = read_inputs("input.txt")

    fishies = defaultdict(int)
    for fish in fish_ages:
        fishies[fish] += 1

    for day in range(0, 256):
        new_fish_ages = defaultdict(int)
        for key, value in fishies.items():
            new_fish_ages[key - 1] = value

        if new_fish_ages[-1]:
            new_fish_ages[8] += new_fish_ages[-1]
            new_fish_ages[6] += new_fish_ages[-1]
            del new_fish_ages[-1]

        fishies = new_fish_ages

    return sum(x for x in fishies.values())


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
