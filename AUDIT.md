# Verification audit — 24 November 2026

## Result

The original complete proof archive was unpacked into a clean working directory and `python -u verify.py` was executed from beginning to end. It exited successfully, with the final message `THEOREM (see PROOF.md): C(14,5,3)=43. All verification stages completed.` Wall-clock time in this environment was 159.59 seconds. This is stronger evidence than the earlier split runs, and it does not use intermediate stored survivor logs as proof inputs.

## Strengthened checks

The verification source was then hardened without changing the mathematical exclusion decisions:

- `core/verify_degree14.py`: assert exactly 13 normalized layouts and 280 labelled completions.
- `two_low/verify_new.py`: assert the exact number and histogram of third-link completions.
- `two_low/verify_local.py`: assert the identities, not only the number, of the four forced high points of relative type 0.
- `core/signature_all.cpp`: explicitly enforce the signature-length bound used to justify injective 64-bit encoding.
- `verify.py`: check complete-root membership and block count of every surviving union; verify the ordered, complete sequence of representative indices, zero timeouts, exact completion totals and matching per-representative survivor counts, including all 2,544,816 completions of the last regular branch.

The strengthened earlier scripts were rerun; the signature output was reproduced exactly. The strengthened input checks passed on all 26,432 one-low surviving unions, and the strict per-representative checks passed on all four regenerated regular enumeration logs. The 43-block witness was also checked independently in both label and bitmask representations.

## Second residual checker

`core/independent_residual.cpp` uses the full residual multiplicities (rather than the changing multiplicities of yet-unselected blocks), bitsets of possible and selected blocks, and disjoint search branches. It checks both complete root links and initial bounds directly from the supplied block masks. For a subset S it maintains lower and upper bounds on the number of residual blocks through S. Counting the larger subsets through S gives the exact identities in Section 8 of PROOF.md. Interval tightening follows from these identities; candidate removal and mandatory selection use the current counts of selected and possible blocks. Slack pruning uses the sum of outstanding lower-bound incidences, and the available budget of larger subsets, after subtracting already selected blocks. All these are necessary conditions. A positive outstanding lower bound ensures that a completion contains at least one undecided candidate through the selected subset. The disjoint branches select the first such block in candidate order, excluding earlier candidates. Thus the recursion partitions every possible completion. All arithmetic is integral. No timeout is used as an exclusion.

The second checker independently rejected every one of the 2,335 matching-branch unions (16,621 search nodes) and every one of the 6,306 simple-branch unions (6,399 search nodes). It was run on the freshly regenerated cases; these also matched the earlier split-run case multisets exactly. See `logs/audit_generated.log`.

## Scope and limitations

The complete original driver has passed in a fresh extraction, and the new or strengthened checks have passed separately on its outputs or by direct rerun. The enhanced wrapper `audit.py` combines these checks for reproduction. During repository preparation it was executed in a fresh extraction of the audited archive and completed successfully (exit status 0), including the second residual checker. See `logs/repository_audit.log`. The explicit guard against Python optimized mode was added while that run was in progress and tested separately; no mathematical decision logic was changed. The optional `audit_local.py` Python-only cross-check of all 143 normalized degree-15 layouts was started but interrupted by choice after more than two minutes; no result from this optional experiment is used to establish the theorem. It can be run with `python audit.py --local` if desired. The main complete verification, including the exact C++ local enumeration, did finish, as did the earlier independently implemented Python checks of the high-weight and rare-triple branches.

No fatal mathematical error was identified in this audit. That is not a guarantee against all future findings. The proof remains computer-assisted, not formally verified in a proof assistant and not independently reviewed by a human mathematician. Scientific novelty and priority are not established by this audit. The new checker is a separate implementation from the same research process, not an external peer review.

## Publication provenance check (24 November 2026)

The explicit 43-block witness was compared with the historical Nurmela–Östergård witness. An incidence-graph isomorphism was found and the resulting point permutation was checked directly as a set equality of all 43 blocks. The standalone checker now additionally verifies the historical data digest and relabeling. This changes no lower-bound algorithm or certificate. See `data/UPPER_WITNESS_PROVENANCE.md`.

## Fresh publication audit

The complete audit was rerun from a clean extraction using Python 3.13.5 and GNU g++ 14.2.0. It completed with exit status 0, reproducing the 54,144 one-low tests, 2,335 matching-branch unions and 6,306 final regular unions, together with the second residual checker. See [logs/publication_audit.log](logs/publication_audit.log). After this run, documentation was standardized and executable Python modules containing assertions were given explicit optimized-mode guards where missing. These guards do not change normal-mode mathematical logic; they were checked separately. The historical witness checker was also tightened to reject repeated labels in a historical block. The complete GitHub Actions run must still be checked after import.
