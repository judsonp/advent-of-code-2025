from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def rectangle_area(self, other: "Point") -> int:
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


def part_one(data: List[str]) -> int:
    points = [Point(*[int(x) for x in line.split(",")]) for line in data]
    return max(a.rectangle_area(b) for a, b in product(points, repeat = 2))


def part_two(data: List[str]) -> int:
    return 0


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    assert part_one(data) == 50


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    # assert part_two(data) == 0


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = f.read().splitlines()

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
