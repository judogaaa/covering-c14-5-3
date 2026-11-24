"""Verify the new two-low-point exclusions with integers only, no numerical solver."""

if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

from itertools import combinations, permutations, product
from collections import Counter
from pathlib import Path
import json
D=Path(__file__).parent; V=set(range(14)); Z={0,6}; X=V-Z
reps=json.loads((D/'reps.json').read_text()); F0={tuple(b) for b in reps[0]}; G=sorted(tuple(x for x in b if x not in Z) for b in F0 if Z<=set(b)); assert len(G)==4 and set().union(*map(set,G))==X
A=frozenset(tuple(x for x in b if x!=0) for b in F0 if 0 in b and 6 not in b)
P={tuple(sorted((a,b))) for g,h in combinations(G,2) for a in g for b in h}; L={tuple(sorted(t)) for t in product(*G)}; cp={b:set(combinations(b,2)) for b in L}; idx={p:[b for b in L if p in cp[b]] for p in P}
def ec(rem):
 if not rem:yield frozenset();return
 opts=min(([b for b in idx[p] if cp[b]<=rem] for p in rem),key=len)
 for b in opts:
  for r in ec(rem-cp[b]):yield r|{b}
links=set(ec(P));assert len(links)==72
images=set(); orbit=[set() for _ in reps]; seconds=[]
for rep in reps:
 F={tuple(b) for b in rep};assert len(F)==22 and {b for b in F if 0 in b}=={b for b in F0 if 0 in b}
 for x in Z:assert Counter(t for b in F if x in b for t in combinations(sorted(set(b)-{x}),2))==Counter(combinations(sorted(V-{x}),2))
 seconds.append(frozenset(tuple(x for x in b if x!=6) for b in F if 6 in b and 0 not in b))
for q in permutations(range(4)):
 for ps in product(*(list(permutations(G[i])) for i in q)):
  f={a:b for g,h in zip(G,ps) for a,b in zip(g,h)}
  def move(S):return frozenset(tuple(sorted(f[x] for x in b)) for b in S)
  aa=move(A);images.add(aa)
  if aa==A:
   for j,s in enumerate(seconds):orbit[j].add(move(s))
assert images==links and set().union(*orbit)==links and sum(map(len,orbit))==len(links)
assert list(map(len,orbit))==[27,24,12,8,1]
print('PASS: five relative orbits exhaust all 72 links:',list(map(len,orbit)))
certs={(a['rep'],a['point']):{c['surplus']:c['weights'] for c in a['cases']} for a in json.loads((D/'local_certs.json').read_text())}; used=set(); ncert=0; nchecks=0; out=[]
for i,rep in enumerate(reps):
 F=list(map(set,rep)); assert all(sum(y in b for b in F)==7 for y in X); forced=[]; miss=len(set(combinations(sorted(X),3))-{t for b in F for t in combinations(sorted(b),3)})
 for y in sorted(X):
  Q=sorted(X-{y}); P=[p for p in combinations(Q,2) if not any({y,*p}<=b for b in F)]; h=Counter(z for p in P for z in p); l={z:(h[z]+2)//3 for z in Q}
  if sum(l.values())>32:forced.append(y);continue
  if (i,y) not in certs:continue
  assert sum(l.values())==31 and set(certs[i,y])==set(Q);used.add((i,y))
  for s in Q:
   cap={z:l[z]+(z==s) for z in Q};tight={z for z in Q if h[z]==3*cap[z]};w=certs[i,y][s];assert len(w)==len(P)+len(Q) and all(isinstance(a,int) and a>=0 for a in w);pw=dict(zip(P,w[:len(P)])); vw=dict(zip(Q,w[len(P):])); worst=0
   for b in combinations(Q,4):
    pairs=list(combinations(b,2))
    if any(p not in pw for p in pairs if tight.intersection(p)):continue
    worst=max(worst,sum(pw.get(p,0) for p in pairs)-sum(vw[z] for z in b));nchecks+=1
   assert sum(pw.values())-sum(cap[z]*vw[z] for z in Q)>8*worst
   ncert+=1
  forced.append(y)
 if i==0:assert set(forced)=={4,8,10,12},forced
 out.append(len(forced)); print('orbit',i,'missing',miss,'forced degree >=16:',forced)
assert used==set(certs) and out==[4,0,10,0,12]
print('PASS:',ncert,'integer certificates;',nchecks,'candidate-block inequalities checked.')
# Deficit below 15 equals excess above 15. With exactly two low points, at most four extra incidences exist.
assert out[2]>4 and out[4]>4 and out[0]>3
print('PASS: orbits 2 and 4 impossible for any two low points; orbit 0 impossible if either has degree 14.')
