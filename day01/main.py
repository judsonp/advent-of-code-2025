from pathlib import Path
from typing import List


def parse(data: List[str]) -> List[int]:
    split_data = [(x[:1], x[1:]) for x in data]
    return [
        int(amount) if direction == "R" else -int(amount)
        for (direction, amount) in split_data
    ]


def part_one(data: List[str]) -> int:
    turns = parse(data)
    dial = 50
    password = 0
    for turn in turns:
        dial += turn
        dial %= 100
        if dial == 0:
            password += 1
    return password


def part_two(data: List[str]) -> int:
    turns = parse(data)
    dial = 50
    password = 0
    for turn in turns:
        # If we start from zero and turn left, divmod will produce 1 just to get the
        # dial positive again, even though we didn't cross zero.
        # In this case, adjust the starting dial position to 100 (which is the same mod
        # 100) so that we don't count this one.
        if dial == 0 and turn < 0:
            dial = 100

        password_delta, dial = divmod(dial + turn, 100)
        password_delta = abs(password_delta)

        # If we turn left and land on exactly zero, divmod won't notice, but it counts.
        # If we turned right, it will have already counted it.
        if turn < 0 and dial == 0:
            password_delta += 1

        password += password_delta
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
