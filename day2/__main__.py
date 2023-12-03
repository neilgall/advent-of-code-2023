from day2 import parse_game, part1, part2

if __name__ == "__main__":
    with open("day2/input.txt", "rt") as f:
        input = [parse_game(l.strip()) for l in f.readlines()]

    print(f"Part 1: {part1(input)}")
    print(f"Part 2: {part2(input)}")
