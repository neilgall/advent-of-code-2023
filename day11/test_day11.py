import pytest
from .day11 import *


EXAMPLE = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def test_parse_and_expand():
    universe = Universe.parse(EXAMPLE)
    universe.expand(1)
    assert universe.extent == Size(12, 11)
    assert Galaxy(0, 4, 0) in universe.galaxies
    assert Galaxy(1, 9, 1) in universe.galaxies
    assert Galaxy(2, 0, 2) in universe.galaxies
    assert Galaxy(3, 8, 5) in universe.galaxies
    assert Galaxy(4, 1, 6) in universe.galaxies
    assert Galaxy(5, 12, 7) in universe.galaxies
    assert Galaxy(6, 9, 10) in universe.galaxies
    assert Galaxy(7, 0, 11) in universe.galaxies
    assert Galaxy(8, 5, 11) in universe.galaxies


@pytest.mark.parametrize(
    "src,dest,distance",
    [
        (Pos(1, 6), Pos(5, 11), 9),
        (Pos(4, 0), Pos(9, 10), 15),
        (Pos(0, 2), Pos(12, 7), 17),
        (Pos(0, 11), Pos(5, 11), 5),
    ],
)
def test_path_distance_to(src, dest, distance):
    assert src.path_distance_to(dest) == distance


def test_part1():
    assert part1(EXAMPLE) == 374


@pytest.mark.parametrize("expand,total", [(10, 1030), (100, 8410)])
def test_part2(expand, total):
    assert part2(EXAMPLE, expand) == total
