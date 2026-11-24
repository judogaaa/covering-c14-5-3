# Local codegree-six classification and exclusion of triple multiplicity five

> Historical proof-stage note. The current argument and supported reproduction commands are in [the main proof](../PROOF.md) and [the reproduction guide](../REPRODUCIBILITY.md). Earlier exploratory scripts mentioned in this note may not be included and are not required by the current verifier.

Research draft, 24 November 2026. Scope: regular (14,5,3) coverings with 42 distinct blocks. Uses the previous computer-checkable result that all pair codegrees in this branch are at most six. Not a determination of C(14,5,3). Priority and external expert review remain unestablished.

## 1. Excess identities and spectral relaxation

Let e(T)=lambda(T)-1 and w(P)=lambda(P)-4. The necessary identities are sum e=56, sum_{T contains x} e(T)=12 and sum_{T contains P} e(T)=3w(P). The vertex-triangle incidence matrix M of the multiset of excess triangles has MM^T=12I+3W, so min eigenvalue(W)>=-4 and MM^T=0 modulo 3. These follow directly by counting and are correct. The modular identity follows from the same exact equality, rather than providing a separate contradiction.

These conditions, including every cut bound, are jointly feasible without claiming an actual covering: take vertices modulo 14, let w=1 precisely at cyclic distances 1,2,3,4 and let e consist of all translates of {0,1,3} once, {0,1,4} twice, and {0,2,4} once. The cyclic difference counts give each positive edge multiplicity three. These identities and the cut bound can be checked by exhaustive enumeration of all 16384 subsets. The example is only a witness for the relaxation.

## 2. Complete local classification for a marked codegree-six pair

At a point x of degree 15, its 15 four-set link covers all 78 pairs of 13 other points. Every link degree is at least four; its excess degrees sum to eight. By the previous regular pair-seven theorem all these excess degrees are at most two. If a pair xy has codegree six, at least one degree excess is two. The only partitions of eight into ones and twos with a two are (2,2,2,2), (1,1,2,2,2), (1,1,1,1,2,2), (1,1,1,1,1,1,2). At least one other point has degree four, so its four blocks partition the remaining twelve into four triples. Relabel it as 0; permuting within and between triples permits sorting all four triple weight multisets. The routine layouts enumerates every such normalized layout. The linked recursion branches on an uncovered pair involving a zero-excess point and includes every compatible four-set; such pairs must occur exactly once. It maintains positive point degrees and pair coverage, and exhaustively chooses any remaining all-positive four-sets. Distinctness of blocks is enforced. Thus the enumeration is complete modulo the stated normalization.

The verifier counts 41 layouts, 19,168 labelled links (summed over layouts; not a count of nonisomorphic links), and 26,076 marked codegree-six events. For each, the positive entries of b_z=e(x,y,z) are:

- 2 pairs of codegree 5, 3 pairs of codegree 6 through x: (1,1,2,2).
- 4 pairs of codegree 5, 2 pairs of codegree 6: (1,1,1,1,2), (1,1,2,2), (2,2,2), (1,1,1,3), (1,2,3), (1,1,4).
- 6 pairs of codegree 5, 1 pair of codegree 6: (1,1,1,1,1,1), (1,1,1,1,2), (1,1,2,2), (1,1,1,3).
- Four pairs of codegree six: no link exists.

In particular a codegree-six pair has at least three repeated triples; six repeated triples require the last feasible profile at both endpoints.

## 3. New theorem: every triple has multiplicity at most four in a regular 42-cover

If a triple has e>=4, each of its three pairs must have w>=2 by sum e(T) over that pair = 3w. Therefore every one of its pairs has codegree six. The local table shows e<=4 and e=4 can only occur at a root with exactly two codegree-six partners and four codegree-five partners. In particular the alleged triple has multiplicity exactly five, and each of its three points has that profile.

Normalize the first link (root 13) as above. Enumerate all links of the required profile and mark each pair whose multiplicity within the link is five. The explicit weight-preserving group of triple and within-triple permutations acts on this set. The routine initial verifies that each orbit lies in the pending set and removes it, leaving precisely two representatives (including the marked pair).

For each representative choose one of the marked points y as the second root (the sorted first point suffices since both have the required profile). Exactly six blocks of its link are fixed by the first root, so nine further four-sets are needed, avoiding the first root. The other marked point must have link degree six; exactly four further points must have link degree five. The routine extend enumerates every assignment of these four points, requiring positive excess at any endpoint of a repeated fixed pair, and excludes only assignments incompatible with fixed degrees. It branches over all ways to cover each remaining pair involving a degree-four link point exactly once, checks the prescribed positive degrees, covers remaining positive-positive pairs, and enumerates any remaining all-positive blocks. The fixed link covers all pairs involving the first root, so none of these pairs require completion. Every full second link is independently checked for all 78 pairs, degree multiset, and distinctness. There are exactly eight completions for each representative, producing 16 distinct-case two-link unions of 24 parent blocks (not necessarily globally inequivalent).

For every one of the 16 unions, the verifier finds at least two pairs P already contained in six fixed blocks but with four triples through P still uncovered. Since a further block through P covers at most three such triples, at least two further blocks through P are required. Thus the final codegree would be at least eight, contradicting the established upper bound six. No numeric solver is used. Therefore every triple has multiplicity at most four in a regular 42-cover. QED.

## Reproduction

Run `python verify_new.py` and `python rare_triple.py` with Python 3.10+ and assertions enabled. Both use only the standard library; the included classification modules are retained from the earlier research. The logs record actual successful runs. The prior regular pair-seven theorem is a separate dependency (its package is covering_pair7_certified.zip, verify.py). This proof does not exclude regular covers with triple codegrees at most four or the nonregular branch. It does not assert scientific novelty without independent priority review.
