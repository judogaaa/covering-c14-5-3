#!/usr/bin/env python3
"""Check the explicit upper-bound witness without other proof machinery."""
from itertools import combinations
from hashlib import sha256
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    points = set(range(1, 15))
    blocks = []
    for line in (root / "upper43_blocks.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        block = tuple(sorted(map(int, line.split())))
        if len(block) != 5 or len(set(block)) != 5 or not set(block) <= points:
            raise SystemExit(f"FAIL: invalid block {block}")
        blocks.append(block)
    if len(blocks) != 43 or len(set(blocks)) != 43:
        raise SystemExit("FAIL: expected exactly 43 distinct blocks")
    expected = set(combinations(sorted(points), 3))
    covered = {triple for block in blocks for triple in combinations(block, 3)}
    if expected != covered:
        raise SystemExit(f"FAIL: missing triples: {sorted(expected - covered)}")
    masks = list(map(int, (root / "two_low/upper43_masks.txt").read_text().split()))
    if len(masks) != 43 or len(set(masks)) != 43 or set(masks) != {
        sum(1 << (v - 1) for v in block) for block in blocks
    }:
        raise SystemExit("FAIL: labelled and bitmask witnesses disagree")
    historical = [tuple(map(int, line.split())) for line in
                  (root / "data/historical43_blocks.txt").read_text().splitlines() if line.strip()]
    permutation = (14, 10, 4, 9, 6, 11, 2, 3, 13, 8, 1, 12, 7, 5)
    if len(historical) != 43 or any(len(b) != 5 or len(set(b)) != 5 or not set(b) <= points for b in historical):
        raise SystemExit("FAIL: malformed historical witness")
    raw = bytes(v for b in historical for v in b)
    if sha256(raw).hexdigest() != "173772ab8d73847ff258f4f5ae2859d0fbe7e312483e1afc23d58c721bd22f93":
        raise SystemExit("FAIL: historical witness digest mismatch")
    if set(permutation) != points or {tuple(sorted(permutation[v-1] for v in b)) for b in historical} != set(blocks):
        raise SystemExit("FAIL: historical relabeling mismatch")
    print("PASS: historical witness digest and explicit relabeling verified.")
    print("PASS: 43 distinct five-element blocks cover all 364 triples.")
    print("This establishes only C(14,5,3) <= 43.")

if __name__ == "__main__":
    main()
