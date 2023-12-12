import pytest
from .day12 import *


EXAMPLE = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

def test_parser():
    rows = parse_input(EXAMPLE)
    assert rows == [
        SpringRow(
            springs=[
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.OPERATIONAL,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.DAMAGED
            ],
            groups=[1,1,3]
        ),
        SpringRow(
            springs=[
                Spring.OPERATIONAL,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.OPERATIONAL,
                Spring.OPERATIONAL,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.OPERATIONAL,
                Spring.OPERATIONAL,
                Spring.OPERATIONAL,
                Spring.UNKNOWN,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.OPERATIONAL
            ],
            groups=[1,1,3]
        ),
        SpringRow(
            springs=[
                Spring.UNKNOWN,
                Spring.DAMAGED,
                Spring.UNKNOWN,
                Spring.DAMAGED,
                Spring.UNKNOWN,
                Spring.DAMAGED,
                Spring.UNKNOWN,
                Spring.DAMAGED,
                Spring.UNKNOWN,
                Spring.DAMAGED,
                Spring.UNKNOWN,
                Spring.DAMAGED,
                Spring.UNKNOWN,
                Spring.DAMAGED,
                Spring.UNKNOWN,                
            ],
            groups=[1,3,1,6]
        ),
        SpringRow(
            springs=[
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.OPERATIONAL,
                Spring.DAMAGED,
                Spring.OPERATIONAL,
                Spring.OPERATIONAL,
                Spring.OPERATIONAL,
                Spring.DAMAGED,
                Spring.OPERATIONAL,
                Spring.OPERATIONAL,
                Spring.OPERATIONAL,
            ],
            groups=[4,1,1]
        ),
        SpringRow(
            springs=[
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.OPERATIONAL,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.OPERATIONAL,
                Spring.OPERATIONAL,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.OPERATIONAL
            ],
            groups=[1,6,5]
        ),
        SpringRow(
            springs=[
                Spring.UNKNOWN,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.DAMAGED,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
                Spring.UNKNOWN,
            ],
            groups=[3,2,1]
        )
    ]

def test_part1():
    assert part1(EXAMPLE) == 0


def test_part2():
    assert part2(EXAMPLE) == 0
