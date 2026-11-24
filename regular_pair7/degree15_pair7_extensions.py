"""Exact two-link extension test for a regular cover containing a pair of codegree 7.
Uses the 10 normalized representatives from degree15_full_links.py.
All second-root links are enumerated, then residual point budgets are tested.
"""

if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

from itertools import combinations
from collections import Counter
from pathlib import Path
import json
D=Path(__file__).parent
V=tuple(range(14)); P=tuple(combinations(V,2)); T=set(combinations(V,3))

def extensions(a):
    x=13; r=Counter(z for b in a for z in b); y=next(z for z in r if r[z]==7)
    Q=tuple(z for z in range(13) if z!=y)
    fixed_parent=[tuple(sorted((*b,x))) for b in a]
    fixed_y=[tuple(z for z in b if z!=y) for b in fixed_parent if y in b]
    assert len(fixed_y)==7
    fixed=Counter(p for b in fixed_y for p in combinations(b,2)); deg=Counter(z for b in fixed_y for z in b)
    lower={z:max(0,deg[z]+(sum(fixed[tuple(sorted((z,t)))]==0 for t in Q if t!=z)+2)//3-4) for z in Q}
    # pairs with x already covered; no future blocks through x.
    assert all(fixed[tuple(sorted((x,z)))]>=1 for z in Q)
    cand_assign=0; nodes=0; completions=0; residual_ok=0; min_def=1000; survivors=[]
    for profile in ((1,1,1,2),(1,1,1,1,1)):
      for high in combinations(Q,len(profile)):
        if any(lower[z]>0 for z in Q if z not in high):continue
        for doubles in ([(z,) for z in high] if 2 in profile else [()]):
          w={z:(2 if z in doubles else 1 if z in high else 0) for z in Q}
          if any(w[z]<lower[z] for z in Q):continue
          H=tuple(high); hs=set(H); hi={z:i for i,z in enumerate(H)}
          # If any pair involving a degree-4 point was repeated, impossible.
          if any(v>1 and any(z!=x and not w[z] for z in p) for p,v in fixed.items()):continue
          goal=tuple(4+w[z]-deg[z] for z in H)
          if min(goal)<0:continue
          cand_assign+=1
          E=[p for p in combinations(Q,2) if not fixed[p] and not set(p)<=hs];ei={p:i for i,p in enumerate(E)}
          hp=[p for p in combinations(H,2) if not fixed[p]];pi={p:i for i,p in enumerate(hp)}
          C=[]; m=[]; h=[]; bh=[]; by=[[] for _ in E]
          for b in combinations(Q,4):
            pairs=list(combinations(b,2))
            if any(fixed[p] and not set(p)<=hs for p in pairs):continue
            j=len(C); C.append(b);m.append(sum(1<<ei[p] for p in pairs if p in ei));h.append(sum(1<<pi[p] for p in pairs if p in pi));bh.append(tuple(hi[z] for z in b if z in hs))
            for p in pairs:
              if p in ei:by[ei[p]].append(j)
          empty=[j for j in range(len(C)) if not m[j]]
          full=(1<<len(E))-1; fullh=(1<<len(hp))-1
          def dfs(rem,d,cov,chosen):
            nonlocal nodes
            nodes+=1;n=len(chosen)
            if not rem:
              k=8-n
              if k<0 or k>len(empty) or sum(t-v for t,v in zip(goal,d))!=4*k:return
              for js in combinations(empty,k):
                ds=list(d);cv=cov
                for j in js:
                  for z in bh[j]:ds[z]+=1
                  cv|=h[j]
                if tuple(ds)==goal and cv==fullh:yield chosen+js
              return
            if n>=8 or rem.bit_count()>6*(8-n):return
            best=None; bits=rem
            while bits:
              bit=bits&-bits;i=bit.bit_length()-1;bits^=bit
              opts=[j for j in by[i] if m[j]&rem==m[j] and all(d[z]<goal[z] for z in bh[j])]
              if not opts:return
              if best is None or len(opts)<len(best):best=opts
              if len(best)==1:break
            for j in best:
              ds=list(d)
              for z in bh[j]:ds[z]+=1
              if any(t-v>7-n for t,v in zip(goal,ds)):continue
              yield from dfs(rem^m[j],tuple(ds),cov|h[j],chosen+(j,))
          for sol in dfs(full,(0,)*len(H),0,()):
            b=fixed_y+[C[j] for j in sol]
            assert len(b)==len(set(b))==15
            assert set(p for u in b for p in combinations(u,2))==set(combinations(tuple(z for z in V if z!=y),2))
            rd=Counter(z for u in b for z in u);assert rd[x]==7 and all(rd[z]==4+w[z] for z in Q)
            F=fixed_parent+[tuple(sorted((*C[j],y))) for j in sol]
            assert len(F)==len(set(F))==23
            completions+=1
            missing=T-{t for u in F for t in combinations(u,3)}
            counts=Counter(z for u in F for z in u)
            h2=Counter(p for t in missing for p in combinations(t,2))
            # lower bound for each pair considering uncovered triples and pair degree >=4.
            pd=Counter(p for u in F for p in combinations(u,2))
            need={p:max(0,4-pd[p],(h2[p]+2)//3) for p in P}
            lowerdeg={z:(sum(need[p] for p in P if z in p)+3)//4 for z in V}
            deficit=max(counts[z]+lowerdeg[z]-15 for z in V)
            min_def=min(min_def,deficit)
            if deficit<=0:
              residual_ok+=1
              survivors.append(F)
    return dict(y=y,assignments=cand_assign,nodes=nodes,completions=completions,residual_ok=residual_ok,min_deficit=min_def,survivors=survivors)
if __name__=='__main__':
    R=json.loads((D/'degree15_full_links.json').read_text());out=[]
    for row in R:
      for a in row['representatives']:
        result=extensions(a);out.append(result)
        print({k:v for k,v in result.items() if k!='survivors'},flush=True)
    (D/'degree15_pair7_extensions.json').write_text(json.dumps(out,indent=2))
    print('TOTAL', {k:sum(r[k] for r in out) for k in ('assignments','nodes','completions','residual_ok')},flush=True)
