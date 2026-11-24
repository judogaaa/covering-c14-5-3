# Reproducibility and review guide

## Environment

- Python 3.10+ (standard library only; assertions enabled).
- GNU `g++` with C++17 support (`CXX` may select another compatible GNU compiler). The sources use GNU headers and built-ins; the reference platform is Linux/WSL.
- Run from the repository root. No Internet access or discovery solver is required.
- The verifier writes generated data and executables to `build/`, and some historical stage scripts regenerate JSON data in their own directories. Use a clean checkout for a fresh audit.

## Commands

```sh
python3 --version
g++ --version
python3 verify_upper.py
python3 -u verify.py
python3 -u audit.py
```

`audit.py` runs `verify.py` itself, then checks its generated data with the second residual solver. Running both commands in succession is optional and duplicates the main verification.

Partial checks:

```sh
python3 -u verify.py prior   # removal lemma, three-low, two-low, prior regular bounds
python3 -u verify.py low     # normalized links and one-low exclusion
python3 -u verify.py regular # normalized links and regular exclusion
python3 -u verify.py core    # low and regular stages, assumes prior results
python3 -u audit.py --local  # optional Python-only local-enumeration cross-check
```

`python3 audit.py --generated-only` checks data already present in `build/` and is **not** a substitute for a fresh run. The optional `--local` cross-check may take much longer; the original audit did not complete that optional experiment, and the proof does not rely on it.

## Expected checkpoints

| Stage | Expected result |
| --- | --- |
| Upper witness | 43 distinct blocks; all 364 triples; historical witness digest and relabeling |
| Degree-14 removal lemma | 13 layouts, 280 completions, every link removable |
| Three exact links | 96 completions; at least 15 additional blocks required |
| Two-low | All five relative types excluded |
| Degree-15 enumeration | 143 layouts; 63,704 completions; 752 representatives |
| One-low | 54,144 tests, 26,432 preliminary survivors, eight final certificates verified |
| Regular codegree-six matching | 2,335 residual unions excluded |
| Last regular branch | 219 representatives, 2,544,816 completions, 6,306 residual unions excluded |
| Additional residual checker | 2,335 + 6,306 cases excluded |

The complete archived verification is recorded in `logs/audit_full_verify.log`. A fresh run of the enhanced audit also completed successfully during repository preparation; see `logs/repository_audit.log`. A further clean publication audit completed successfully (`logs/publication_audit.log`). `logs/audit_generated.log` records additional checks on regenerated data. Other logs are retained as provenance, including interrupted exploratory runs, and should not be interpreted as proof of exclusion. The executable scripts regenerate the required enumerations and check exact certificates; stored output logs are not a replacement for running the verification.

## Continuous integration

The supplied GitHub Actions workflow runs the standalone witness check and the full `audit.py` on a fresh checkout. It uploads verification logs and records a failure if any command fails or exceeds the job timeout. A successful CI run is reproducibility evidence, not independent mathematical review. The workflow is included in the complete package. Check the public Actions tab for the actual run status of the imported revision.

## Suggested independent review order

1. Check the definitions and covering reductions in Sections 1–3 of `PROOF.md`.
2. Confirm exhaustive normalization, orbit handling, and local enumeration in Section 4.
3. Check the correspondence between one-low survivors and certificate rows in Section 5.
4. Check the high-codegree and triple restrictions in Sections 6–7.
5. Verify the exact residual identities, pruning rules, and exhaustive branching in Sections 8–9. Compare both implementations.
6. Reproduce all stages from a clean checkout and record compiler, Python version, commit ID, exit status, and logs.
7. Check the provenance and originality of the result separately from computational correctness.

A positive certificate or a concrete counterexample should be checked directly against the original covering definitions. Do not infer mathematical impossibility from a solver or CI timeout.
