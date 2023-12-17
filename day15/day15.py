
def hash(input: str) -> int:
    value = 0
    for c in input:
        value = ((value + ord(c)) * 17) % 256
    return value


def part1(input: str) -> int:
    return sum(hash(part) for part in input.strip().split(","))


def part2(input: str) -> int:
    return 0
