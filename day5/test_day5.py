import pytest
from .day5 import *

EXAMPLE = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def test_parser():
    almanac = Almanac.parse(EXAMPLE)
    assert almanac == Almanac(
        seeds_list=[79, 14, 55, 13],
        category_maps=[
            CategoryMap(
                source_category=Category.SEED,
                destination_category=Category.SOIL,
                mappings=[
                    RangeMapping(
                        destination_range_start=50,
                        source_range_start=98,
                        range_length=2,
                    ),
                    RangeMapping(
                        destination_range_start=52,
                        source_range_start=50,
                        range_length=48,
                    ),
                ],
            ),
            CategoryMap(
                source_category=Category.SOIL,
                destination_category=Category.FERTILIZER,
                mappings=[
                    RangeMapping(
                        destination_range_start=0,
                        source_range_start=15,
                        range_length=37,
                    ),
                    RangeMapping(
                        destination_range_start=37,
                        source_range_start=52,
                        range_length=2,
                    ),
                    RangeMapping(
                        destination_range_start=39,
                        source_range_start=0,
                        range_length=15,
                    ),
                ],
            ),
            CategoryMap(
                source_category=Category.FERTILIZER,
                destination_category=Category.WATER,
                mappings=[
                    RangeMapping(
                        destination_range_start=49,
                        source_range_start=53,
                        range_length=8,
                    ),
                    RangeMapping(
                        destination_range_start=0,
                        source_range_start=11,
                        range_length=42,
                    ),
                    RangeMapping(
                        destination_range_start=42, source_range_start=0, range_length=7
                    ),
                    RangeMapping(
                        destination_range_start=57, source_range_start=7, range_length=4
                    ),
                ],
            ),
            CategoryMap(
                source_category=Category.WATER,
                destination_category=Category.LIGHT,
                mappings=[
                    RangeMapping(
                        destination_range_start=88,
                        source_range_start=18,
                        range_length=7,
                    ),
                    RangeMapping(
                        destination_range_start=18,
                        source_range_start=25,
                        range_length=70,
                    ),
                ],
            ),
            CategoryMap(
                source_category=Category.LIGHT,
                destination_category=Category.TEMPERATURE,
                mappings=[
                    RangeMapping(
                        destination_range_start=45,
                        source_range_start=77,
                        range_length=23,
                    ),
                    RangeMapping(
                        destination_range_start=81,
                        source_range_start=45,
                        range_length=19,
                    ),
                    RangeMapping(
                        destination_range_start=68,
                        source_range_start=64,
                        range_length=13,
                    ),
                ],
            ),
            CategoryMap(
                source_category=Category.TEMPERATURE,
                destination_category=Category.HUMIDITY,
                mappings=[
                    RangeMapping(
                        destination_range_start=0, source_range_start=69, range_length=1
                    ),
                    RangeMapping(
                        destination_range_start=1, source_range_start=0, range_length=69
                    ),
                ],
            ),
            CategoryMap(
                source_category=Category.HUMIDITY,
                destination_category=Category.LOCATION,
                mappings=[
                    RangeMapping(
                        destination_range_start=60,
                        source_range_start=56,
                        range_length=37,
                    ),
                    RangeMapping(
                        destination_range_start=56,
                        source_range_start=93,
                        range_length=4,
                    ),
                ],
            ),
        ],
    )


@pytest.mark.parametrize(
    "source,destination", [(98, 50), (99, 51), (97, None), (100, None)]
)
def test_range_mapping_integers(source: int, destination: int | None):
    map = RangeMapping(
        destination_range_start=50, source_range_start=98, range_length=2
    )
    assert map.translate(source) == destination


@pytest.mark.parametrize(
    "mappings,source,destination",
    [
        (
            [RangeMapping(50, 98, 2), RangeMapping(52, 50, 48)],
            range(0, 110),
            [range(0, 50), range(52, 100), range(50, 52), range(100, 110)],
        )
    ],
)
def test_range_mapping_ranges(
    mappings: list[RangeMapping], source: range, destination: list[range]
):
    map = CategoryMap(
        source_category=Category.SOIL,
        destination_category=Category.SOIL,
        mappings=mappings,
    )
    assert list(map.translate_range(source)) == destination


@pytest.mark.parametrize(
    "source,destination", [(98, 50), (99, 51), (53, 55), (110, 110)]
)
def test_category_map(source: int, destination: int):
    map = CategoryMap(
        source_category=Category.SEED,
        destination_category=Category.SOIL,
        mappings=[
            RangeMapping(
                destination_range_start=50, source_range_start=98, range_length=2
            ),
            RangeMapping(
                destination_range_start=52, source_range_start=50, range_length=48
            ),
        ],
    )
    assert map.translate(source) == destination


@pytest.mark.parametrize("seed,location", [(79, 82), (14, 43), (55, 86), (13, 35)])
def test_almanac_find(seed: int, location: int):
    almanac = Almanac.parse(EXAMPLE)
    assert almanac.find(Category.LOCATION, Category.SEED, seed) == location


def test_part1():
    assert part1(EXAMPLE) == 35


def test_part2():
    assert part2(EXAMPLE) == 46
