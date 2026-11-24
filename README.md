# The covering number C(14,5,3)

**Research draft — 24 November 2026**

Let $C(v,k,t)$ denote the minimum number of distinct $k$-subsets of a $v$-element set that contain every $t$-subset in at least one block. This project investigates $C(14,5,3)$; its proposed exact value is 43.

## Verification status

The explicit 43-block construction establishes the upper bound. It is a relabeling of the historical construction of Nurmela and Östergård (1996), not a new construction. The proposed contribution is the exclusion of 42 blocks by exhaustive finite enumeration and exact integer certificates.

The complete lower-bound artifact is prepared locally but has **not yet been imported in full** into this repository. The earlier [proof draft](PROOF_DRAFT.md) is available for inspection; it is not a standalone reproducible proof of optimality. No independent peer review, formal verification, or scientific priority claim is made.

## Reproduce the upper bound

Run from the repository root, with Python 3.10+:

```sh
python3 verify_upper.py
```

The checker verifies all 364 triples, the 43 distinct blocks, the historical data digest and the explicit relabeling. A successful check establishes only $C(14,5,3)\leq 43$.

## Source and review

- [Historical witness provenance](data/UPPER_WITNESS_PROVENANCE.md)
- [Attribution and related work](ATTRIBUTION.md)
- [Review guidelines](CONTRIBUTING.md)

Once the full verification package is imported, the main proof will be in `PROOF.md` and the complete audit will run with `python3 -u audit.py` using GNU C++17 and Python's standard library. The current repository is an initial research release, not a refereed publication.
