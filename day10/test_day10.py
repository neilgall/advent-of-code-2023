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

PART2_EXAMPLE = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

PART2_EXAMPLE_WITH_SQUEEZING = """
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
"""

PART2_LARGE_EXAMPLE = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

PART2_LARGE_EXAMPLE2 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
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
        extent=Pos(4, 4),
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
        extent=Pos(4, 4),
    )


@pytest.mark.parametrize(
    "input,pos,distance",
    [(EXAMPLE_WITH_START, Pos(3, 3), 4), (COMPLEX_EXAMPLE, Pos(4, 2), 8)],
)
def test_find_furthest_tile_from_start(input, pos, distance):
    field = Field.parse(input)
    assert field.find_furthest_tile_from_start() == (pos, distance)


@pytest.mark.parametrize(
    "input,positions",
    [
        (
            EXAMPLE_WITH_START,
            [
                Pos(1, 1),
                Pos(2, 1),
                Pos(3, 1),
                Pos(1, 2),
                Pos(3, 2),
                Pos(1, 3),
                Pos(2, 3),
                Pos(3, 3),
            ],
        ),
        (
            COMPLEX_EXAMPLE,
            [
                Pos(2, 0),
                Pos(3, 0),
                Pos(1, 1),
                Pos(2, 1),
                Pos(3, 1),
                Pos(0, 2),
                Pos(1, 2),
                Pos(3, 2),
                Pos(4, 2),
                Pos(0, 3),
                Pos(1, 3),
                Pos(2, 3),
                Pos(3, 3),
                Pos(4, 3),
                Pos(0, 4),
                Pos(1, 4),
            ],
        ),
    ],
)
def test_find_loop(input, positions):
    field = Field.parse(input)
    assert field.find_loop() == positions


def test_is_inside_loop():
    field = Field.parse(PART2_EXAMPLE)
    assert field.is_inside_loop(Pos(0, 0)) == (False, set())
    assert field.is_inside_loop(Pos(2, 6)) == (True, set([Pos(2, 6), Pos(3, 6)]))
    assert field.is_inside_loop(Pos(3, 6)) == (True, set([Pos(2, 6), Pos(3, 6)]))
    assert field.is_inside_loop(Pos(7, 6)) == (True, set([Pos(7, 6), Pos(8, 6)]))
    assert field.is_inside_loop(Pos(8, 6)) == (True, set([Pos(7, 6), Pos(8, 6)]))


@pytest.mark.parametrize(
    "input,count",
    [
        (PART2_EXAMPLE, 4),
        (PART2_EXAMPLE_WITH_SQUEEZING, 12),
    ],
)
def test_positions_enclosed_by_loop(input, count):
    field = Field.parse(input)
    positions = list(field.positions_enclosed_by_loop())
    assert len(positions) == count


@pytest.mark.parametrize(
    "input,count",
    [
        (PART2_EXAMPLE, 4),
        (PART2_EXAMPLE_WITH_SQUEEZING, 4),
    ],
)
def test_positions_enclosed_by_loop_with_squeezing(input, count):
    field = Field.parse(input)
    positions = list(field.positions_enclosed_by_loop_with_squeezing())
    assert len(positions) == count


def test_part1():
    assert part1(COMPLEX_EXAMPLE) == 8


@pytest.mark.parametrize(
    "input,count",
    [
        (PART2_LARGE_EXAMPLE, 8),
        (PART2_LARGE_EXAMPLE2, 10),
    ],
)
def test_part2(input, count):
    assert part2(input) == count
