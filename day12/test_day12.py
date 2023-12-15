import pytest
from .day12 import *


EXAMPLE = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


@pytest.mark.parametrize("input,expect", [
    ("???.### 1,1,3", SpringRow("UUUODDD", [1,1,3])),
    (".??..??...?##. 1,1,3", SpringRow("OUUOOUUOOOUDDO", [1,1,3]))
])
def test_from_string(input, expect):
    row = SpringRow.from_string(input)
    assert row == expect


@pytest.mark.parametrize("input,count", [
    ("#.#.### 1,1,3", 1)
])
def test_group_matching(input, count):
    row = parse_input(input)[0]
    assert row.matches() == count


def test_part1():
    assert part1(EXAMPLE) == 0


def test_part2():
    assert part2(EXAMPLE) == 0
