from day15 import part1, part2


if __name__ == "__main__":
    with open("day15/input.txt", "rt") as f:
        input = f.read()

    print(f"Part 1: {part1(input)}")
    print(f"Part 2: {part2(input)}")
