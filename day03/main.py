from pathlib import Path
from typing import List


def bank_joltage(bank: str) -> int:
    first_pos, first = max(enumerate(int(x) for x in iter(bank[:-1])), key=lambda x: x[1])
    _, second = max(enumerate(int(x) for x in iter(bank[first_pos+1:])), key=lambda x: x[1])
    return first * 10 + second


def part_one(banks: List[str]) -> int:
    return sum(bank_joltage(bank) for bank in banks)


def part_two(banks: List[str]) -> int:
    return 0


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    assert part_one(data) == 357


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    # assert part_two(data) == 0


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = f.read().splitlines()

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
