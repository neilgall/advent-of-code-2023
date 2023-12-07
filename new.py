#!/usr/bin/env python
from datetime import datetime
from pathlib import Path


if __name__ == "__main__":
    today = f"day{datetime.now().day}"
    dir = Path(today)

    dir.mkdir(parents=True)
    (dir / "__init__.py").touch()

    (dir / f"{today}.py").write_text(
        """
def part1(input: str) -> int:
    return 0


def part2(input: str) -> int:
    return 0
"""
    )

    (dir / f"test_{today}.py").write_text(
        f'''import pytest
from .{today} import *


EXAMPLE = """
"""


def test_part1():
    assert part1(EXAMPLE) == 0


def test_part2():
    assert part2(EXAMPLE) == 0
'''
    )

    (dir / "__main__.py").write_text(
        f"""from {today} import part1, part2


if __name__ == "__main__":
    with open("{today}/input.txt", "rt") as f:
        input = f.read()

    print(f"Part 1: {{part1(input)}}")
    print(f"Part 2: {{part2(input)}}")
"""
    )
