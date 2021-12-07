import pathlib
from typing import List, Tuple


def read_inputs(input_file: str) -> List[List[int]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    total = []
    for line in lines:
        total.append([int(x) for x in line.strip()])

    return total


def part1() -> int:
    # 10 minutes
    lines = read_inputs("input.txt")

    holder = [0] * len(lines[0])
    for line in lines:
        for index, bit in enumerate(line):
            holder[index] += 1 if bit else -1

    gamma_holder = ""
    epsilon_holder = ""
    for index, count in enumerate(holder):
        gamma_holder += "1" if count > 0 else "0"
        epsilon_holder += "0" if count > 0 else "1"

    return int(gamma_holder, 2) * int(epsilon_holder, 2)


def part2() -> int:
    # 9 minutes
    lines = read_inputs("input.txt")

    oxygen_indices = list(range(0, len(lines)))
    co2_indices = list(range(0, len(lines)))

    for action_bit in range(0, len(lines[0])):
        if len(oxygen_indices) > 1:
            oxygen_one_indices = [
                index for index in oxygen_indices if lines[index][action_bit]
            ]
            oxygen_zero_indices = list(set(oxygen_indices) - set(oxygen_one_indices))
            oxygen_indices = (
                oxygen_one_indices
                if len(oxygen_one_indices) >= len(oxygen_zero_indices)
                else oxygen_zero_indices
            )

        if len(co2_indices) > 1:
            co2_one_indices = [
                index for index in co2_indices if lines[index][action_bit]
            ]
            co2_zero_indices = list(set(co2_indices) - set(co2_one_indices))
            co2_indices = (
                co2_one_indices
                if len(co2_one_indices) < len(co2_zero_indices)
                else co2_zero_indices
            )

    oxygen = int("".join([str(x) for x in lines[oxygen_indices[0]]]), 2)
    co2 = int("".join([str(x) for x in lines[co2_indices[0]]]), 2)
    return oxygen * co2


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
