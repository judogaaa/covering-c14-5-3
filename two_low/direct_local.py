"""Enumerate every local completion at point 1 in the restricted type-0 branch.
No precomputed degree-profile classification or numerical solver is used.
"""

if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

from itertools import combinations
from collections import Counter
from pathlib import Path
import json
D=Path(__file__).parent
F=list(map(set,json.loads((D/'reps.json').read_text())[0])); X=set(range(14))-{0,6}

def local(y):
    Q=tuple(sorted(X-{y})); P=list(combinations(Q,2)); known=[b-{y} for b in F if y in b]; assert len(known)==7
    fixed=Counter(p for b in known for p in combinations(sorted(b),2)); d=Counter(z for b in known for z in b)
    lower={z:max(0,d[z]+(sum(fixed[tuple(sorted((z,t)))]==0 for t in Q if t!=z)+2)//3-4) for z in Q}
    roots=[tuple(tuple(sorted(b-{r})) for b in known if r in b) for r in (0,6)]
    assert all(len(g)==4 and len(set().union(*map(set,g)))==12 for g in roots)
    feasible=[]
    cache={}
    def extension(w):
        H=tuple(z for z in Q if w[z]); hs=set(H); hidx={z:i for i,z in enumerate(H)}
        goal=tuple(4+w[z]-d[z] for z in H)
        if H not in cache:
            E=[p for p in P if not fixed[p] and not set(p)<=hs]; ei={p:i for i,p in enumerate(E)}
            hp=[p for p in P if not fixed[p] and set(p)<=hs]; hi={p:i for i,p in enumerate(hp)}
            C=[];m=[];h=[];bh=[];by=[[] for _ in E]
            for b in combinations(Q,4):
                pairs=list(combinations(b,2))
                if any(fixed[p] and not set(p)<=hs for p in pairs):continue
                j=len(C); C.append(b);m.append(sum(1<<ei[p] for p in pairs if p in ei));h.append(sum(1<<hi[p] for p in pairs if p in hi));bh.append(tuple(hidx[z] for z in b if z in hs))
                for p in pairs:
                    if p in ei:by[ei[p]].append(j)
            cache[H]=(E,hp,C,m,h,bh,by,[j for j,mask in enumerate(m) if not mask])
        E,hp,C,m,h,bh,by,empty=cache[H]; full=(1<<len(E))-1; fullh=(1<<len(hp))-1
        def dfs(rem,deg,cov,n):
            if not rem:
                k=8-n
                if k<0 or k>len(empty) or sum(t-v for t,v in zip(goal,deg))!=4*k:return
                for js in combinations(empty,k):
                    ds=list(deg);cv=cov
                    for j in js:
                        for i in bh[j]:ds[i]+=1
                        cv|=h[j]
                    if tuple(ds)==goal and cv==fullh:yield js
                return
            if n>=8 or rem.bit_count()>6*(8-n):return
            best=None;bits=rem
            while bits:
                bit=bits&-bits;i=bit.bit_length()-1;bits^=bit
                opts=[j for j in by[i] if m[j]&rem==m[j] and all(deg[k]<goal[k] for k in bh[j])]
                if not opts:return
                if best is None or len(opts)<len(best):
                    best=opts
                    if len(best)==1:break
            for j in best:
                ds=list(deg)
                for i in bh[j]:ds[i]+=1
                if any(t-v>7-n for t,v in zip(goal,ds)):continue
                for r in dfs(rem^m[j],tuple(ds),cov|h[j],n+1):yield (j,*r)
        out=[]
        for sol in dfs(full,(0,)*len(H),0,0):
            blocks=[tuple(sorted(b)) for b in known]+[C[j] for j in sol]
            assert len(blocks)==len(set(blocks))==15
            assert set(p for b in blocks for p in combinations(b,2))==set(combinations(sorted(set(range(14))-{y}),2))
            r=Counter(z for b in blocks for z in b);assert all(r[z]==4+w[z] for z in w)
            out.append(tuple(sorted(C[j] for j in sol)))
        return out
    # Independent enumeration: no stored classification or layout filters.
    # The lower bounds sum to four, leaving four units to distribute over 11 points.
    from itertools import combinations_with_replacement
    assert sum(lower.values())==4
    tested=0;valid=0
    for extra in combinations_with_replacement(Q,8-sum(lower.values())):
        w={0:0,6:0,**lower}
        for z in extra:w[z]+=1
        tested+=1
        sol=extension(w)
        if sol:valid+=1;feasible.extend(sol)
    assert (tested,valid)==(1001,141)
    print('Weight assignments tested:',tested,'locally feasible:',valid,flush=True)
    return feasible
if __name__=='__main__':
    import sys
    ys=[1]
    out={y:sorted(set(local(y))) for y in ys}
    assert len(out[1])==1522
    print({y:len(v) for y,v in out.items()},flush=True)
    (Path(__file__).parent/"all_local_direct.json").write_text(json.dumps(out,indent=2))
