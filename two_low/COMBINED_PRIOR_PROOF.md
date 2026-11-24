# New structural exclusions for (14,5,3) coverings with 42 blocks

> Historical proof-stage note. The current argument and supported reproduction commands are in [the main proof](../PROOF.md) and [the reproduction guide](../REPRODUCIBILITY.md). Earlier exploratory scripts mentioned in this note may not be included and are not required by the current verifier.

Research draft, 24 November 2026. Not independently peer-reviewed or Lean-formalized; no claim of scientific priority or of the exact unrestricted covering number. The earlier lower-bound proof uses the removable-block lemma of Gardiner (itself citing Sane); see PREVIOUS_PROOF.md. The finite enumerations described here actually ran. All exclusion calculations use exact integers, not floating-point MILP or spectral numerical thresholds.

## 1. Preliminary reduction

Let C be a covering by 42 distinct five-sets on 14 points. Every point has degree at least 13, every pair codegree at least 4, and the point-degree sum is 210. The previous theorem (verify_new.py) excludes three or more points of degree at most 14 and excludes 41 or fewer blocks. The 43-block upper witness is checked by the same program.

For any selected points of degree 13 or 14, use the removable-block lemma for degree 14. Delete the corresponding distinct special blocks, once each. A degree-13 point belongs to none of these blocks. If two degree-14 points belong to the same special block, their special blocks coincide, as proved in PREVIOUS_PROOF.md. Consequently each selected point now has its exact 13-block link. Every triple touching a selected point is covered by those links. Replace each deleted block by a five-set of unselected points containing its intersection with the unselected points (there are at least 12 unselected points when selecting one or two). This preserves coverage of every triple outside the selected points, and no unselected point's degree decreases. If any replacement repeats an existing block, removing repetitions would give at most 41 blocks, already excluded. Therefore it is sufficient to exclude 42-block coverings with exactly two degree-13 roots, or with exactly one degree-13 root. This reduction is an existence reduction; restrictions on other point degrees in the reduced design need not be identical to restrictions in the unreduced design.

## 2. All two-low-point cases are impossible

Assume two degree-13 roots. Their exact parent links have union F of size 22; the remaining twenty blocks avoid both roots. The classification and certificates in NEW_PROOF.md and TYPE0_PROOF.md exclude relative types 0, 2, 4. The five relative types exhaust all 72 second transversal families; orbit sizes 27,24,12,8,1. We now exclude types 1 and 3.

Write X for the twelve nonroot points. Every x in X has seven fixed incident blocks, and by the three-low-point theorem d(x)>=15. Since the two roots each have degree 13, sum_{x in X}(d(x)-15)=4. At least eight points of X have degree exactly 15.

### Complete local domains

At a potential degree-15 point y, eight further parent blocks must contain y and avoid both roots. Removing y gives eight four-subsets of Q=X\\{y}. In its completed 15-block link, each nonroot point z has degree 4+w(z), w(z)>=0, and sum w=8 (the two roots each have link degree four). Write f(p) for fixed pair multiplicities in the seven known link blocks and d_F(z) for fixed link point degrees. Every possible weight vector satisfies

    w(z) >= max(0,d_F(z)+ceil(number of missing Q-pairs through z / 3)-4).

local.py enumerates every vector by distributing the remaining excess units, without assuming any precomputed degree profiles. For each vector, all pairs involving a zero-excess point must occur exactly once in the completed link. Reject candidates repeating a fixed pair at such a point. Partition the missing pairs into E (touching a zero-excess point) and P (both ends positive). Cover E exactly by branching on a missing pair and considering every admissible block containing it; track positive point degrees and covered P pairs. Once E is empty, enumerate every distinct choice of remaining four-sets with empty E-mask and check exact positive degrees and full coverage of P. This is exhaustive; the zero-point degrees follow from exact coverage of their incident pairs. Each resulting 15-block link is verified independently for distinctness, all 78 pairs, and degrees. Counts in the following table are of distinct labelled local completions at representatives, not isomorphism-class counts.

| Relative type | Automorphism group order (roots fixed) | Orbit of nonroot points | Local domain size |
|---|---:|---|---:|
| 1 | 18 | 9 points, representative 1 | 1522 |
| 1 | 18 | 3 points, representative 8 | 140 |
| 3 | 54 | 9 points, representative 2 | 140 |
| 3 | 54 | 3 points | not required |

