
if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

from itertools import combinations,permutations,product
from collections import Counter
from pathlib import Path
import json
D=Path(__file__).resolve().parent;F={tuple(sorted(b)) for b in json.load(open(D/'reps.json'))[0]};X=set(range(14))-{0,6};H={4,8,10,12};Y=sorted(X-H)
G=[tuple(x for x in b if x not in {0,6}) for b in sorted(F) if {0,6}<=set(b)]; A={tuple(x for x in b if x!=0) for b in F if 0 in b and 6 not in b}; B={tuple(x for x in b if x!=6) for b in F if 6 in b and 0 not in b};pms={}
for gp in permutations(G):
 for p in product(*(tuple(permutations(g)) for g in gp)):
  m={x:y for a,b in zip(G,p) for x,y in zip(a,b)}
  if all(tuple(sorted(m[x] for x in a)) in A for a in A) and all(tuple(sorted(m[x] for x in b)) in B for b in B):
   pms[m[1]]=m
assert set(pms)==set(Y)
assert all({m[z] for z in H}==H for m in pms.values())
raw=json.load(open(D/'all_local_direct.json'))['1'];assert len(raw)==1522
blocks=list(combinations(sorted(X),5));idx={b:i for i,b in enumerate(blocks)};by={y:sum(1<<i for i,b in enumerate(blocks) if y in b) for y in X}
Doms={y:{sum(1<<idx[tuple(sorted(m[z] for z in [1,*b]))] for b in l) for l in raw} for y,m in pms.items()}
assert all(len(d)==1522 for d in Doms.values())
# Pairwise agreement on the entire family of blocks containing both points.
# Propagation preserves every globally consistent assignment.
def ac(dom):
 while True:
  before=sum(map(len,dom.values()))
  for x,y in combinations(Y,2):
   mask=by[x]&by[y];common={a&mask for a in dom[x]}&{b&mask for b in dom[y]}
   dom[x]={a for a in dom[x] if a&mask in common};dom[y]={b for b in dom[y] if b&mask in common}
   if not dom[x] or not dom[y]:return False
  after=sum(map(len,dom.values()))
  if after==before:return True
ok=ac(Doms);print('Arc consistency:',ok,{y:len(d) for y,d in Doms.items()},flush=True)
N=0;leaf=0;hist=Counter();profiles=Counter();good=0
U=set(combinations(sorted(X),3))-{t for b in F for t in combinations(b,3)}
def visit(dom):
 global N,leaf,good
 N+=1
 if not ac(dom):return
 if all(len(d)==1 for d in dom.values()):
  leaf+=1
  forced=0
  for d in dom.values():forced|=next(iter(d))
  sol=[b for i,b in enumerate(blocks) if forced>>i&1]
  hist[len(sol)]+=1
  deg=tuple(sorted((forced&by[h]).bit_count() for h in H))
  miss=len(U-{t for b in sol for t in combinations(b,3)})
  profiles[(len(sol),deg,miss)]+=1
  if len(sol)==20 and deg==(9,9,9,9) and miss==0:good+=1
  return
 y=min((y for y in Y if len(dom[y])>1),key=lambda y:len(dom[y]))
 for v in sorted(dom[y]):
  child=dom.copy();child[y]={v};visit(child)
if ok:visit(Doms)
print('Search states',N,'pairwise consistent complete assignments',leaf,'union size histogram',sorted(hist.items()))
print('Profiles (union size, high degrees, uncovered triples):',sorted(profiles.items()))
assert good==0 and leaf==36 and hist==Counter({22:36})
assert profiles==Counter({(22,(11,11,11,13),0):8,(22,(11,11,12,12),0):28})
print("PASS: type 0 requires more than 20 residual blocks.")
