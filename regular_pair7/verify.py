"""Exact verification of the regular pair-7 exclusion. Standard library only.
Run with assertions enabled (python verify.py, not python -O).
"""

if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

from itertools import combinations
from collections import Counter
from pathlib import Path
import json
from classify_degree15 import partitions, layouts
from degree15_full_links import enumerate_links, representatives
from degree15_pair7_extensions import extensions
D=Path(__file__).parent

def load(name):return json.loads((D/name).read_text())
def norm(F):return tuple(sorted(tuple(sorted(b)) for b in F))

def verify_case(r,tree):
 F=r['blocks'];X=tuple(z for z in range(14) if z not in (13,r['y']));B=list(combinations(X,5));T=list(combinations(X,3));P=list(combinations(X,2));bs=[set(b) for b in B]
 covered={t for b in F for t in combinations(b,3)};p=Counter(t for b in F for t in combinations(b,2));d=Counter(z for b in F for z in b)
 rows=[]
 def add(s,v,sign):rows.append((tuple(s),sign*v,sign))
 add((),19,1);add((),19,-1)
 for z in X:add((z,),15-d[z],1);add((z,),15-d[z],-1)
 for q in P:add(q,max(0,4-p[q]),1);add(q,7-p[q],-1)
 for t in T:
  if t not in covered:add(t,1,1)
 for b in B:add(b,1,-1)
 def rec(tree,rows):
  if 'cert' in tree:
   w=tree['cert'];assert w and len(set(i for i,v in w))==len(w)
   assert all(type(i)==int and type(v)==int and 0<=i<len(rows) and v>0 for i,v in w)
   weighted=[(set(rows[i][0]),rows[i][1]*v,rows[i][2]*v) for i,v in w]
   assert sum(rhs for s,rhs,sgn in weighted)>0
   assert all(sum(sgn for s,rhs,sgn in weighted if s<=b)<=0 for b in bs)
   return 1
  q=tuple(tree['branch']);k=tree['floor'];assert set(q)<=set(X) and len(q)==len(set(q)) and len(q) in (2,5) and type(k)==int
  return rec(tree['left'],rows+[(q,-k,-1)])+rec(tree['right'],rows+[(q,k+1,1)])
 return rec(tree,rows)

def main():
 # Every degree-15 link has at least one degree-4 point. Normalize it to 0.
 # Exhaust ALL layouts with some weight >= 3, including weights > 3.
 saved=load('degree15_full_links.json'); lookup={tuple(map(tuple,r['groups'])):r for r in saved}; got=set();counts=Counter()
 for profile in partitions(8):
  if max(profile)<3:continue
  for g in layouts(profile):
   A,n=enumerate_links(g);counts['layouts']+=1;counts['nodes']+=n
   if not A:continue
   assert max(profile)==3 and profile in ((1,1,1,1,1,3),(1,1,1,2,3))
   reps,_=representatives(A,g);r=lookup[g];assert len(A)==r['labelled'] and set(map(norm,reps))==set(map(norm,r['representatives']))
   got.add(g);counts['labelled']+=len(A);counts['reps']+=len(reps)
 assert got==set(lookup) and counts['layouts']==98 and counts['labelled']==208 and counts['reps']==10
 print('PASS: all 98 high-weight layouts; 208 labelled links, 10 representatives. No weight >3.',flush=True)
 E=load('degree15_pair7_extensions.json');actual=[];j=0
 for r in saved:
  for a in r['representatives']:
   result=extensions(a);expected=E[j];j+=1
   assert all(result[k]==expected[k] for k in ('y','assignments','nodes','completions','residual_ok','min_deficit'))
   assert set(map(norm,result['survivors']))==set(map(norm,expected['survivors']))
   actual.extend((F,result['y']) for F in result['survivors'])
 assert len(E)==j==10 and sum(r['completions'] for r in E)==80 and len(actual)==24
 print('PASS: all 80 second-link completions; 56 fail integer point budgets, 24 remain.',flush=True)
 R=load('degree15_pair7_reps.json'); maps=load('orbit_maps.json'); assert len(R)==4 and len(maps)==len(actual)
 counts=Counter()
 for (F,y),m in zip(actual,maps):
  i=m['target'];p=m['permutation'];assert sorted(p)==list(range(14));assert {p[13],p[y]}=={13,R[i]['y']}
  assert norm([tuple(p[z] for z in b) for b in F])==norm(R[i]['blocks']);counts[i]+=1
 assert [counts[i] for i in range(4)]==[r['count'] for r in R]
 leaves=sum(verify_case(r,load(f'pair7_exact_case{i}.json')) for i,r in enumerate(R))
 assert leaves==5
 print('PASS: 24 explicit relabellings to 4 classes; 5 exact integer certificates.',flush=True)
 print('THEOREM: every regular 42-block (14,5,3) covering has pair codegrees <= 6.',flush=True)
 print('This does not exclude regular covers with codegrees <= 6, or nonregular covers.',flush=True)
if __name__=='__main__':main()