verify_all_subsets.py explicitly enumerates the permutations of the four common groups and their internal labels, keeps only those preserving each exact root link, computes the orbits, and transports the complete local domain to every point of the indicated orbit. In type 3, at least five of the nine points in the large orbit have degree 15 because at most four points of X can have larger degree. No domain is needed at the other three points.

### Necessary pairwise agreement

For any two degree-15 points x,y, their respective local residual FIVE-set families L_x,L_y must satisfy

    {B in L_x : y in B} = {B in L_y : x in B}.

This equality is essential: agreement just on the number of common blocks would not suffice. For each candidate subset S of points required to have degree 15, remove a choice at x if no choice at y in S agrees on the complete common-block signature. Repeat for every pair until stable or a domain becomes empty. No restriction is placed on points outside S, and this elimination cannot remove any genuinely compatible assignment. No assumption is made that the unknown covering has any symmetry.

Test every 8-subset of X for type 1 (495 subsets, without a subset orbit quotient), and every 5-subset of the large orbit for type 3 (126 subsets). All 621 tests fail at arc consistency itself, before any further branching or block-budget condition. Thus no compatible assignment exists in either type. Since the previous certificates exclude all other relative types, there cannot be two points of degree <=14 in a 42-block covering, by the reduction in Section 1. This is the main new theorem.

## 3. One exact low point: finite two-link reduction and exclusion of codegree seven at degree-15 points

If exactly one point has degree 13, the sum of degree excesses over 15 on the other thirteen points is two. Their degrees are therefore 15^12,17 or 15^11,16^2. Pick any degree-15 point y, and let x be the degree-13 point. Their pair codegree is exactly four. The four common parent blocks partition the other 12 points Q into four triples. The nine further x-blocks (after removing x) are transversals of these four groups, covering each cross-group pair exactly once. one_low_input.py enumerates all 72 such transversal designs by exact cover, as well as every sorted normalized layout of the twelve link excess weights for y (sum 8, all 143 layouts). All allocations reduce to these by group permutations and within-group permutations. In this labeling x=12,y=13 and Q={0,...,11}.

The completed link of y requires 11 four-sets on Q, after the four fixed blocks through x. The same zero-weight exact pair cover and positive-weight residual method as Section 2 enumerates all solutions for each normalized layout. In one_low.cpp, all positive and zero point degrees are tracked explicitly. The group preserving the normalized weights and group partition acts on these solutions. The code removes each full orbit and retains one representative, then pairs each such representative with **all** 72 x-transversal designs. This covers every possible relative alignment, because the same relabeling used to normalize y also maps the x-design to one of the 72 designs. The full run yielded 63,704 labelled local links (summed over the 143 normalized layouts), 752 representatives, and 54,144 two-link cases (not necessarily distinct isomorphism types). It also recovers exactly the six previously feasible degree-15 excess profiles, none with weight above three. The proof does not assume a global cap of six for nonregular coverings.

Each two-link union F has 24 blocks, leaving 18 blocks on Q, hence 90 residual point incidences. For a pair p in Q write q(p) for its fixed codegree and h(p) for the number of still-uncovered triples through p. For a point z write h(z) for its number of still-uncovered triples, and d_F(z) for its fixed degree. The necessary lower bounds are

    r(p) >= max(4-q(p),ceil(h(p)/3));
    r(z) >= max(15-d_F(z),ceil(h(z)/6),ceil(sum_{p contains z} r_lower(p)/4)).

These follow by counting the at most three new triples per pair, at most six per point, and four pair incidences per residual block through a point. The sum of the point lower bounds must not exceed 90. The program excludes 27,712 cases; 26,432 survive this test. This does not close the one-low branch.

For the branch where y has a codegree-seven partner (one excess weight 3), one_low_pair7.cpp uses exactly the same complete enumeration but retains layouts of maximum weight three. It obtains 208 labelled local links, 10 representatives, and 720 two-link cases. The incidence bound excludes 489. extract_cases.py reconstructs the remaining 231 unions of 24 actual five-sets, and check_cases.py independently verifies all of these have the required root links and pass the incidence test.

