import itertools
import pathlib
import re
from collections import defaultdict
from typing import Tuple, Dict


def read_inputs(input_file: str) -> Tuple[int, int]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    regex = re.compile(r"Player \d starting position: (\d+)")
    return int(regex.match(lines[0]).group(1)), int(regex.match(lines[1]).group(1))


def part1() -> int:
    # 38 minutes
    p1_spot, p2_spot = read_inputs("input.txt")

    p1_score = 0
    p2_score = 0

    total_dice_rolled = 0
    current_die_value = 1
    while p1_score < 1000 and p2_score < 1000:
        dice_roll_total = 0
        for _ in range(0, 3):
            dice_roll_total += current_die_value
            current_die_value = (current_die_value + 1) % 100
            total_dice_rolled += 1

        p1_spot = (p1_spot + dice_roll_total) % 10
        if p1_spot == 0:
            p1_spot = 10

        p1_score += p1_spot

        # Player 2 won't go if Player 1 has already won
        if p1_score >= 1000:
            break

        dice_roll_total = 0
        for _ in range(0, 3):
            dice_roll_total += current_die_value
            current_die_value = (current_die_value + 1) % 100
            total_dice_rolled += 1

        p2_spot = (p2_spot + dice_roll_total) % 10
        if p2_spot == 0:
            p2_spot = 10

        p2_score += p2_spot

    return min(p1_score, p2_score) * total_dice_rolled


def part2() -> int:
    # 2 hours 18 minutes
    p1_spot, p2_spot = read_inputs("input.txt")

    roll_chances = defaultdict(int)
    roll_products = itertools.product(range(1, 4), repeat=3)
    for p1_roll_duplicates in list(map(sum, roll_products)):
        roll_chances[p1_roll_duplicates] += 1

    p1_wins, p2_wins = 0, 0
    states = defaultdict(int)
    states[(p1_spot, p2_spot, 0, 0)] = 1

    while states:
        # Player 1's Turn!
        new_states = defaultdict(int)
        for (p1_spot, p2_spot, p1_score, p2_score), duplicates in states.items():
            for p1_roll, p1_roll_duplicates in roll_chances.items():
                new_p1_spot = (p1_spot + p1_roll) % 10
                if not new_p1_spot:
                    new_p1_spot = 10
                new_states[
                    (new_p1_spot, p2_spot, new_p1_spot + p1_score, p2_score)
                ] += (duplicates * p1_roll_duplicates)

        additional_p1_wins, additional_p2_wins, states = remove_wins_from_states(
            new_states
        )
        p1_wins += additional_p1_wins
        p2_wins += additional_p2_wins

        # Player 2's Turn!
        new_states = defaultdict(int)
        for (p1_spot, p2_spot, p1_score, p2_score), duplicates in states.items():
            for p2_roll, p2_roll_duplicates in roll_chances.items():
                new_p2_spot = (p2_spot + p2_roll) % 10
                if not new_p2_spot:
                    new_p2_spot = 10
                new_states[
                    (p1_spot, new_p2_spot, p1_score, new_p2_spot + p2_score)
                ] += (duplicates * p2_roll_duplicates)

        additional_p1_wins, additional_p2_wins, states = remove_wins_from_states(
            new_states
        )
        p1_wins += additional_p1_wins
        p2_wins += additional_p2_wins

    return max(p1_wins, p2_wins)


def remove_wins_from_states(
    states: Dict[Tuple[int, int, int, int], int]
) -> Tuple[int, int, Dict[Tuple[int, int, int, int], int]]:
    p1_wins = 0
    p2_wins = 0
    for (p1, p2, score1, score2), duplicates in states.copy().items():
        if score1 >= 21:
            p1_wins += duplicates
            del states[(p1, p2, score1, score2)]
        elif score2 >= 21:
            p2_wins += duplicates
            del states[(p1, p2, score1, score2)]

    return p1_wins, p2_wins, states


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
