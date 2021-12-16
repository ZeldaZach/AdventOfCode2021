import pathlib
from functools import reduce
from typing import List, Tuple


def read_inputs(input_file: str) -> str:
    with pathlib.Path(input_file).open() as fp:
        return str(fp.readline()).strip()


def part1() -> int:
    # 35 minutes
    line = read_inputs("input.txt")

    total = ""
    for char in line:
        x = bin(int(char, 16))[2:].zfill(4)
        total += x

    return operate_on_data_recursively(total)[0]


def part2() -> int:
    # 14 minutes
    line = read_inputs("input.txt")

    total = ""
    for char in line:
        x = bin(int(char, 16))[2:].zfill(4)
        total += x

    return operate_on_data_recursively(total)[2]


def operate_on_data_recursively(bin_data: str) -> Tuple[int, int, int]:
    version = int(bin_data[0:3], 2)
    type_id = int(bin_data[3:6], 2)

    version_sum_found, offset_bits, inner_values = (
        operate_on_inner_packets_recursively(bin_data) if type_id != 4 else (0, 0, 0)
    )

    version_sum = version + version_sum_found

    if type_id == 0:
        return version_sum, offset_bits, sum(x for x in inner_values)
    if type_id == 1:
        return version_sum, offset_bits, reduce(lambda x, y: x * y, inner_values)
    if type_id == 2:
        return version_sum, offset_bits, min(inner_values)
    if type_id == 3:
        return version_sum, offset_bits, max(inner_values)
    if type_id == 4:
        all_bits_in_number = ""

        offset_bits = 6
        while bin_data[offset_bits] == "1":
            all_bits_in_number += bin_data[offset_bits + 1 : offset_bits + 5]
            offset_bits += 5

        all_bits_in_number += bin_data[offset_bits + 1 : offset_bits + 5]

        value = int(all_bits_in_number, 2)
        return version_sum, offset_bits + 5, value
    if type_id == 5:
        return version_sum, offset_bits, int(inner_values[0] > inner_values[1])
    if type_id == 6:
        return version_sum, offset_bits, int(inner_values[0] < inner_values[1])
    if type_id == 7:
        return version_sum, offset_bits, int(inner_values[0] == inner_values[1])


def operate_on_inner_packets_recursively(bin_data: str) -> Tuple[int, int, List[int]]:
    inner_values = []
    version_sum = 0

    type_id_length = int(bin_data[6], 2)
    if type_id_length:
        offset_bits = 18

        total_number_of_sub_packets = int(bin_data[7:18], 2)
        for _ in range(total_number_of_sub_packets):
            version_sum_found, bits_used, value = operate_on_data_recursively(
                bin_data[offset_bits:]
            )
            offset_bits += bits_used
            inner_values.append(value)
            version_sum += version_sum_found
    else:
        offset_bits = 22

        length_of_all_sub_packets = int(bin_data[7:22], 2) + offset_bits
        while offset_bits < length_of_all_sub_packets:
            version_sum_found, bits_used, value = operate_on_data_recursively(
                bin_data[offset_bits:]
            )
            offset_bits += bits_used
            inner_values.append(value)
            version_sum += version_sum_found

    return version_sum, offset_bits, inner_values


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
