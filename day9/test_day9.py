import pytest
from .day9 import *


EXAMPLE = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def test_parse():
    h = History.from_string("0 3 6 9 12 15")
    assert h.values == [0, 3, 6, 9, 12, 15]


def test_diff():
    h = History([0, 3, 6, 9, 12, 15])
    assert h.diff().values == [3, 3, 3, 3, 3]


@pytest.mark.parametrize("input,expect", [
    ([0, 3, 6, 9, 12, 15], 18),
    ([1, 3, 6, 10, 15, 21], 28),
    ([10, 13, 16, 21, 30, 45], 68)
])
def test_predict(input,expect):
    h = History(input)
    assert h.predict() == expect


def test_part1():
    assert part1(EXAMPLE) == 114


def test_part2():
    assert part2(EXAMPLE) == 0
