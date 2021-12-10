import pathlib
from typing import List


def read_inputs(input_file: str) -> List[List[str]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    return [[str(x) for x in line.strip()] for line in lines]


def part1() -> int:
    # 7 minutes
    lines = read_inputs("input.txt")

    open_chars = ["(", "[", "{", "<"]
    close_mapping = {")": 3, "]": 57, "}": 1197, ">": 25137}

    game = 0
    for line in lines:
        stack = []
        for char in line:
            if char in open_chars:
                stack.append(char)
                continue

            corrupted_entry = False
            for open_char, close_char in zip(open_chars, close_mapping.keys()):
                if char == close_char:
                    if stack[-1] == open_char:
                        stack.pop()
                    else:
                        game += close_mapping[close_char]
                        corrupted_entry = True
                    break

            if corrupted_entry:
                break

    return game


def part2() -> int:
    # 9 minutes
    lines = read_inputs("input.txt")

    open_mapping = {"(": 1, "[": 2, "{": 3, "<": 4}
    close_mapping = {")": 3, "]": 57, "}": 1197, ">": 25137}

    valid_scores = []
    for line in lines:
        stack = []
        corrupted_entry = False
        for char in line:
            if char in open_mapping:
                stack.append(char)
                continue

            for open_char, close_char in zip(open_mapping.keys(), close_mapping.keys()):
                if char == close_char:
                    if stack[-1] == open_char:
                        stack.pop()
                    else:
                        corrupted_entry = True
                    break

        if not corrupted_entry:
            game = 0
            for char in reversed(stack):
                game = 5 * game + (open_mapping[char])
            valid_scores.append(game)

    return sorted(valid_scores)[len(valid_scores) // 2]


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
