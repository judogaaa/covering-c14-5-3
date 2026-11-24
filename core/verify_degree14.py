"""Self-contained integer enumeration of 14 four-sets covering all pairs on 13 points."""

if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

from itertools import combinations,combinations_with_replacement
from collections import Counter
G=[tuple(range(3*i,3*i+3)) for i in range(4)]
fixed=[tuple((*g,12)) for g in G]
P=list(combinations(range(12),2));fixedpairs={p for b in fixed for p in combinations(b,2) if 12 not in p}
allpairs=set(combinations(range(13),2))
def layouts(total):
    triples=list(combinations_with_replacement(range(total+1),3))
    def rec(start,left,n):
        if n==0:
            if left==0:yield ()
            return
        for j in range(start,len(triples)):
            g=triples[j];s=sum(g)
            if s<=left:
                for a in rec(j,left-s,n-1):yield (g,)+a
    for gs in rec(0,total,4):yield tuple(v for g in gs for v in g)
def solve(w):
    H={x for x in range(12) if w[x]};goal=[3+v for v in w];E=[p for p in P if p not in fixedpairs and not set(p)<=H];Hmiss=[p for p in P if p not in fixedpairs and set(p)<=H];ei={p:i for i,p in enumerate(E)};hi={p:i for i,p in enumerate(Hmiss)};B=[];em=[];hm=[];by=[[] for _ in E];pure=[]
    for b in combinations(range(12),4):
        ps=list(combinations(b,2))
        if any(p in fixedpairs and not set(p)<=H for p in ps):continue
        j=len(B);B.append(b);m=sum(1<<ei[p] for p in ps if p in ei);em.append(m);hm.append(sum(1<<hi[p] for p in ps if p in hi));
        if not m:pure.append(j)
        for p in ps:
            if p in ei:by[ei[p]].append(j)
    fullh=(1<<len(Hmiss))-1;d=[0]*12;chosen=[];ans=0
    def finish(rem,deg,h):
        nonlocal ans
        if rem==0:
            k=10-len(chosen)
            for tail in combinations(pure,k):
                ds=deg.copy();cov=h
                for j in tail:
                    for x in B[j]:ds[x]+=1
                    cov|=hm[j]
                if ds!=goal or cov!=fullh:continue
                L=fixed+[B[j] for j in chosen+list(tail)];c=Counter(p for b in L for p in combinations(b,2));assert len(L)==len(set(L))==14 and set(c)==allpairs
                assert any(all(c[p]>=2 for p in combinations(b,2)) for b in L),L
                ans+=1
            return
        n=len(chosen)
        if n==10 or rem.bit_count()+(fullh^h).bit_count()>6*(10-n):return
        bits=rem;opts=None
        while bits:
            q=bits&-bits;bits^=q;i=q.bit_length()-1
            a=[j for j in by[i] if em[j]&rem==em[j] and all(deg[x]<goal[x] for x in B[j])]
            if not a:return
            if opts is None or len(a)<len(opts):opts=a
            if len(opts)==1:break
        for j in opts:
            ds=deg.copy()
            for x in B[j]:ds[x]+=1
            if any(g-x>9-n for g,x in zip(goal,ds)):continue
            chosen.append(j);finish(rem^em[j],ds,h|hm[j]);chosen.pop()
    finish((1<<len(E))-1,d,0);return ans
if __name__=='__main__':
    a=list(layouts(4));n=0
    for w in a:
        c=solve(w);n+=c
        if c:print('layout',w,'solutions',c,flush=True)
    assert len(a)==13 and n==280, (len(a),n)
    print('PASS: all',len(a),'layouts,',n,'labelled links have a removable block.')
