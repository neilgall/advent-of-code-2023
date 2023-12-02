import pytest
from day1 import parse_line, calibration_value, Input, part1


@pytest.mark.parametrize("input,expect", [
    ("1abc2", [1,2]),
    ("pqr3stu8vwx", [3,8]), 
    ("a1b2c3d4e5f", [1,2,3,4,5]),
    ("treb7uchet", [7])
])
def test_parse_line(input: str, expect: list[int]):
    assert parse_line(input) == expect


@pytest.mark.parametrize("input,expect", [
    ([1,2], 12),
    ([3,8], 38), 
    ([1,2,3,4,5], 15),
    ([7], 77)
])
def test_calibration_value(input: Input, expect: int):
    assert calibration_value(input) == expect


def test_part1():
    result = part1(["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"])
    assert result == 142
