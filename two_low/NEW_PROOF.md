# Local degree certificates for two low-degree points in a (14,5,3) covering

> Historical proof-stage note. The current argument and supported reproduction commands are in [the main proof](../PROOF.md) and [the reproduction guide](../REPRODUCIBILITY.md). Earlier exploratory scripts mentioned in this note may not be included and are not required by the current verifier.

24 November 2026. Research draft; scientific priority and independent review pending.

## Scope
We strengthen the previously established restrictions on a hypothetical 42-block covering. We do not determine C(14,5,3) exactly. The earlier lower bound 42 and upper bound 43, and the restriction to at most two points of degree 13 or 14, are in PREVIOUS_PROOF.md and verify_new.py. The earlier argument uses the removable-block lemma of Rob Gardiner (2026), https://github.com/renidrag/covering/blob/main/coverings/14-5-3/proof.md. The new exclusions below depend on that lemma and the earlier three-low-point theorem.

## Theorem
Assume that a 42-block covering has exactly two points of degree at most 14. Delete their special blocks if needed to make their links exact, as in the previous proof. Let F be the union of the resulting exact parent links, containing 22 blocks, and let X be the other twelve points. Up to relabeling there are five relative link types. They have respectively 156, 153, 162, 153 and 180 uncovered triples in X, with orbit sizes 27, 24, 12, 8 and 1. Types 2 and 4 (zero-based indices) are impossible. Type 0 is possible only if both selected points have degree 13, four specifically determined points in X have degree 16, and the remaining eight have degree 15. This does not assert that any remaining type is realizable.

## Proof
The relative classification is the same exact enumeration of two links as in the earlier proof, now verified directly for the five representatives in reps.json. Their four common blocks partition X into four triples; each remaining line is a transversal. The verifier enumerates all 72 exact transversal families, proves transitivity for the first family under within-group permutations and group permutations, and verifies that the stabilizer of that first family partitions the second families into the five supplied orbits. All points y of X occur in exactly seven blocks of F, and F is a subfamily of the original covering. All have degree at least 15 by the earlier theorem.

Fix y in X and define Q=X minus {y}. Let H be the graph on Q whose edges {z,w} correspond to triples {y,z,w} not covered by F. If the full degree of y is 15, exactly eight blocks containing y remain outside F. Remove y from these blocks and discard any of the two roots. Pad each resulting set to a four-set of Q arbitrarily (possible because |Q|=11). The eight four-sets, possibly repeated, must cover every edge of H. Padding cannot remove an edge of H already covered. Thus a proof that no eight four-sets cover H also proves degree(y)>=16 in the original design, regardless of placement of the deleted special blocks.

For z in Q write h(z) for its degree in H and l(z)=ceil(h(z)/3). A four-set through z covers at most three incident edges. Eight four-sets have 32 point incidences, so sum l(z)>32 immediately gives impossibility. When sum l(z)=31, the incidence counts must be exactly c(z)=l(z)+[z=s] for some one surplus vertex s. There are eleven choices for s. If h(z)=3c(z), every four-set containing z must use only edges of H through z: otherwise its c(z) occurrences could not cover all h(z) distinct edges. Call such z tight.

For each of the 143 configurations requiring this test (13 pairs of relative type and y, each with 11 choices of s), local_certs.json contains nonnegative integer weights a(e) for edges e of H and b(z) for vertices z of Q. For every eligible four-set K (all edges in K touching tight vertices must belong to H), define

    score(K) = sum_{e subset K, e in H} a(e) - sum_{z in K} b(z).
    M = max(0, max_K score(K)).

The verifier checks for each certificate

    sum_{e in H} a(e) - sum_{z in Q} c(z)b(z) > 8M.

If eight eligible four-sets covered H with these incidence counts, their summed score would be at least the left side, because all a(e) are nonnegative and every edge is covered. It would also be at most 8M. This contradiction is exact and remains valid if the four-sets repeat. Numerical optimization was used to discover weights, but the verification uses only integer arithmetic and all candidate four-sets. The graph with 45 missing edges also gives direct contradiction by the incidence count.

The verified results are:

| Type (zero-based) | Missing triples in X | Orbit size | Points forced to degree >=16 |
|---|---:|---:|---:|
| 0 | 156 | 27 | 4 |
| 1 | 153 | 24 | 0 established |
| 2 | 162 | 12 | 10 |
| 3 | 153 | 8 | 0 established |
| 4 | 180 | 1 | 12 |

The total point degree in 42 blocks is 210=14*15. The deficit below degree 15 contributed by the two roots is at most four, and it exactly equals the total excess above 15 in X. Types 2 and 4 force at least ten and twelve units of excess respectively, a contradiction. Type 0 forces four units, possible only if both roots have degree 13 and those four forced points have degree 16, every other point in X having degree 15. In the representative labeling the four forced points are 4,8,10,12. This completes the stated exclusions.

## Reproduction and limitations
Run `python verify_new.py` and `python verify_local.py` (Python 3.10+, standard library, assertions enabled). The latter verifies 143 certificates and 20,124 candidate four-set inequalities. The numerical discovery script is cert_local.py (NumPy, SciPy). local_links.py and case0_lp.py are exploratory only; the case-0 linear relaxation was feasible and the MILP reached its 12-second limit without a witness or refutation. Neither is used as proof. The main problem remains unresolved: no 42-block construction or universal 42-block impossibility certificate was obtained. Scientific priority has not been established; no independent expert or Lean verification has been performed.

Related research: Alfonso Gippini Requeijo, *Links of minimum degree and exact covering numbers*, arXiv:2610.31696, 2026 (classification and certified SAT for other covering numbers). Gardiner's current source still states 41 <= C(14,5,3) <= 43; this is not evidence by itself of priority for the new results.
