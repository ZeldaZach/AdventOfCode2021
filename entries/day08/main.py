import pathlib
import re
from typing import List


def read_inputs(input_file: str) -> List[List[str]]:
    with pathlib.Path(input_file).open() as fp:
        lines = fp.readlines()

    regex = re.compile(r"([a-g]+)")

    return [
        ["".join(sorted(string)) for string in regex.findall(line)] for line in lines
    ]


def part1() -> int:
    # 19 minutes
    result = 0

    lines = read_inputs("input.txt")
    for line in lines:
        test_signals, answers = line[:10], line[10:]

        mapping = {}

        for test_signal in test_signals:
            if len(test_signal) == 7:
                mapping[test_signal] = 8
            elif len(test_signal) == 2:
                mapping[test_signal] = 1
            elif len(test_signal) == 4:
                mapping[test_signal] = 4
            elif len(test_signal) == 3:
                mapping[test_signal] = 7

        result += sum(1 for answer in answers if answer in mapping)

    return result


def part2() -> int:
    # 57 minutes
    """
    Lets think of the signals as indexes...

    0000
    1  2
    1  2
    3333
    4  5
    4  5
    6666

    From this, we know the following information:
    (*) Denotes we can deduce this without question, from Part 1 in some way

    (*) For Value 1: 2,5            2
    For Value 2: 0,2,3,4,6          5
    For Value 3: 0,2,3,5,6          5
    (*) For Value 4: 1,2,3,5        4
    For Value 5: 0,1,3,5,6          5
    For Value 6: 0,1,3,4,5,6        6
    (*) For Value 7: 0,2,5          3
    (*) For Value 8: 0,1,2,3,4,5,6  7
    For Value 9: 0,1,2,3,5,6        6
    For Value 0: 0,1,2,4,5,6        6
    """

    g_total = 0

    lines = read_inputs("input.txt")
    for line in lines:
        test_signals, answers = line[:10], line[10:]

        """
        We will reduce down the mapping as we eliminate invalid entries
        until we have only one entry per slot
        """
        mapping = {i: {"a", "b", "c", "d", "e", "f", "g"} for i in range(0, 6 + 1)}

        """
        If we engage with the signals in size order, we can deduce components
        as we iterate through
        """
        test_signals = sorted(test_signals, key=len)

        """
        Number 1 - Two Digits
        We know that Index 2 and 5 can only be one of two values
        """
        mapping[2] = set(sorted(test_signals[0]))
        mapping[5] = mapping[2]

        """
        Number 7 - Three Digits
        We know that Seven marks off Indexes 0, 2, and 5. Index 2 and 5 were established above
        This means we definitively know what Index 0 is
        """
        mapping[0] = set(sorted(test_signals[1])) - mapping[2]

        """
        Number 4 - Four Digits
        Since we know Indexes 2 and 5 were 50/50 set above, we have two possible solutions
        for Indexes 1 and 3 now.
        """
        mapping[1] = set(sorted(test_signals[2])) - mapping[2]
        mapping[3] = mapping[1]

        """
        Number 2, 3, or 5 - Five Digits
        These numbers all share their top, middle, and bottom segments, so we can deduce a bit
        We know the top (Index 0) from 7 earlier, so we can now 50/50
        the middle (Index 3) and bottom (Index 6) values
        """
        top_middle_bottom = (
            set(sorted(test_signals[3]))
            .intersection(set(sorted(test_signals[4])))
            .intersection(set(sorted(test_signals[5])))
        )
        mapping[3] = top_middle_bottom - mapping[0]
        mapping[6] = mapping[3]

        """
        Number 6, 9, or 0 - Six Digits
        We can determine the middle (Index 3) from the 0 case, as it will be the only
        number in 6 and 9 that don't have all top, middle, and bottom set and has only
        the middle value (Index 3) turned off.
        Since we now know the top and middle, we also implicitly know the bottom (Index 6) value.
        """
        for i in range(6, 8 + 1):
            if (
                top_middle_bottom.intersection(set(sorted(test_signals[i])))
                != top_middle_bottom
            ):
                mapping[3] = {"a", "b", "c", "d", "e", "f", "g"} - set(
                    sorted(test_signals[i])
                )
                mapping[6] -= mapping[3]
                break

        """
        Going back a bit, from the 4 case, we now know what Index 1 is, since we definitively
        know the right segments and the mid point.
        """
        mapping[1] -= mapping[3] - mapping[2] - mapping[5]

        """
        Since we know what Indices 0, 1, 3, and 6 definitively are,
        and what Indices 2 and 5 are (50/50), we know what Index 4 is by deduction. 
        """
        mapping[4] = (
            mapping[4] - mapping[0] - mapping[1] - mapping[3] - mapping[6] - mapping[2]
        )

        """
        Finally, we can determine what Indices 2 and 5 are by reading the number 5 from the input.
        The number 5 will be the only number in 2, 3, and 5 that doesn't have Index 1 set.
        Once we have the 5 case, we can finish our decoding by establishing what Indices 2 and 5 
        definitively are.
        """
        # We can determine 2/5 positioning from the "five" signal, as it will have 1 and 5
        for i in range(3, 5 + 1):
            if list(mapping[1])[0] in set(sorted(test_signals[i])):
                mapping[5] = (
                    set(sorted(test_signals[i]))
                    - mapping[0]
                    - mapping[3]
                    - mapping[6]
                    - mapping[1]
                )
                mapping[2] -= mapping[5]
                break

        """
        Now we need to construct a mapping between signals and the final results
        """
        top = list(mapping[0])[0]
        top_left = list(mapping[1])[0]
        top_right = list(mapping[2])[0]
        mid = list(mapping[3])[0]
        bottom_left = list(mapping[4])[0]
        bottom_right = list(mapping[5])[0]
        bottom = list(mapping[6])[0]

        decoded_operations = {
            tuple(sorted(top_right + bottom_right)): "1",
            tuple(sorted(top + top_right + mid + bottom_left + bottom)): "2",
            tuple(sorted(top + top_right + mid + bottom_right + bottom)): "3",
            tuple(sorted(top_left + top_right + mid + bottom_right)): "4",
            tuple(sorted(top + top_left + mid + bottom_right + bottom)): "5",
            tuple(
                sorted(top + top_left + mid + bottom_left + bottom_right + bottom)
            ): "6",
            tuple(sorted(top + top_right + bottom_right)): "7",
            tuple(
                sorted(
                    top
                    + top_left
                    + top_right
                    + mid
                    + bottom_left
                    + bottom_right
                    + bottom
                )
            ): "8",
            tuple(
                sorted(top + top_left + top_right + mid + bottom_right + bottom)
            ): "9",
            tuple(
                sorted(top + top_left + bottom_left + bottom + bottom_right + top_right)
            ): "0",
        }

        """
        The row has been fully decoded, lets get what 4 digit number we add to running total
        """
        answer_value_string = ""
        for digit in line[10:]:
            answer_value_string += decoded_operations[tuple(sorted(digit))]

        g_total += int(answer_value_string)

    return g_total


def main() -> None:
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
