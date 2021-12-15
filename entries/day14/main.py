import pathlib
import re
from collections import defaultdict
from typing import Tuple, Dict


def read_inputs(input_file: str) -> Tuple[str, Dict[str, int]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    split_regex = re.compile(r"([A-Z])([A-Z]) -> ([A-Z])\n")

    mapping = defaultdict(str)
    for line in lines[2:]:
        match = split_regex.match(line)
        mapping[match.group(1) + match.group(2)] = match.group(3)

    return lines[0].strip(), dict(mapping)


def part1() -> int:
    # 15 minutes
    polymer, rules = read_inputs("input.txt")

    for _ in range(0, 10):
        new_polymer = ""
        for i, letter in enumerate(polymer[:]):
            new_polymer += letter

            two_letters = "".join(polymer[i : i + 2])
            if two_letters in rules:
                new_polymer += rules[two_letters]

        polymer = new_polymer

    mapping = defaultdict(int)
    for char in polymer:
        mapping[char] += 1

    return max(mapping.values()) - min(mapping.values())


def part2() -> int:
    # 55 minutes
    polymer, rules = read_inputs("input.txt")

    polymer_mapping = defaultdict(int)
    for i in range(len(polymer) - 1):
        two_letters = "".join(polymer[i : i + 2])
        polymer_mapping[two_letters] += 1

    for i in range(0, 40):
        new_polymer_mapping = defaultdict(int)

        for pair, total in polymer_mapping.items():
            if pair in rules:
                back_pair = pair[0] + rules[pair]
                front_pair = rules[pair] + pair[1]

                new_polymer_mapping[back_pair] += total
                new_polymer_mapping[front_pair] += total

        polymer_mapping = defaultdict(int)
        for pair, total in new_polymer_mapping.items():
            polymer_mapping[pair] = total

    letter_map = defaultdict(int)
    letter_map[polymer[-1]] = 1  # Last letter doesn't get counted by default
    for pair, total in polymer_mapping.items():
        letter_map[pair[0]] += total

    return max(letter_map.values()) - min(letter_map.values())


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