For each of the 231 unions and each z in Q, local_feasible.cpp checks whether the local link at z can have degree 15. Exactly k=15-d_F(z) additional blocks through z are required. They avoid both x and y. In the link at z the degree of x is 4 and that of y is already fixed, say 4+w_y, because no more blocks through either root can occur. The excess-degree budget for the other eleven points is 8-w_y. For each of them enumerate every excess vector satisfying the same lower bounds as Section 2 with the actual number k of remaining blocks. Recurse over all exact missing zero-weight pairs and check all positive-weight pairs, with the exact target degrees for all eleven points. The search stops at a local witness if one exists; if the entire search fails, z must have degree at least 16. Every pruning test is a necessary bound on remaining degrees, number of blocks or number of missing pairs. Fixed triples touching either completed root are already covered, so no additional root-containing blocks are needed or allowed.

The run tested all 231 cases, and in each found three points with no degree-15 link, contradicting the total excess budget two. It visited 1,706,915 search states, with no timeout. Therefore in the one-exact-low-point case, no pair incident to a degree-15 point can have codegree seven (or above, by the full local profile enumeration). This does not exclude a high-high pair of codegree seven, nor does it assert the same bound for all unreduced degree-14 designs. A separate exploratory run on profile (1,1,2,2,2) excluded 83 of 95 surviving cases; 12 remained. A longer run on another profile was interrupted and is not used in any theorem.

## 4. Regular case: limitations of excess-graph relaxations

The claim that the number of triples with excess 2 is at most 2 is not proved. The number of triangles of the positive graph is not the number of positive-excess triples. An explicit relaxation example is as follows: on Z/14Z let all cyclic distances 1,2,3,4 be edges. Take all translates of (0,1,3) with multiplicity 1, (0,1,4) with multiplicity 2, and (0,2,4) with multiplicity 1. All pair excess sums are 3 on edges and 0 off edges, vertex sums are 12, and total excess is 56. This implies the Gram PSD condition exactly. There are 84 graph triangles, 42 positive-excess triangles, and 14 with excess 2. This is NOT an actual five-block covering and only refutes the deduction from the listed relaxation constraints.

Let m2 count triangles with excess 2 and let n_i count unordered pairs of distinct copies in the 56-triangle excess multiset intersecting in exactly i points. Then n3=m2, n2=168-3*m2, n1=588+3*m2, n0=784-m2. In particular the proposed constant intersection counts erroneously omit identical-triangle copies. The submitted SAT encoding also reuses auxiliary variable numbers from separate cardinality encodings; a shared variable pool or increasing top_id is necessary. The graph generator uses WL hashes as complete isomorphism certificates, which is unsound (indeed regular graphs of a fixed order and degree receive the same uniform-color WL refinement). The MILP code appends a constraint row without matching bounds and does not encode the claimed m2 count. Its failure or no-solution output cannot establish an exclusion.

## 5. Exact exclusion of a symmetry class

Suppose the 42-block covering admits an automorphism with cycle structure 7+7 on points. Since at most one point may be below degree 15 and any degree is constant on each cycle, all degrees are 15. Each block and triple orbit has length seven (a set invariant under the whole action would have size divisible by seven). orbit7.py enumerates all 286 block orbits and 52 triple orbits. Select six distinct block orbits; their triple orbit masks must cover all 52, and their representative intersections with the first point cycle must sum to 15. orbit7.cpp branches on an uncovered triple orbit and partitions choices by the first chosen candidate covering it; no earlier candidate in that branch may be chosen later. Every completion must choose some candidate covering the pivot, so this partitions the complete search. The bounds on marginal coverage and cycle degree are necessary. The exact search exhausted 234,037 states without a solution. This excludes only the indicated cycle structure, not all order-seven actions or all possible coverings.

## 6. Status and reproduction

The exact unrestricted value remains unknown in this work: 42 <= C(14,5,3) <= 43. At most one point of degree 13 or 14 can occur in a 42-cover. After the existence reduction, only the degree profiles 15^14, (13,15^12,17), (13,15^11,16^2) need be checked. Regular covers, and exact-one-low covers with the remaining codegrees, are not excluded. No 42-block witness was found. All new theorems still depend on the earlier removable-block lemma and finite enumeration; external mathematical review is required. See `../REPRODUCIBILITY.md` for the current commands and scope of logs.
