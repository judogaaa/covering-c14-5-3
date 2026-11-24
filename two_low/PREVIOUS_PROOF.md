# Three almost-exact links force at least 43 blocks in a (14,5,3) covering

> Historical proof-stage note. The current argument and supported reproduction commands are in [the main proof](../PROOF.md) and [the reproduction guide](../REPRODUCIBILITY.md). Earlier exploratory scripts mentioned in this note may not be included and are not required by the current verifier.

Research draft — 24 November 2026. Independent expert review and priority verification pending.

## Main results

**Theorem.** Let F be a family of distinct five-subsets of a fourteen-element set V covering every three-subset. If at least three points occur in at most fourteen blocks each, then |F| >= 43.

**Corollary.** 42 <= C(14,5,3) <= 43. If a 42-block covering exists, it has at most two points of degree less than 15. This is a necessary restriction, not a claim to know the exact covering number.

The proof below replaces the earlier rational LP certificates with two integer rounding inequalities and a small exact enumeration. The accompanying standard-library Python program checks the finite part without a numerical optimizer. It enumerates 72 possible second links and all 96 third-link completions; it does not assume global symmetry of the covering.

## 1. Exact links after deletion

Write d(x) for the number of blocks through x. The four-subsets obtained by deleting x from those blocks cover all 78 pairs of V\\{x}. Each four-subset contains six pairs, so d(x) >= 13. At degree 13 the link covers every pair exactly once. At degree 14, use the removable-block lemma (Gardiner, 2026, Lemmas 7–8, citing Sane's projective failed-design result): any fourteen four-subsets covering the pairs of thirteen points contain an occurrence whose deletion gives exact pair coverage. The source supplies a proof and reports a Lean formalization of the lemma. This draft relies on that published lemma.

For a degree-14 point x, let K_x be the parent block removed. Precisely the six triples of K_x through x are doubled; all other triples through x are covered once. A degree-13 point cannot belong to K_x, because its triples are all unique. If y is another degree-14 point in K_x, all three triples {x,y,t} for t in K_x\\{x,y} are doubled. Thus all five points of K_x are in K_y, and K_x = K_y. (These are the special-block properties in Gardiner's Lemma 9.)

Choose three distinct points of degree 13 or 14. Delete the distinct special blocks belonging to the chosen points of degree 14, once each. No chosen degree-13 point loses a block. Every chosen degree-14 point loses exactly its special block, by the preceding compatibility observation. The remaining family has exact links at the three chosen points. It need not cover triples outside those points. We only use its blocks through the chosen points, which also belong to the original family.

## 2. Exhaustive link enumeration

Call two of the chosen points 0 and 1; call the third y. The four blocks through 0 and 1 partition the remaining twelve points into four triples G_1,...,G_4. Renumber these groups as (2,3,4), (5,6,7), (8,9,10), (11,12,13).

In the exact link of 0, each of the other nine four-point lines meets each group once: a second pair from one group would violate exactness because its pair was already covered by a line through 1. These nine transversals cover each of the 54 pairs joining different groups exactly once. Conversely all such transversal families are included by the exact-cover enumeration of the 54 pairs among the 81 possible transversals. The same applies to the link of 1.

The verifier enumerates 72 transversal families and verifies that the independent permutations of the three labels inside each group map the lexicographically first family onto all 72. Therefore fixing the first family loses no case. It retains all 72 second families without taking an orbit quotient. The union of the two parent links has 22 distinct blocks and is exact at 0 and 1.

For each y outside {0,1}, seven of those blocks contain y: four from each link and one shared. If these seven blocks repeat a pair in the link of y, no exact third link is possible. Otherwise 36 pairs of its link remain uncovered. The six further blocks containing y must avoid both 0 and 1, since those links are already complete. Enumerate all exact covers of the 36 pairs by four-subsets of V\\{0,1,y}. This lists every possible third link. In total there are 96 completions, each yielding a 28-block subfamily F0 of the original covering.

The exact-cover routine branches on an uncovered pair, considers every eligible block containing it and removes the pairs in that block. Because all pairs must occur once, every completion belongs to one of these branches. Each recursion strictly decreases the number of remaining pairs, so it terminates. The script checks the resulting links exactly by integer counters.

## 3. Two rounds of integer counting

Let U be the set of triples not covered by F0. For each pair P let h(P) count the members of U that contain P, and let r(P) count the original blocks outside F0 that contain P. Such a block covers at most three members of U through P. Consequently

    r(P) >= ceil(h(P)/3).

For each point x let r(x) count original blocks outside F0 containing x. Every such block contains exactly four pairs through x, so

    4*r(x) = sum_{P containing x} r(P),
    r(x) >= ceil((sum_{P containing x} ceil(h(P)/3))/4).

Let L be the sum over the fourteen points of the last lower bounds. If n original blocks remain outside F0, their total point incidence is 5*n, and thus 5*n >= L. This is valid even when remaining blocks contain any of the three chosen points. It does not use a degree cap, distinctness of residual blocks or the assumption that the deleted blocks are outside all selected points.

The complete enumeration gives:

| Uncovered triples | L | Number of completions |
| ---: | ---: | ---: |
| 108 | 72 | 72 |
| 117 | 74 | 24 |

For 42 or fewer total blocks, there are at most 14 blocks outside the 28 fixed ones, hence at most 70 residual point incidences. In every case L >= 72, a contradiction. Equivalently all cases need at least 15 additional blocks. This proves the theorem.

## 4. Corollaries and limitations

For a hypothetical covering with at most 41 blocks, total point incidence is at most 205. If at most two points have degree less than 15, using the universal floor 13 gives total incidence at least 12*15 + 2*13 = 206. So at least three low-degree points are necessary, contradicting the theorem. This establishes C(14,5,3) >= 42 without the previous rational certificates. A separate check of upper43_masks.txt confirms a 43-block witness (all 364 triples); the historical upper bound is credited to Nurmela and Östergård (1996) in Gardiner's source.

For 42 blocks the total degree is 210. The theorem excludes all degree profiles with three or more points of degree 13 or 14, but does not exclude an entirely 15-regular covering, or profiles with one or two low-degree points. A further independently checked two-link observation: among the 72 second links, the one identical to the first leaves 180 uncovered triples and forces 108 residual point incidences, exceeding the 100 available with 20 residual blocks. This rules out that particular two-link alignment in a 42-block cover. It is not a general exclusion of 42.

The exploratory MILP and local search logs are not used in the proof. They have no exact global infeasibility certificate. No 42-block witness was found. The final mathematical status of this draft remains 42 <= C(14,5,3) <= 43; the exact value is not established. Scientific novelty and attribution require independent review. This draft is not independently refereed or Lean-formalized.

## Reproduction

Run `python verify_new.py` using Python 3.10+ without `-O`. The verifier checks integer counts and exact finite enumeration, and verifies the upper witness. No third-party packages required. See `../logs/prior_verification.log` and the current complete audit logs for run output. The supplied proof must be reviewed together with the source lemma and the verifier.

## Reference

Rob Gardiner, *A structural proof of 41 <= C(14,5,3) <= 43*, 22 October 2026. https://github.com/renidrag/covering/blob/main/coverings/14-5-3/proof.md (especially Lemmas 7–9). The source credits Sane's earlier projective failed-design result and Nurmela–Östergård's 1996 upper construction. Checked 24 November 2026. This citation is not a claim of independent peer review of the source.
