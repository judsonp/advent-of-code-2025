from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(order = True, frozen = True)
class InclusiveRange:
    lower: int
    upper: int

    def contains(self, n: int) -> bool:
        return self.lower <= n <= self.upper

    def size(self) -> int:
        return self.upper - self.lower + 1

    def overlaps(self, other: "InclusiveRange") -> bool:
        return self.lower <= other.lower <= self.upper or \
               self.lower <= other.upper <= self.upper

    def merge(self, other: "InclusiveRange") -> "InclusiveRange":
        return InclusiveRange(min(self.lower, other.lower),
                              max(self.upper, other.upper))

    def __repr__(self) -> str:
        return f"{self.lower}-{self.upper}"


@dataclass(frozen = True)
class Input:
    ranges: List[InclusiveRange]
    items: List[int]


def merge_ranges(ranges: List[InclusiveRange]) -> List[InclusiveRange]:
    sorted_ranges = sorted(ranges)
    merged_ranges = []
    cur = None
    for rng in sorted_ranges:
        if cur is None:
            cur = rng
        elif cur.overlaps(rng):
            cur = cur.merge(rng)
        else:
            merged_ranges.append(cur)
            cur = rng
    if cur is not None:
        merged_ranges.append(cur)
    return merged_ranges


def part_one(data: Input) -> int:
    fresh = 0
    for item in data.items:
        if any(rng.contains(item) for rng in data.ranges):
            fresh += 1
    return fresh


def part_two(data: Input) -> int:
    return sum(rng.size() for rng in merge_ranges(data.ranges))


def parse(data: str) -> Input:
    range_text, item_text = data.split("\n\n", 1)
    text_ranges = range_text.splitlines()
    tuple_ranges = [tuple(r.split("-", 1)) for r in text_ranges]
    ranges = [InclusiveRange(int(x), int(y)) for (x, y) in tuple_ranges]
    items = [int(x) for x in item_text.splitlines()]
    return Input(ranges, items)


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = parse(f.read())
    assert part_one(data) == 3


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = parse(f.read())
    assert part_two(data) == 14


def test_check_parse() -> None:
    with Path("example.txt").open() as f:
        data = parse(f.read())
    assert(len(data.ranges) == 4)
    assert(len(data.items) == 6)


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = parse(f.read())

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
