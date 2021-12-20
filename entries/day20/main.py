import itertools
import pathlib
from typing import Any, List, Tuple


def read_inputs(input_file: str) -> Tuple[List[str], List[List[str]]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    return [x for x in lines[0].strip()], [
        [x for x in line.strip()] for line in lines[2:]
    ]


def enhance_image(
    image: List[List[bool]], enhanced_replacement: List[bool], infinite_space_on: bool
) -> Tuple[List[List[bool]], bool]:
    # Add a border around the image to account for infinite space
    row_padding = [[infinite_space_on] * len(image)]
    col_padding = [infinite_space_on]
    image = row_padding + image + row_padding
    for i in range(len(image)):
        image[i] = col_padding + image[i] + col_padding

    new_image = []
    for x, row in enumerate(image):
        new_image_row = []
        for y in range(len(row)):
            binary_total = 0

            for x_off in range(-1, 2):
                for y_off in range(-1, 2):
                    binary_total <<= 1

                    if (0 <= x + x_off < len(image)) and (0 <= y + y_off < len(row)):
                        binary_total += int(image[x + x_off][y + y_off])
                    else:
                        binary_total += int(infinite_space_on)

            new_image_row.append(enhanced_replacement[binary_total])
        new_image.append(new_image_row)

    # Account for infinite space polarity
    if enhanced_replacement[0]:
        infinite_space_on = not infinite_space_on

    return new_image, infinite_space_on


def enhance_image_n_times(
    char_enhanced_replacement: List[str],
    char_image: List[List[str]],
    times_to_enhance: int,
) -> int:
    bool_enhanced_replacement = list(map(lambda x: x == "#", char_enhanced_replacement))
    bool_image = [list(map(lambda x: x == "#", row)) for row in char_image]

    infinite_space_on = False
    for i in range(0, times_to_enhance):
        bool_image, infinite_space_on = enhance_image(
            bool_image, bool_enhanced_replacement, infinite_space_on
        )

    return sum(list(itertools.chain(*bool_image)))


def part1() -> int:
    # 1 hour 1 minute
    char_enhanced_replacement, char_image = read_inputs("input.txt")
    return enhance_image_n_times(char_enhanced_replacement, char_image, 2)


def part2() -> int:
    # 1 minute
    char_enhanced_replacement, char_image = read_inputs("input.txt")
    return enhance_image_n_times(char_enhanced_replacement, char_image, 50)


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
