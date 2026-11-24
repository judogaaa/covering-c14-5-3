"""Exhaustively test compatibility of three regular links with a triple of multiplicity 5.
Discovery/verification recursion using exact integer masks, no solver.
"""

if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

from collections import Counter
from itertools import combinations
from classify_degree15 import layouts
from degree15_full_links import enumerate_links,group_perms
V=tuple(range(14)); P=tuple(combinations(V,2)); T=tuple(combinations(V,3))
def norm(F):return tuple(sorted(tuple(sorted(b)) for b in F))
def triples(F):return Counter(t for b in F for t in combinations(b,3))

def initial():
    for g in layouts((1,1,1,1,2,2)):
        A,_=enumerate_links(g); ps=list(group_perms(g)); pending=set()
        for a in A:
            c=Counter(p for b in a for p in combinations(b,2))
            for p,n in c.items():
                if n==5:pending.add((a,p))
        while pending:
            a,p=min(pending);orb={(norm(tuple(q[z] for z in b) for b in a),tuple(sorted(q[z] for z in p))) for q in ps}
            assert orb<=pending;pending-=orb
            yield norm((*b,13) for b in a),p

def extend(F,parent,prev,force2):
    Q=tuple(z for z in V if z!=parent and z not in prev)
    fixed=tuple(tuple(z for z in b if z!=parent) for b in F if parent in b)
    N=15-len(fixed); fc=Counter(p for b in fixed for p in combinations(b,2));fd=Counter(z for b in fixed for z in b)
    assert all(fc[p]>=1 for p in combinations(tuple(z for z in V if z!=parent),2) if set(p)&set(prev))
    # All three roots must have profile (4,2): their two codegree-6 partners are the other roots.
    if any(fd[z]>6 for z in force2):return
    forced1={z for z in Q if z not in force2 and (fd[z]>4 or any(z in p and v>1 for p,v in fc.items()))}
    if len(forced1)>4:return
    # non-root positive points have degree exactly 5
    if any(fd[z]>5 for z in Q if z not in force2):return
    f2=set(force2);forced1-=f2
    for extra in combinations([z for z in Q if z not in f2|forced1],4-len(forced1)):
        H=tuple(sorted(f2|forced1|set(extra)));hs=set(H); hi={z:i for i,z in enumerate(H)}
        allpos=hs|set(prev)
        if any(v>1 and not set(p)<=allpos for p,v in fc.items()):continue
        goal=tuple((6 if z in f2 else 5)-fd[z] for z in H)
        if min(goal,default=0)<0:continue
        E=[p for p in combinations(Q,2) if not fc[p] and not set(p)<=hs];ei={p:i for i,p in enumerate(E)}
        hp=[p for p in combinations(H,2) if not fc[p]];pi={p:i for i,p in enumerate(hp)}
        C=[];m=[];h=[];bh=[];by=[[] for _ in E]
        for b in combinations(Q,4):
            pairs=list(combinations(b,2))
            if any(fc[p] and not set(p)<=hs for p in pairs):continue
            j=len(C);C.append(b);m.append(sum(1<<ei[p] for p in pairs if p in ei));h.append(sum(1<<pi[p] for p in pairs if p in pi));bh.append(tuple(hi[z] for z in b if z in hs))
            for p in pairs:
                if p in ei:by[ei[p]].append(j)
        empty=[j for j in range(len(C)) if not m[j]]; full=(1<<len(E))-1;fullh=(1<<len(hp))-1
        def dfs(rem,d,cov,chosen):
            n=len(chosen)
            if not rem:
                k=N-n
                if k<0 or k>len(empty) or sum(t-v for t,v in zip(goal,d))!=4*k:return
                for js in combinations(empty,k):
                    ds=list(d);cv=cov
                    for j in js:
                        for z in bh[j]:ds[z]+=1
                        cv|=h[j]
                    if tuple(ds)==goal and cv==fullh:yield chosen+js
                return
            if n>=N or rem.bit_count()>6*(N-n):return
            best=None;bits=rem
            while bits:
                bit=bits&-bits;i=bit.bit_length()-1;bits^=bit
                opts=[j for j in by[i] if m[j]&rem==m[j] and all(d[z]<goal[z] for z in bh[j])]
                if not opts:return
                if best is None or len(opts)<len(best):best=opts
                if len(best)==1:break
            for j in best:
                ds=list(d)
                for z in bh[j]:ds[z]+=1
                if any(t-v>N-n-1 for t,v in zip(goal,ds)):continue
                yield from dfs(rem^m[j],tuple(ds),cov|h[j],chosen+(j,))
        for sol in dfs(full,(0,)*len(H),0,()):
            link=fixed+tuple(C[j] for j in sol); assert len(link)==len(set(link))==15
            assert set(p for b in link for p in combinations(b,2))==set(combinations(tuple(z for z in V if z!=parent),2))
            deg=Counter(z for b in link for z in b);assert sorted(deg.values())==[4]*7+[5]*4+[6]*2
            yield norm((*F,*(tuple(sorted((*C[j],parent))) for j in sol)))

def feasible(F):
    d=Counter(z for b in F for z in b);p=Counter(q for b in F for q in combinations(b,2));t=triples(F)
    if any(v>6 for v in p.values()) or any(v>5 for v in t.values()):return False
    h=Counter(q for a in T if not t[a] for q in combinations(a,2));need={q:max(0,4-p[q],(h[q]+2)//3) for q in P}
    if any(p[q]+need[q]>6 for q in P):return False
    return all(d[z]+(sum(need[q] for q in P if z in q)+3)//4<=15 for z in V)

def main():
    n=two=excluded=0
    for F,(y,z) in initial():
        n+=1; count=0
        for FF in extend(F,y,{13},{z}):
            count+=1;two+=1
            assert len(FF)==24  # 15+15-6
            p=Counter(q for b in FF for q in combinations(b,2));t=triples(FF)
            h=Counter(q for a in T if not t[a] for q in combinations(a,2))
            bad=[q for q in P if p[q]==6 and h[q]>=4]
            assert len(bad)>=2
            assert not feasible(FF)
            excluded+=1
            print('case',n,count,'contradictory pairs',[(q,p[q],h[q]) for q in bad])
        assert count==8
    assert (n,two,excluded)==(2,16,16)
    print('PASS: all 16 two-link unions are impossible; triple multiplicity >=5 excluded in the regular case.')
if __name__=='__main__':main()
