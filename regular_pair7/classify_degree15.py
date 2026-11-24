"""Exact finite classification of local degree profiles for 15 distinct 4-sets covering all pairs on 13 points.
No solver dependencies. Every zero-excess point can be normalized to 0; four blocks through it partition the other 12 into triples. For a given multiset of positive excesses, enumerate every allocation to these four triples modulo their permutations and internal permutations. Then cover every remaining pair incident to a zero-excess point exactly once. Residual all-positive blocks are enumerated separately. No heuristic pruning.
"""

if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

from itertools import combinations
from collections import Counter
from functools import lru_cache
import json
from pathlib import Path
G=tuple(tuple(range(1+3*i,4+3*i)) for i in range(4)); F=tuple((0,*g) for g in G)
P=tuple(combinations(range(1,13),2)); fixed={p for b in F for p in combinations(b,2)}

def partitions(n,lo=1):
    if n==0:yield ()
    for k in range(lo,n+1):
        for p in partitions(n-k,k):yield (k,*p)

def layouts(profile):
    def rec(remaining,last,gs):
        if not remaining:
            yield gs;return
        for group in sorted(set(combinations(remaining,3))):
            if group<last:continue
            left=list(remaining)
            for i in group:left.remove(i)
            yield from rec(tuple(left),group,gs+(group,))
    return rec(tuple(sorted((0,)*(12-len(profile))+profile)),(),())

def solve(groups):
    w={x:a for g,ws in zip(G,groups) for x,a in zip(g,ws)}
    H=tuple(x for x in w if w[x]); hs=set(H); hi={v:i for i,v in enumerate(H)}
    goal=tuple(3+w[x] for x in H)
    E=[p for p in P if not set(p)<=hs and p not in fixed]; ei={p:i for i,p in enumerate(E)}
    hp=list(combinations(H,2)); pi={p:i for i,p in enumerate(hp)}
    B=[]; masks=[]; hm=[]; bh=[]; containing=[[] for _ in E]
    for b in combinations(range(1,13),4):
        pairs=list(combinations(b,2))
        if any(p in fixed and not set(p)<=hs for p in pairs):continue
        mask=sum(1<<ei[p] for p in pairs if p in ei); hmask=sum(1<<pi[p] for p in pairs if p in pi)
        j=len(B); B.append(b); masks.append(mask);hm.append(hmask);bh.append(tuple(hi[v] for v in b if v in hs))
        for p in pairs:
            if p in ei:containing[ei[p]].append(j)
    full=(1<<len(E))-1; allh=(1<<len(hp))-1; init_h=sum(1<<i for i,p in enumerate(hp) if p in fixed)
    empty=[j for j,mask in enumerate(masks) if mask==0]; nodes=0
    @lru_cache(None)
    def tail(deg,coveredh,n):
        k=11-n
        if k<0 or k>len(empty) or sum(goal[i]-deg[i] for i in range(len(H)))!=4*k:return None
        for js in combinations(empty,k):
            ds=list(deg); cov=coveredh
            for j in js:
                for i in bh[j]:ds[i]+=1
                cov|=hm[j]
            if tuple(ds)==goal and cov==allh:return js
        return None
    @lru_cache(None)
    def dfs(rem,deg,coveredh,n):
        nonlocal nodes
        nodes+=1
        if not rem:return tail(deg,coveredh,n)
        if n>=11 or rem.bit_count()>6*(11-n):return None
        best=None;bits=rem
        while bits:
            bit=bits&-bits;i=bit.bit_length()-1;bits^=bit
            opts=[j for j in containing[i] if masks[j]&rem==masks[j] and all(deg[k]<goal[k] for k in bh[j])]
            if not opts:return None
            if best is None or len(opts)<len(best):
                best=opts
                if len(best)==1:break
        for j in best:
            d=list(deg)
            for k in bh[j]:d[k]+=1
            if any(t-v>10-n for t,v in zip(goal,d)):continue
            result=dfs(rem^masks[j],tuple(d),coveredh|hm[j],n+1)
            if result is not None:return (j,*result)
        return None
    sol=dfs(full,(0,)*len(H),init_h,0)
    if sol is not None:
        blocks=F+tuple(B[j] for j in sol)
        assert len(blocks)==len(set(blocks))==15
        c=Counter(p for b in blocks for p in combinations(b,2));assert set(c)==set(combinations(range(13),2))
        r=Counter(x for b in blocks for x in b); assert r[0]==4 and all(r[x]==4+w[x] for x in w)
    else:blocks=None
    return nodes,blocks

if __name__=='__main__':
    import sys
    maxh=int(sys.argv[1]) if len(sys.argv)>1 else 5
    report=[]
    for profile in sorted(partitions(8),key=lambda p:(len(p),p)):
        if len(profile)>maxh:continue
        total=0;n=0;witness=None
        for groups in layouts(profile):
            nodes,sol=solve(groups);total+=nodes;n+=1
            if sol is not None:
                witness=sol;break
        print(profile,'layouts',n,'nodes',total,'feasible',witness is not None,flush=True)
        report.append(dict(profile=profile,layouts_checked=n,nodes=total,witness=witness))
    Path(__file__).with_name(f'local_degree_profiles_{maxh}.json').write_text(json.dumps(report,indent=2))
