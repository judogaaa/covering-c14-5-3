# Excluding relative two-link type 0 in a hypothetical 42-block (14,5,3) covering

> Historical proof-stage note. The current argument and supported reproduction commands are in [the main proof](../PROOF.md) and [the reproduction guide](../REPRODUCIBILITY.md). Earlier exploratory scripts mentioned in this note may not be included and are not required by the current verifier.

Research draft, 24 November 2026. Scientific priority and external peer review are not established. This result does not determine the exact covering number.

## Theorem
Conditional on the previously established three-low-point theorem and the two-link structural certificates (included as PREVIOUS_PROOF.md, NEW_PROOF.md, verify_new.py and verify_local.py), relative type 0 is impossible in any 42-block covering. Consequently, of the five relative types for two points of degree at most 14, only types 1 and 3 remain unexcluded. All indices are zero-based, and point labels run from 0 to 13.

## Reduction
The earlier results force both roots to have degree 13, and permit normalization to the 22 fixed blocks F in reps.json, entry 0, with roots 0 and 6. On X=V\{0,6}, the four points H={4,8,10,12} must have degree 16; the eight points Y=X\H must have degree 15. Every point of X is in seven fixed blocks. Any completion must have exactly 20 residual five-sets on X. At each point of Y, exactly eight residual blocks are incident.

## Exhaustive local enumeration
Fix y=1 in Y. Removing y from its seven fixed incident blocks gives seven known four-sets. Let Q=X\{y}, and let f(p) count occurrences of a pair p in these known four-sets; let d_F(z) count occurrences of z. The completed link is a covering of all pairs of V\{y} by 15 distinct four-sets. Its point degrees have the form 4+w(z), with w(z)>=0 and sum w=8. The two roots have w=0 since their exact links give pair codegree 4. For z in Q, each of the eight new four-sets through z covers at most three pairs through z, so

    w(z) >= max(0, d_F(z) + ceil(number of missing pairs through z in Q / 3) - 4).

The eleven lower bounds sum to 4. Thus the four remaining units can be distributed over the eleven coordinates in precisely binom(14,4)=1001 ways. direct_local.py enumerates all these assignments, without relying on any earlier degree-profile tables.

For each assignment, a point with w=0 has degree 4 in the completed link and therefore every pair through it occurs exactly once (12 pairs, four four-sets, three pairs per set). Enumerate all candidate four-sets on Q, excluding any that repeat an already covered pair incident to a zero-weight point. The universe E consists of missing pairs incident to a zero-weight point, all of which require exact coverage. The other missing pairs have two positive-weight endpoints and require coverage at least once. Track the residual degree target of each positive-weight point and the number of chosen blocks.

At each recursion step choose an uncovered pair in E and branch over all admissible candidate four-sets containing it, with all their E-pairs still uncovered. This is exhaustive because every completion contains exactly one block covering that pair. A chosen block with a nonempty E-mask cannot occur again, so no chosen-block-history restriction is missing. When E becomes empty, any remaining block must be entirely on positive-weight points and have empty E-mask. Enumerate all distinct such blocks of the required cardinality, checking degrees and remaining pair coverage. The tests that prune the recursion are necessary: too many blocks, insufficient pair capacity, excessive positive-point degree, or insufficient remaining blocks to achieve that degree. Each output is separately checked for all 78 pairs, exact point degrees and 15 distinct four-sets. Results: 141 weight assignments have at least one extension, and 1522 distinct local completions are enumerated.

## Compatibility across all eight points
compat_all.py explicitly enumerates permutations of the four common groups and of the three points in each group. It retains permutations preserving the two fixed root links individually. The script checks that the orbit of point 1 is exactly Y, and that the selected relabelings preserve H. Transporting the exhaustive list therefore gives all 1522 local completions at each point in Y. No symmetry of the unknown residual covering is assumed.

Represent a local completion by the set L_y of its eight residual FIVE-sets (the point y is reinserted). For distinct x,y in Y, any actual residual family must satisfy

    {B in L_x : y in B} = {B in L_y : x in B}.

Enforce this condition for every pair of points in Y. Iteratively delete a local choice if no choice at another point agrees with it on the entire common-block set. This deletes no globally compatible assignment. At convergence there are five local choices at each of the eight points. Exhaustively branch on every remaining choice at a point, repeating the same consistency procedure; the resulting search visits 50 states and has 36 complete, pairwise consistent assignments. There is no bound on total block count imposed during this compatibility enumeration.

For each complete assignment the union of the eight local families contains 22 distinct residual five-sets. Indeed, the enumeration yields 36 cases of size 22 and zero of size 20. Every five-set on X meets Y, since H contains only four points. Consequently the union is the entire residual family in any actual covering. It cannot have 20 blocks, contradicting the hypothesized 42-block budget (22 fixed + 20 residual). This excludes type 0. The 36 compatible assignments are not 42-block witnesses; they each require 44 total blocks, and their high-point degrees differ from the required 42-block profile.

Together with the earlier verified exclusions of types 2 and 4, this leaves only types 1 and 3 (24 and 8 normalized second links respectively). The zero-low-point and one-low-point branches remain unresolved.

## Reproduction
Run in this directory using Python 3.10+ with assertions enabled:

    python verify_new.py
    python verify_local.py
    python direct_local.py
    python compat_all.py

All four commands use only the standard library. The main audit logs in `../logs/` record the executable proof stages. all_local_direct.json is generated by direct_local.py. The proof still uses the earlier removable-block lemma described in PREVIOUS_PROOF.md, and has not been formalized in Lean or externally peer-reviewed. The exact global bound remains 42 <= C(14,5,3) <= 43.

## Additional geometric observations (not used in the exclusion)
The geometric classification of 5-sets in PG(2,3) can be reproduced by direct enumeration: 468 have one collinear triple, 702 have two, and 117 have four; hence the proposed necessary inequality m2+3*m4<=27 for a 29-block residual is correct. The proposed (2,1,1) excess-degree pattern for a 14-block point-link is only a candidate from a partial counting argument, not an actual realizable profile: the excess graph would have three edges each from u to v and from u to w, and none from v to w. In the link, uv and uw then each occur four times among the six blocks through u. At least two of those blocks contain both v and w, contradicting their pair multiplicity of one. The stronger removable-block theorem from prior work is still used. The full group of permutations of the four triples and within each triple has order 24*6^4=31104, not 1944. The sample MILP in an earlier exploratory proposal does not enumerate all relative types, nor does it address the degree-14 cases. No solver output is asserted from that sample.
