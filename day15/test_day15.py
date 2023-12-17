import pytest
from .day15 import *


EXAMPLE = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

def test_hash():
    assert hash("HASH") == 52


def test_part1():
    assert part1(EXAMPLE) == 1320


def test_part2():
    assert part2(EXAMPLE) == 0
