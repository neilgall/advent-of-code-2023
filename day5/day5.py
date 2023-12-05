from enum import Enum
from dataclasses import dataclass
from itertools import batched
from parsy import decimal_digit, from_enum, seq, string, whitespace
from typing import Generator, Iterable
from sys import maxsize


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
        if value in self.source_range:
            return value + self.destination_range_start - self.source_range_start

    @property
    def source_range(self) -> range:
        return range(
            self.source_range_start, self.source_range_start + self.range_length
        )


@dataclass
class CategoryMap:
    source_category: Category
    destination_category: Category
    mappings: list[RangeMapping]

    def translate(self, value: int) -> int:
        translations = (m.translate(value) for m in self.mappings)
        valid_translations = (v for v in translations if v is not None)
        return next(valid_translations, value)

    def translate_range(self, value: range) -> Generator[range, None, None]:
        candidate_breaks = set(
            [
                value.start,
                value.stop,
                *(m.source_range.start for m in self.mappings),
                *(m.source_range.stop for m in self.mappings),
            ]
        )
        breaks = sorted([b for b in candidate_breaks if value.start <= b <= value.stop])
        start = breaks[0]
        for b in breaks[1:]:
            yield range(self.translate(start), self.translate(b - 1) + 1)
            start = b


@dataclass
class Almanac:
    seeds_list: list[int]
    category_maps: list[CategoryMap]

    @classmethod
    def parse(cls, input: str) -> "Almanac":
        integer = decimal_digit.at_least(1).map(lambda ds: int("".join(ds)))
        integer_list = integer.sep_by(whitespace)
        seeds_list = string("seeds:") >> whitespace >> integer_list
        range_mapping = seq(
            integer << whitespace, integer << whitespace, integer
        ).combine(RangeMapping)
        category_map = seq(
            from_enum(Category) << string("-to-"),
            from_enum(Category) << whitespace << string("map:") << whitespace,
            range_mapping.sep_by(whitespace),
        ).combine(CategoryMap)
        almanac = seq(
            seeds_list << whitespace, category_map.sep_by(whitespace)
        ).combine(Almanac)
        return almanac.parse(input.strip())

    def mapping_from(self, category: Category) -> CategoryMap:
        return next(cm for cm in self.category_maps if cm.source_category == category)

    def find(
        self,
        destination_category: Category,
        source_category: Category,
        source_value: int,
    ) -> int:
        if source_category == destination_category:
            return source_value
        else:
            category_map = self.mapping_from(source_category)
            return self.find(
                destination_category=destination_category,
                source_category=category_map.destination_category,
                source_value=category_map.translate(source_value),
            )

    def find_range(
        self,
        destination_category: Category,
        source_category: Category,
        source_range: range,
    ) -> Generator[range, None, None]:
        if source_category == destination_category:
            yield source_range
        else:
            category_map = self.mapping_from(source_category)
            for destination_range in category_map.translate_range(source_range):
                yield from self.find_range(
                    destination_category=destination_category,
                    source_category=category_map.destination_category,
                    source_range=destination_range,
                )


def part1(input: str) -> int:
    almanac = Almanac.parse(input)
    return min(
        almanac.find(Category.LOCATION, Category.SEED, seed)
        for seed in almanac.seeds_list
    )


def part2(input: str) -> int:
    almanac = Almanac.parse(input)

    def find_location_ranges():
        seed_ranges = [
            range(start, start + length)
            for start, length in batched(almanac.seeds_list, 2)
        ]
        for seed_range in seed_ranges:
            yield from almanac.find_range(Category.LOCATION, Category.SEED, seed_range)

    ranges = find_location_ranges()
    return min(r.start for r in ranges)
