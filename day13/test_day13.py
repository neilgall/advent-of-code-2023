import pytest
from .day13 import *


EXAMPLE = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def test_find_reflection_in_grid():
    [grid1, grid2] = list(parse_input(EXAMPLE))
    assert find_reflection_in_grid(grid1) == 5
    assert find_reflection_in_grid(transpose(grid2)) == 4


def test_part1():
    assert part1(EXAMPLE) == 405


def test_part2():
    assert part2(EXAMPLE) == 0
