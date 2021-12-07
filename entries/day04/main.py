import pathlib
from typing import List, Tuple, Set


def read_inputs(input_file: str) -> Tuple[List[int], List[List[int]]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    call_order = list(map(int, lines[0].split(",")))

    boards = []

    board = []
    for line in lines[2:]:
        if not line.strip():
            boards.append(board)
            board = []
            continue

        board.extend([int(x) for x in line.strip().split(" ") if x])

    boards.append(board)
    return call_order, boards


def part1() -> int:
    # 26 minutes
    call_order, boards = read_inputs("input.txt")

    board_sets = [set() for _ in range(len(boards))]

    for call_number in call_order:
        for index, board in enumerate(boards):
            try:
                board_sets[index].add(board.index(call_number))
            except ValueError:
                continue

        winning_board_indices = test_for_win(board_sets)
        for winning_board_index in winning_board_indices:
            winning_board = boards[winning_board_index]

            total = 0
            for i in range(0, len(winning_board)):
                if i not in board_sets[winning_board_index]:
                    total += winning_board[i]
            last_winning_board_total = total * call_number

            return last_winning_board_total


def part2() -> int:
    # 15 minutes
    call_order, boards = read_inputs("input.txt")

    board_sets = [set() for _ in range(len(boards))]

    last_winning_board_total = 0
    for call_number in call_order:
        for index, board in enumerate(boards):
            try:
                board_sets[index].add(board.index(call_number))
            except ValueError:
                continue

        winning_board_indices = test_for_win(board_sets)
        for winning_board_index in sorted(list(winning_board_indices), reverse=True):
            winning_board = boards[winning_board_index]

            total = 0
            for i in range(0, len(winning_board)):
                if i not in board_sets[winning_board_index]:
                    total += winning_board[i]
            last_winning_board_total = total * call_number

            # Remove winning boards as we don't need them anymore
            del boards[winning_board_index]
            del board_sets[winning_board_index]

    return last_winning_board_total


def test_for_win(board_sets: List[Set[int]]) -> Set[int]:
    winning_boards = set()

    for index, board_set in enumerate(board_sets):
        # Test for Column win
        for i in range(0, 6):
            if all(x in board_set for x in [0 + i, 5 + i, 10 + i, 15 + i, 20 + i]):
                winning_boards.add(index)

        # Test for Row win
        for i in range(0, 25, 5):
            if all(x in board_set for x in [0 + i, 1 + i, 2 + i, 3 + i, 4 + i]):
                winning_boards.add(index)

    return winning_boards


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
