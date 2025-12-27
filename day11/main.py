from pathlib import Path


def parse_input(data: str) -> dict[str, list[str]]:
    machines = {}
    for line in data.splitlines():
        m_in, m_out_str = line.split(":", 1)
        m_out_list = m_out_str.split()
        machines[m_in] = m_out_list
    return machines


def count_paths(start_name: str, end_name: str, graph: dict[str, list[str]]) -> int:
    memo: dict[str, int] = {}

    def _dfs(current: str) -> int:
        if current == end_name:
            return 1
        if current in memo:
            return memo[current]

        total_paths = 0
        if current in graph:
            for neighbor in graph[current]:
                total_paths += _dfs(neighbor)

        memo[current] = total_paths
        return total_paths

    return _dfs(start_name)


def part_one(graph: dict[str, list[str]]) -> int:
    return count_paths("you", "out", graph)


def part_two(graph: dict[str, list[str]]) -> int:
    # Path 1: svr -> fft -> dac -> out
    path1 = (count_paths("svr", "fft", graph) *
             count_paths("fft", "dac", graph) *
             count_paths("dac", "out", graph))

    # Path 2: svr -> dac -> fft -> out
    path2 = (count_paths("svr", "dac", graph) *
             count_paths("dac", "fft", graph) *
             count_paths("fft", "out", graph))

    return path1 + path2


def test_parse_input() -> None:
    with Path("example.txt").open() as f:
        data = parse_input(f.read())
    assert data["you"] == ["bbb", "ccc"]


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = parse_input(f.read())
    assert part_one(data) == 5


def test_part_two() -> None:
    with Path("example2.txt").open() as f:
        data = parse_input(f.read())
    assert part_two(data) == 2


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = parse_input(f.read())

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
