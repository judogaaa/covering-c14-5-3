#!/usr/bin/env python3
"""Independently verify the explicit upper-bound construction."""
from itertools import combinations
from pathlib import Path

def main():
    points = set(range(1, 15))
    path = Path(__file__).resolve().with_name("upper43_blocks.txt")
    blocks = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        block = tuple(sorted(map(int, line.split())))
        if len(block) != 5 or len(set(block)) != 5 or not set(block) <= points:
            raise SystemExit(f"FAIL: invalid block {block}")
        blocks.append(block)
    if len(blocks) != 43 or len(set(blocks)) != 43:
        raise SystemExit("FAIL: expected exactly 43 distinct blocks")
    expected = set(combinations(sorted(points), 3))
    covered = {t for b in blocks for t in combinations(b, 3)}
    if covered != expected:
        raise SystemExit(f"FAIL: missing triples: {sorted(expected - covered)}")
    print("PASS: 43 distinct five-element blocks cover all 364 triples.")
    print("This establishes only the upper bound C(14,5,3) <= 43.")

if __name__ == "__main__":
    main()
