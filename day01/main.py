from pathlib import Path
from typing import List


def part_one(data: List[str]) -> int:
    split_data = [(x[:1], x[1:]) for x in data]
    int_data = [
        int(amount) if direction == "R" else -int(amount)
        for (direction, amount) in split_data
    ]
    dial = 50
    password = 0
    for turn in int_data:
        dial += turn
        dial %= 100
        if dial == 0:
            password += 1
    return password


def signum(n: int) -> int:
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0

def part_two(data: List[str]) -> int:
    split_data = [(x[:1], x[1:]) for x in data]
    int_data = [
        int(amount) if direction == "R" else -int(amount)
        for (direction, amount) in split_data
    ]
    dial = 50
    password = 0
    for turn in int_data:
        direction = signum(turn)
        for _ in range(abs(turn)):
            dial = (dial + direction) % 100
            if dial == 0:
                password += 1
    return password

def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    assert part_one(data) == 3


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    assert part_two(data) == 6


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = f.read().splitlines()

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
