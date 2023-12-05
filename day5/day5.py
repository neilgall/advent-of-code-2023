from enum import Enum
from dataclasses import dataclass
from parsy import decimal_digit, from_enum, seq, string, whitespace

class Category(Enum):
    SEED = "seed"
    SOIL = "soil"
    FERTILIZER = "fertilizer"
    WATER = "water"
    LIGHT = "light"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    LOCATION = "location"

@dataclass
class RangeMapping:
    destination_range_start: int
    source_range_start: int
    range_length: int


@dataclass
class CategoryMap:
    source_category: Category
    destination_category: Category
    mappings: list[RangeMapping]


@dataclass
class Almanac:
    seeds_to_plant: list[int]
    category_maps: list[CategoryMap]

    @classmethod
    def parse(cls, input: str) -> "Almanac":
        integer = decimal_digit.at_least(1).map(lambda ds: int("".join(ds)))
        integer_list = integer.sep_by(whitespace)
        seeds_list = string("seeds:") >> whitespace >> integer_list
        range_mapping = seq(integer << whitespace, integer << whitespace, integer).combine(RangeMapping)
        category_map = seq(
            from_enum(Category) << string("-to-"),
            from_enum(Category) << whitespace << string("map:") << whitespace,
            range_mapping.sep_by(whitespace)
        ).combine(CategoryMap)
        almanac = seq(seeds_list << whitespace, category_map.sep_by(whitespace)).combine(Almanac)
        return almanac.parse(input.strip())


def part1(input: str) -> int:
    return 0


def part2(input:str) -> int:
    return 0
