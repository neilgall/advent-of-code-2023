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

    def translate(self, value: int) -> int | None:
        if value in range(self.source_range_start, self.source_range_start + self.range_length):
            return self.destination_range_start + value - self.source_range_start


@dataclass
class CategoryMap:
    source_category: Category
    destination_category: Category
    mappings: list[RangeMapping]

    def translate(self, value: int) -> int:
        for mapping in self.mappings:
            result = mapping.translate(value)
            if result:
                return result
        return value


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

    def find(self, destination_category: Category, source_category: Category, source_value: int) -> int:
        category = source_category
        value = source_value
        while category != destination_category:
            category_map = next(cm for cm in self.category_maps if cm.source_category == category)
            value = category_map.translate(value)
            category = category_map.destination_category
        return value


def part1(input: str) -> int:
    almanac = Almanac.parse(input)
    return min(almanac.find(Category.LOCATION, Category.SEED, seed) for seed in almanac.seeds_to_plant)


def part2(input:str) -> int:
    return 0
