import pathlib
import re
from typing import List, Tuple


def read_inputs(input_file: str) -> Tuple[List[Tuple[int, ...]], List[Tuple[str, int]]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    fold_line_regex = re.compile(r"fold along ([xy])=(\d+)\n")
    coordinate_regex = re.compile(r"(\d+),(\d+)\n")

    coords = []
    actions = []
    for line in lines:
        if not line.strip():
            continue

        if line.startswith("fold"):
            axis, magnitude = fold_line_regex.findall(line)[0]
            actions.append((axis, int(magnitude)))
        else:
            x, y = coordinate_regex.findall(line)[0]
            coords.append((int(x), int(y)))

    return coords, actions


def part1() -> int:
    # 17 min
    coords, actions = read_inputs("input.txt")
    coords = fold_the_stuff(coords, actions, 1)
    return len(coords)


def part2() -> str:
    # 17 minutes
    coords, actions = read_inputs("input.txt")
    coords = fold_the_stuff(coords, actions)

    full_string = ""
    column_count = max([y for x, y in coords])
    row_count = max([x for x, y in coords])
    for y in range(column_count + 1):
        inner_string = ""
        for x in range(row_count + 1):
            inner_string += "#" if (x, y) in coords else " "
        full_string += inner_string + "\n"

    return full_string


def fold_the_stuff(
    coords: List[Tuple[int, ...]],
    actions: List[Tuple[str, int]],
    iteration_loops: int = 0,
) -> List[Tuple[int, ...]]:
    """
    Folding across X means...
    For all values with X > fold point:
        Dist = N => subtract 2 * N from the X value

    Folding across Y means...
        All values with Y > fold point get changed to
        Dist = N => subtract 2 * N from the Y value
    """
    iterations = 0
    for axis, fold_point in actions:
        if axis == "x":
            for index, coord in enumerate(coords):
                x, y = coord
                if x > fold_point:
                    coords[index] = (x - 2 * (x - fold_point), y)
        elif axis == "y":
            for index, coord in enumerate(coords):
                x, y = coord
                if y > fold_point:
                    coords[index] = (x, y - 2 * (y - fold_point))
        else:
            raise ValueError("Unknown Axis")

        coords = list(set(coords))

        iterations += 1
        if iterations == iteration_loops:
            break

    return coords


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
