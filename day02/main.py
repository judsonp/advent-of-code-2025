from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import Iterator, List


@dataclass(order = True, frozen = True)
class InclusiveRange:
    lower: int
    upper: int

    def contains(self, n: int) -> bool:
        return self.lower <= n <= self.upper

    def __repr__(self) -> str:
        return f"{self.lower}-{self.upper}"


def num_digits(n: int) -> int:
    return len(str(abs(n)))


def split_range(r: InclusiveRange) -> Iterator[InclusiveRange]:
    min_digits = num_digits(r.lower)
    max_digits = num_digits(r.upper)
    digits = min_digits
    while digits <= max_digits:
        lower = 10 ** (digits - 1)
        if digits == min_digits:
            lower = r.lower
        upper = (10 ** digits) - 1
        if digits == max_digits:
            upper = r.upper
        yield InclusiveRange(lower, upper)
        digits += 1


def half_range(r: InclusiveRange) -> InclusiveRange:
    # r.lower and r.upper must be the same number of digits
    # and must be an even number of digits
    half_len = num_digits(r.lower) // 2
    lower = str(r.lower)[:half_len]
    upper = str(r.upper)[:half_len]
    return InclusiveRange(int(lower), int(upper))


def expand_half_to_invalid(half: int) -> int:
    # half must be positive
    return int(f"{half}{half}")


def truncated_range(r: InclusiveRange, sublen: int) -> InclusiveRange:
    # r.lower and r.upper must be the same number of digits
    # and must be evenly divisible by sublen
    lower = str(r.lower)[:sublen]
    upper = str(r.upper)[:sublen]
    return InclusiveRange(int(lower), int(upper))


def expand_trunc_to_invalid(half: int, repeats: int) -> int:
    return int(str(half) * repeats)


def parse(data: str) -> List[InclusiveRange]:
    text_ranges = data.split(",")
    tuple_ranges = [tuple(r.split("-", 1)) for r in text_ranges]
    return [InclusiveRange(int(x), int(y)) for (x, y) in tuple_ranges]


def part_one(data: str) -> int:
    answer = 0

    ranges = parse(data)
    split_ranges = (split_range(r) for r in ranges)
    consolidated = chain.from_iterable(split_ranges)
    even_ranges = list(filter(lambda r: num_digits(r.lower) % 2 == 0, consolidated))

    for rng in even_ranges:
        half_rng = half_range(rng)
        # actually only need to check the edges;
        # the intermediate values are always within the range
        for half in range(half_rng.lower, half_rng.upper + 1):
            invalid = expand_half_to_invalid(half)
            if rng.contains(invalid):
                answer += invalid

    return answer


def part_two(data: str) -> int:
    invalid_numbers = set()

    ranges = parse(data)
    split_ranges = (split_range(r) for r in ranges)
    consolidated = list(chain.from_iterable(split_ranges))

    for rng in consolidated:
        rng_len = num_digits(rng.lower)
        substr_lens = filter(lambda x: rng_len % x == 0, range(1, rng_len // 2 + 1))
        for substr_len in substr_lens:
            times = rng_len // substr_len
            trunc_range = truncated_range(rng, substr_len)
            for trunc in range(trunc_range.lower, trunc_range.upper + 1):
                invalid = expand_trunc_to_invalid(trunc, times)
                if rng.contains(invalid):
                    invalid_numbers.add(invalid)

    return sum(invalid_numbers)


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = f.read()
    assert part_one(data) == 1227775554


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = f.read()
    assert part_two(data) == 4174379265


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = f.read()

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
