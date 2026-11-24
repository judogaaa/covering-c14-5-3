"""Integer-only verifier for the 42-block lower bound and a low-degree exclusion.
The mathematical reduction is in PROOF.md. Run with Python 3.10+ without -O.
"""

if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
V=set(range(14)); P=set(combinations(sorted(V),2)); U=set(combinations(sorted(V),3))
# Labels 0,1 are two chosen points with exact links after deletion.
X=V-{0,1}; groups=[tuple(range(2+3*i,5+3*i)) for i in range(4)]
shared=[tuple((0,1)+g) for g in groups]

def exact_covers(universe, candidates):
    """Sets, not numerical optimization: pick an uncovered pair and branch."""
    c={b:frozenset(combinations(b,2)) for b in candidates}
    c={b:p for b,p in c.items() if p<=universe}
    index={p:[b for b,q in c.items() if p in q] for p in universe}
    def rec(remaining):
        if not remaining:
            yield (); return
        options=min(([b for b in index[p] if c[b]<=remaining] for p in remaining),key=len)
        for b in options:
            for rest in rec(remaining-c[b]): yield tuple(sorted((b,)+rest))
    return set(rec(frozenset(universe)))

cross={tuple(sorted((x,z))) for g,h in combinations(groups,2) for x in g for z in h}
trans=list(product(*groups)); links=exact_covers(cross,trans)
assert len(links)==72
first=min(links)
# Explicitly check transitivity; all 72 possibilities for the second link are retained.
images=set()
for ps in product(*[list(permutations(g)) for g in groups]):
    f={a:b for g,h in zip(groups,ps) for a,b in zip(g,h)}
    images.add(tuple(sorted(tuple(sorted(f[x] for x in b)) for b in first)))
assert images==links

def check_link(F,x):
    assert Counter(t for b in F if x in b for t in combinations(sorted(set(b)-{x}),2))==Counter(combinations(sorted(V-{x}),2))

def bounds(F):
    missing=U-{t for b in F for t in combinations(b,3)}
    mp=Counter(p for t in missing for p in combinations(t,2))
    # Every residual block through p covers at most three missing triples through p.
    need={p:(mp[p]+2)//3 for p in P}
    # Every residual block through x contains exactly four pairs through x.
    deg={x:(sum(n for p,n in need.items() if x in p)+3)//4 for x in V}
    return len(missing),sum(deg.values())

hist=Counter(); pairhist=Counter(); count=0
for second in sorted(links):
    fixed=shared+[(0,)+b for b in first]+[(1,)+b for b in second]
    assert len(set(fixed))==22
    check_link(fixed,0); check_link(fixed,1)
    pairhist[bounds(fixed)]+=1
    if second==first: assert bounds(fixed)==(180,108)
    for y in sorted(X):
        known=Counter(t for b in fixed if y in b for t in combinations(sorted(set(b)-{y}),2))
        if any(n>1 for n in known.values()): continue
        residual=set(combinations(sorted(V-{y}),2))-set(known)
        assert len(residual)==36
        for third in exact_covers(residual,combinations(sorted(X-{y}),4)):
            F=fixed+[tuple(sorted((y,)+b)) for b in third]
            assert len(F)==len(set(F))==28
            for x in (0,1,y): check_link(F,x)
            h,d=bounds(F)
            hist[h,d]+=1; count+=1
            assert d>5*(42-28), (F,h,d)
assert count==96 and hist==Counter({(108,72):72,(117,74):24}), (count,hist)
print('Second links:',len(links))
print('Two-link cases (missing triples, residual point-incidence lower bound):',sorted(pairhist.items()))
print('Three-link completions:',count)
print('Three-link cases (missing triples, residual point-incidence lower bound):',sorted(hist.items()))
print('PASS: every three-link case needs at least 15 additional blocks, hence at least 43 total.')
print('PASS: a 42-block cover can have at most two points of degree at most 14.')
print('PASS: 41 or fewer blocks are impossible by the degree sum.')

masks=list(map(int,Path(__file__).with_name('upper43_masks.txt').read_text().split()))
assert len(masks)==len(set(masks))==43 and all(0<m<1<<14 and m.bit_count()==5 for m in masks)
B=[tuple(i for i in range(14) if m>>i&1) for m in masks]
assert {t for b in B for t in combinations(b,3)}==U
print('PASS: 43 distinct blocks cover all 364 triples.')
