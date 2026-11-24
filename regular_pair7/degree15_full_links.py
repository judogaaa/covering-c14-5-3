"""Enumerate every 15-block pair covering for specified normalized weight layouts.
Proof scope: a fixed distinguished zero-excess point and four fixed triples.
No SAT solver used. All labelled completions, not just one witness per layout.
"""

if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

from itertools import combinations, permutations, product
from collections import Counter
from pathlib import Path
import json
from classify_degree15 import G,F,P,fixed

def enumerate_links(groups):
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
    def dfs(rem,deg,coveredh,chosen):
        nonlocal nodes
        nodes+=1; n=len(chosen)
        if not rem:
            k=11-n
            if k<0 or k>len(empty) or sum(goal[i]-deg[i] for i in range(len(H)))!=4*k:return
            for js in combinations(empty,k):
                ds=list(deg); cov=coveredh
                for j in js:
                    for i in bh[j]:ds[i]+=1
                    cov|=hm[j]
                if tuple(ds)==goal and cov==allh:yield tuple(sorted(F+tuple(B[j] for j in chosen+js)))
            return
        if n>=11 or rem.bit_count()>6*(11-n):return
        best=None;bits=rem
        while bits:
            bit=bits&-bits;i=bit.bit_length()-1;bits^=bit
            opts=[j for j in containing[i] if masks[j]&rem==masks[j] and all(deg[k]<goal[k] for k in bh[j])]
            if not opts:return
            if best is None or len(opts)<len(best):best=opts
            if len(best)==1:break
        for j in best:
            d=list(deg)
            for k in bh[j]:d[k]+=1
            if any(t-v>10-n for t,v in zip(goal,d)):continue
            yield from dfs(rem^masks[j],tuple(d),coveredh|hm[j],chosen+(j,))
    answers=set(dfs(full,(0,)*len(H),init_h,()))
    for a in answers:
        assert len(a)==len(set(a))==15
        assert set(p for b in a for p in combinations(b,2))==set(combinations(range(13),2))
        r=Counter(x for b in a for x in b)
        assert r[0]==4 and all(r[x]==4+w[x] for x in w)
    return answers,nodes

def group_perms(groups):
    for gp in permutations(range(4)):
        if any(groups[i]!=groups[gp[i]] for i in range(4)):continue
        options=[]
        for i in range(4):
            options.append([p for p in permutations(G[gp[i]]) if all(groups[i][j]==groups[gp[i]][G[gp[i]].index(p[j])] for j in range(3))])
        for ps in product(*options):yield (0,)+tuple(x for p in ps for x in p)

def representatives(answers,groups):
    ps=list(group_perms(groups)); pending=set(answers); reps=[]
    while pending:
        a=min(pending)
        orbit={tuple(sorted(tuple(sorted(p[x] for x in b)) for b in a)) for p in ps}
        assert orbit<=answers
        pending-=orbit; reps.append(a)
    return reps,len(ps)

if __name__=='__main__':
    import sys
    R=json.loads(Path(__file__).with_name('local_degree_layouts.json').read_text()); report=[]
    for row in R:
        if 3 not in row['profile'] and '--all' not in sys.argv:continue
        for c in row['cases']:
            if c['witness'] is None:continue
            g=tuple(map(tuple,c['groups'])); A,n=enumerate_links(g); reps,order=representatives(A,g)
            print(g,len(A),len(reps),order,n,flush=True)
            report.append(dict(groups=g,labelled=len(A),nodes=n,group_order=order,representatives=reps))
    Path(__file__).with_name('degree15_full_links.json').write_text(json.dumps(report,indent=2))
    print('TOTAL',sum(r['labelled'] for r in report),sum(len(r['representatives']) for r in report),sum(r['nodes'] for r in report),flush=True)
