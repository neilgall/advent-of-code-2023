import pytest
from .day6 import *


EXAMPLE = """
Time:      7  15   30
Distance:  9  40  200
"""


def test_parser():
    races = parse_input(EXAMPLE)
    assert races == [Race(7, 9), Race(15, 40), Race(30, 200)]


def test_parser2():
    race = parse_input2(EXAMPLE)
    assert race == Race(71530, 940200)


def test_part1():
    assert part1(EXAMPLE) == 288


def test_part2():
    assert part2(EXAMPLE) == 71503
