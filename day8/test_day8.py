import pytest
from .day8 import *


EXAMPLE = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

EXAMPLE2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


def test_parser():
    document = Document.parse(EXAMPLE)
    assert document == Document(
        directions = [Direction.RIGHT, Direction.LEFT],
        network = {
            "AAA": ("BBB", "CCC"),
            "BBB": ("DDD", "EEE"),
            "CCC": ("ZZZ", "GGG"),
            "DDD": ("DDD", "DDD"),
            "EEE": ("EEE", "EEE"),
            "GGG": ("GGG", "GGG"),
            "ZZZ": ("ZZZ", "ZZZ")
        }
    )



@pytest.mark.parametrize("input,steps", [
    (EXAMPLE, 2),
    (EXAMPLE2, 6),
])
def test_part1(input, steps):
    assert part1(input) == steps


def test_part2():
    assert part2(EXAMPLE) == 0
