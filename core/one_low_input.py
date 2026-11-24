
if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

# normalized weight layouts for 12 points partitioned in four triples.
from itertools import combinations,product,permutations
from pathlib import Path
from collections import Counter
def partitions(n,lo=1):
 if not n:yield ();return
 for k in range(lo,n+1):
  for p in partitions(n-k,k):yield (k,*p)
def layouts(p):
 def rec(rem,last,gs):
  if not rem:yield gs;return
  for g in sorted(set(combinations(rem,3))):
   if g<last:continue
   r=list(rem)
   for v in g:r.remove(v)
   yield from rec(tuple(r),g,gs+(g,))
 return rec(tuple(sorted((0,)*(12-len(p))+p)),(),())
G=[tuple(range(3*i,3*i+3)) for i in range(4)]
# Include all layouts, even ones known impossible, for independence of prior local classification.
L=[g for p in partitions(8) for g in layouts(p)]
# TD(4,3) enumeration of exact cross-pair covers
cross={tuple(sorted((x,y))) for i,j in combinations(range(4),2) for x in G[i] for y in G[j]};B=list(product(*G));cov=[set(combinations(b,2)) for b in B];by={p:[i for i,c in enumerate(cov) if p in c] for p in cross}
def ec(rem):
 if not rem:yield ();return
 opts=min(([i for i in by[p] if cov[i]<=rem] for p in rem),key=len)
 for i in opts:
  for rest in ec(rem-cov[i]):yield (sum(1<<x for x in B[i]),*rest)
TD=sorted(set(tuple(sorted(t)) for t in ec(cross)));assert len(TD)==72
with open('one_low_input.txt','w') as f:
 print(len(TD),len(L),file=f)
 for t in TD:print(*t,file=f)
 for g in L:print(*(x for q in g for x in q),file=f)
print('TDs',len(TD),'layouts',len(L))
