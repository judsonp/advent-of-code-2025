from pathlib import Path
from typing import Dict, List


def part_one(data: List[str]) -> int:
    initial_line = data[0]
    data = data[1:]
    start_pos = initial_line.index("S")
    num_splits = 0
    beam_cols = {start_pos}

    for row in data:
        splitter_locs = {i for i, c in enumerate(row) if c == "^"}
        new_beam_cols = set()
        for col in beam_cols:
            if col in splitter_locs:
                new_beam_cols.add(col + 1)
                new_beam_cols.add(col - 1)
                num_splits += 1
            else:
                new_beam_cols.add(col)
        beam_cols = new_beam_cols

    return num_splits


def addsert(d: Dict[int, int], k: int, v: int) -> None:
    if k not in d:
        d[k] = 0
    d[k] += v


def part_two(data: List[str]) -> int:
    initial_line = data[0]
    data = data[1:]
    start_pos = initial_line.index("S")
    timelines = {start_pos: 1}

    for row in data:
        splitter_locs = {i for i, c in enumerate(row) if c == "^"}
        new_timelines: Dict[int, int] = {}
        for col, count in timelines.items():
            if col in splitter_locs:
                addsert(new_timelines, col + 1, count)
                addsert(new_timelines, col - 1, count)
            else:
                addsert(new_timelines, col, count)
        timelines = new_timelines

    return sum(timelines.values())

def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    assert part_one(data) == 21


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    assert part_two(data) == 40


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = f.read().splitlines()

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
