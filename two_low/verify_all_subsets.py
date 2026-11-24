
if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

from local import local
from itertools import combinations, permutations, product
from pathlib import Path
from collections import Counter
import json,sys,time
D=Path(__file__).parent; X=set(range(14))-{0,6}; reps=json.loads((D/'reps.json').read_text()); typ=int(sys.argv[1]); F={tuple(sorted(b)) for b in reps[typ]};
G=[tuple(x for x in b if x not in {0,6}) for b in sorted(F) if {0,6}<=set(b)]; A={tuple(x for x in b if x!=0) for b in F if 0 in b and 6 not in b}; B={tuple(x for x in b if x!=6) for b in F if 6 in b and 0 not in b};auts=[]
for gp in permutations(G):
 for p in product(*(tuple(permutations(g)) for g in gp)):
  m={x:y for a,b in zip(G,p) for x,y in zip(a,b)}
  if all(tuple(sorted(m[x] for x in a)) in A for a in A) and all(tuple(sorted(m[x] for x in b)) in B for b in B):auts.append(m)
pend=set(X);orbs=[]
while pend:
 y=min(pend); o={m[y] for m in auts};pend-=o;orbs.append((y,sorted(o)))
print('Type',typ,'auts',len(auts),'orbits',orbs,flush=True)
blocks=list(combinations(sorted(X),5));idx={b:i for i,b in enumerate(blocks)};by={y:sum(1<<i for i,b in enumerate(blocks) if y in b) for y in X}; doms={}
for y,o in sorted(orbs,key=lambda p:-len(p[1])):
 # In type 3 we can ignore the three-point orbit; this relaxes the problem.
 if typ==3 and len(o)==3:continue
 t=time.monotonic(); f=D/f'type{typ}_local_{y}.json'
 if f.exists() and "--fresh" not in sys.argv:raw=json.loads(f.read_text())
 else:
  raw=sorted(set(local(list(map(set,F)),y)))
  if f.exists():assert json.loads(f.read_text())==json.loads(json.dumps(raw))
  f.write_text(json.dumps(raw))
 assert len(raw)==(1522 if typ==1 and y==1 else 140)
 print('Local',y,len(raw),'seconds',round(time.monotonic()-t,3),flush=True)
 for z in o:
  m=next(m for m in auts if m[y]==z)
  doms[z]={sum(1<<idx[tuple(sorted(m[v] for v in [y,*b]))] for b in l) for l in raw}
# At most four high vertices, so at least eight vertices of X have degree 15.
# For a relaxation, ignore vertices for which no local domain was enumerated.
Y=set(doms); k=len(Y)-4; sub=list(combinations(sorted(Y),k))
print('Subsets to test',len(sub),'size',k,flush=True)
# Necessary agreement of full common-block signatures.
N=0;leaves=0;hist=Counter(); survivors=[]
def ac(dom):
 while True:
  before=sum(map(len,dom.values()))
  for x,y in combinations(dom,2):
   mask=by[x]&by[y];common={a&mask for a in dom[x]}&{b&mask for b in dom[y]}
   if not common:return False
   dom[x]={a for a in dom[x] if a&mask in common};dom[y]={b for b in dom[y] if b&mask in common}
  if sum(map(len,dom.values()))==before:return True

def visit(dom):
 global N,leaves
 N+=1
 if not ac(dom):return
 forced=0
 for d in dom.values():
  it=iter(d); common=next(it)
  for b in it:common&=b
  forced|=common
 if forced.bit_count()>20:return
 if all(len(d)==1 for d in dom.values()):
  leaves+=1;hist[forced.bit_count()]+=1
  if len(survivors)<20:survivors.append([b for i,b in enumerate(blocks) if forced>>i&1])
  return
 y=min((y for y in dom if len(dom[y])>1),key=lambda y:len(dom[y]))
 for v in sorted(dom[y]):
  child=dom.copy();child[y]={v};visit(child)
for s in sub:
 a=N;b=leaves;dom={y:doms[y].copy() for y in s};ok=ac(dom)
 if ok:visit(dom)
print('FINAL',typ,'states',N,'leaves',leaves,'hist',dict(hist),flush=True)
assert N==0 and leaves==0
(D/f'type{typ}_survivors.json').write_text(json.dumps(survivors))
