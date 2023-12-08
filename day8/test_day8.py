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

EXAMPLE3 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


def test_parser():
    document = Document.parse(EXAMPLE)
    assert document == Document(
        directions=[Direction.RIGHT, Direction.LEFT],
        network={
            "AAA": ("BBB", "CCC"),
            "BBB": ("DDD", "EEE"),
            "CCC": ("ZZZ", "GGG"),
            "DDD": ("DDD", "DDD"),
            "EEE": ("EEE", "EEE"),
            "GGG": ("GGG", "GGG"),
            "ZZZ": ("ZZZ", "ZZZ"),
        },
    )


def test_start_nodes():
    document = Document.parse(EXAMPLE3)
    assert document.start_nodes() == ["11A", "22A"]


@pytest.mark.parametrize(
    "input,steps",
    [
        (EXAMPLE, 2),
        (EXAMPLE2, 6),
    ],
)
def test_part1(input, steps):
    assert part1(input) == steps


def test_part2():
    assert part2(EXAMPLE3) == 6
