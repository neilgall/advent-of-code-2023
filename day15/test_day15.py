import pytest
from .day15 import *


EXAMPLE = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

def test_hash():
    assert hash("HASH") == 52


def test_parse_instructions():
    instructions = parse_instructions(EXAMPLE)
    assert instructions == [
        ReplaceInstruction(label="rn", focal_length=1),
        RemoveInstruction(label="cm"),
        ReplaceInstruction(label="qp", focal_length=3),
        ReplaceInstruction(label="cm", focal_length=2),
        RemoveInstruction(label="qp"),
        ReplaceInstruction(label="pc", focal_length=4),
        ReplaceInstruction(label="ot", focal_length=9),
        ReplaceInstruction(label="ab", focal_length=5),
        RemoveInstruction(label="pc"),
        ReplaceInstruction(label="pc", focal_length=6),
        ReplaceInstruction(label="ot", focal_length=7),
    ]


def test_part1():
    assert part1(EXAMPLE) == 1320


def test_part2():
    assert part2(EXAMPLE) == 145
