# A candidate computer-assisted proof of C(14,5,3)=43

**Research draft and reproducibility package — 24 November 2026**

**Preprint author:** Egor Demin (independent researcher).  
**Zenodo preprint, version v1:** [10.5281/zenodo.24514296](https://doi.org/10.5281/zenodo.24514296).  
**Research revision identified in the preprint:** [`5811830`](https://github.com/judogaaa/covering-c14-5-3/tree/58118307a11a08c5f2a53b37a160c5b36a2567c1).

See [CITATION.cff](CITATION.cff) and [CITATION.md](CITATION.md) for citation guidance, [LICENSE](LICENSE) for the research-verification terms, and [ATTRIBUTION.md](ATTRIBUTION.md) for the substantial contribution of generative AI tools and related work. The preprint is a candidate proof, not a peer-reviewed or priority-certified result.

This repository presents a candidate computer-assisted proof of the exact covering number

$$ C(14,5,3)=43. $$

Here $C(v,k,t)$ is the smallest number of distinct $k$-subsets of a $v$-element set such that every $t$-subset is contained in at least one chosen block. For these parameters, there are 364 triples and 2,002 candidate five-element blocks.

The package includes a 43-block construction (a relabeling of the historical Nurmela–Östergård witness; see [provenance](data/UPPER_WITNESS_PROVENANCE.md)), a reduction of the lower bound to finite cases, exhaustive enumeration algorithms, and integer certificates excluding the remaining 42-block cases. Verification uses only Python's standard library and C++17; it does not require a numerical optimization solver, a SAT solver, or Internet access.

**Status:** the archived full verifier completed successfully (159.59 seconds on the original audit environment). The enhanced full audit was also rerun successfully during repository preparation (exit status 0), including the second residual checker. A further fresh publication audit also completed with exit status 0. See [AUDIT.md](AUDIT.md), [the repository audit](logs/repository_audit.log), and [the publication audit](logs/publication_audit.log). These are computational checks, not independent human peer review or formal verification in a proof assistant. Scientific novelty and priority have not been established.

## Start here

| File | Purpose |
| --- | --- |
| [PROOF.md](PROOF.md) | Main mathematical argument; read this first |
| [AUDIT.md](AUDIT.md) | Audit methodology, results, and limitations |
| [verify.py](verify.py) | Complete proof verification driver |
| [audit.py](audit.py) | Full verification plus the second residual checker |
| [upper43_blocks.txt](upper43_blocks.txt) | Explicit 43-block witness, labels 1–14 |
| [REPRODUCIBILITY.md](REPRODUCIBILITY.md) | Detailed commands, expected results, and review checklist |
| [ATTRIBUTION.md](ATTRIBUTION.md) | Research provenance and source notes |
| [PUBLISHING.md](PUBLISHING.md) | Release checklist and Git commands |

## Reproduce the result

Requirements: Python 3.10 or newer, GNU C++ with C++17 support (`g++`), and a terminal. The commands below assume a Linux shell; Windows users can use WSL. On macOS install GNU GCC rather than relying on the default Apple Clang. No Python packages are required.

From the repository root:

```sh
python3 verify_upper.py   # fast, independent check of the upper bound only
python3 -u audit.py       # complete proof and additional audit
```

The full audit may take several minutes or longer, depending on hardware. A successful full run ends with:

```text
AUDIT PASS: full proof verification and additional checks completed.
```

The upper-bound check alone does **not** prove optimality. An interruption, nonzero exit, failed assertion or timeout is **not** a proof of impossibility. Do not disable assertions (`python -O`, `PYTHONOPTIMIZE`, or compiler flag `-DNDEBUG`). Set `CXX` to choose a compatible compiler if needed.

## Proof architecture

1. Verify the 43-block witness and the removable-block lemma for a link of degree 14.
2. Exclude three or more low-degree points; derive the lower bound 42.
3. Reduce degree-14 points to exact degree-13 links; exclude the two-low cases.
4. Enumerate normalized degree-15 links and exclude the one-low cases.
5. Exclude regular covers with high pair or triple multiplicities.
6. Exclude the remaining regular cases via exact residual constraint propagation and exhaustive branching.

All lower-bound exclusions must hold for the claimed equality to follow. See the complete arguments, hypotheses, and exact counts in [PROOF.md](PROOF.md).

## Repository layout

```text
core/                  Main C++ enumeration and residual solvers
                       Python helpers and the degree-14 removal check
data/                  Exact integer certificates for final exclusions
two_low/               Earlier lower-bound and two-low proof stages
regular_pair7/         Regular high-codegree proof stage
regular_triple5/       Rare-triple proof stage
logs/                  Recorded historical runs (not proof inputs)
.github/workflows/     Continuous verification configuration
verify.py              Full verification entry point
audit.py               Extended audit entry point
verify_upper.py        Standalone upper-bound check
```

The proof subdirectories retain intermediate documents for traceability. Their statements that the exact value was still unresolved describe earlier research stages, not the conclusion of the main draft. The generated `build/` directory is disposable and excluded from version control.

## Review and attribution

Independent scrutiny of the mathematical reductions, symmetry coverage, finite enumerators, and integer certificates is welcome. Please report any issue with a minimal counterexample or reproducible command. See [CONTRIBUTING.md](CONTRIBUTING.md).

Research provenance, including the use of generative tools, is documented in [ATTRIBUTION.md](ATTRIBUTION.md). The additional checker is a separate implementation, not an external peer review. The original copyrightable materials are subject to [LICENSE](LICENSE); the historical witness is attributed separately under its source data license. See [CITATION.md](CITATION.md) for citation guidance. No claim of priority is made.
