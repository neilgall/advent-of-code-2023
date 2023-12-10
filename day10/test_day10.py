import pytest
from .day10 import *


EXAMPLE = """
.....
.F-7.
.|.|.
.L-J.
.....
"""

EXAMPLE_WITH_START = """
.....
.S-7.
.|.|.
.L-J.
.....
"""

COMPLEX_EXAMPLE = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""


def test_parser():
    field = Field.parse(EXAMPLE)
    assert field == Field(
        tiles={
            Pos(1, 1): Tile(connected=Directions.SOUTH | Directions.EAST),
            Pos(2, 1): Tile(connected=Directions.EAST | Directions.WEST),
            Pos(3, 1): Tile(connected=Directions.SOUTH | Directions.WEST),
            Pos(1, 2): Tile(connected=Directions.NORTH | Directions.SOUTH),
            Pos(3, 2): Tile(connected=Directions.NORTH | Directions.SOUTH),
            Pos(1, 3): Tile(connected=Directions.NORTH | Directions.EAST),
            Pos(2, 3): Tile(connected=Directions.EAST | Directions.WEST),
            Pos(3, 3): Tile(connected=Directions.NORTH | Directions.WEST),
        },
        start=Pos(0, 0),
    )


def test_infer_connections():
    field = Field.parse(EXAMPLE_WITH_START)
    assert field == Field(
        tiles={
            Pos(1, 1): Tile(connected=Directions.SOUTH | Directions.EAST),
            Pos(2, 1): Tile(connected=Directions.EAST | Directions.WEST),
            Pos(3, 1): Tile(connected=Directions.SOUTH | Directions.WEST),
            Pos(1, 2): Tile(connected=Directions.NORTH | Directions.SOUTH),
            Pos(3, 2): Tile(connected=Directions.NORTH | Directions.SOUTH),
            Pos(1, 3): Tile(connected=Directions.NORTH | Directions.EAST),
            Pos(2, 3): Tile(connected=Directions.EAST | Directions.WEST),
            Pos(3, 3): Tile(connected=Directions.NORTH | Directions.WEST),
        },
        start=Pos(1, 1),
    )


@pytest.mark.parametrize(
    "input,pos,distance",
    [(EXAMPLE_WITH_START, Pos(3, 3), 4), (COMPLEX_EXAMPLE, Pos(4, 2), 8)],
)
def test_find_furthest_tile_from_start(input, pos, distance):
    field = Field.parse(input)
    assert field.find_furthest_tile_from_start() == (pos, distance)


def test_part1():
    assert part1(COMPLEX_EXAMPLE) == 8


def test_part2():
    assert part2(EXAMPLE) == 0
