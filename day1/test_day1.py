import pytest
from day1 import parse_line_part1, parse_line_part2, calibration_value, Input, calculate


@pytest.mark.parametrize(
    "input,expect",
    [
        ("1abc2", [1, 2]),
        ("pqr3stu8vwx", [3, 8]),
        ("a1b2c3d4e5f", [1, 2, 3, 4, 5]),
        ("treb7uchet", [7]),
    ],
)
def test_parse_line_part1(input: str, expect: list[int]):
    assert parse_line_part1(input) == expect


@pytest.mark.parametrize(
    "input,expect",
    [
        ("two1nine", [2, 1, 9]),
        ("eightwothree", [8, 2, 3]),
        ("abcone2threexyz", [1, 2, 3]),
        ("xtwone3four", [2, 1, 3, 4]),
        ("4nineeightseven2", [4, 9, 8, 7, 2]),
        ("zoneight234", [1, 8, 2, 3, 4]),
        ("7pqrstsixteen", [7, 6]),
    ],
)
def test_parse_line_part2(input: str, expect: list[int]):
    assert parse_line_part2(input) == expect


@pytest.mark.parametrize(
    "input,expect", [([1, 2], 12), ([3, 8], 38), ([1, 2, 3, 4, 5], 15), ([7], 77)]
)
def test_calibration_value(input: Input, expect: int):
    assert calibration_value(input) == expect


def test_part1():
    result = calculate(
        ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"], parse_line_part1
    )
    assert result == 142


def test_part2():
    result = calculate(
        [
            "two1nine",
            "eightwothree",
            "abcone2threexyz",
            "xtwone3four",
            "4nineeightseven2",
            "zoneight234",
            "7pqrstsixteen",
        ],
        parse_line_part2,
    )
    assert result == 281
