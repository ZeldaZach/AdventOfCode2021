import pathlib
import re
from typing import List, Union, Tuple


def read_inputs(input_file: str) -> List[int]:
    with pathlib.Path(input_file).open() as fp:
        line = fp.readline()

    area_regex = re.compile(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)")
    return list(map(int, area_regex.findall(line)[0]))


def check_if_probe_hits_recursively(
    probe_x: int,
    probe_y: int,
    velocity_x: int,
    velocity_y: int,
    target_x_range: List[int],
    target_y_range: List[int],
    max_probe_y: Union[int, float],
):
    probe_x += velocity_x
    probe_y += velocity_y

    velocity_x += -1 if velocity_x > 0 else (1 if velocity_x else 0)
    velocity_y -= 1

    if probe_x in target_x_range and probe_y in target_y_range:
        return True, max_probe_y
    if probe_x > max(target_x_range) or probe_y < min(target_y_range):
        return False, max_probe_y

    return check_if_probe_hits_recursively(
        probe_x,
        probe_y,
        velocity_x,
        velocity_y,
        target_x_range,
        target_y_range,
        max(max_probe_y, probe_y),
    )


def anal_the_probes(
    target_min_x: int, target_max_x: int, target_min_y: int, target_max_y: int
) -> Tuple[int, int]:
    valid_target_x = list(range(target_min_x, target_max_x + 1))
    valid_target_y = list(range(target_min_y, target_max_y + 1))

    valid_velocities = []
    max_height_of_valid_probe = float("-inf")

    for probe_x in range(1, max(valid_target_x)):
        for probe_y in range(min(valid_target_y), 100):
            does_hit_target, max_height = check_if_probe_hits_recursively(
                0, 0, probe_x, probe_y, valid_target_x, valid_target_y, float("-inf")
            )
            if does_hit_target:
                max_height_of_valid_probe = max(max_height_of_valid_probe, max_height)
                valid_velocities.append((probe_x, probe_y))

    return max_height_of_valid_probe, len(valid_velocities)


def part1() -> int:
    # 20 minutes
    x_min, x_max, y_min, y_max = read_inputs("input.txt")
    return anal_the_probes(x_min, x_max, y_min, y_max)[0]


def part2() -> int:
    # 7 minutes
    x_min, x_max, y_min, y_max = read_inputs("input.txt")
    return anal_the_probes(x_min, x_max, y_min, y_max)[1]


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
