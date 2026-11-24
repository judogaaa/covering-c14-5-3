#!/usr/bin/env python3
"""Reproduce the complete computer-assisted exclusion of 42 blocks.
Only Python's standard library and a C++17 compiler are needed. No LP solver.
Run with Python assertions enabled. Interruptions/errors are NOT successful checks.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter,defaultdict
import subprocess,sys,json,os,time
D=Path(__file__).resolve().parent;C=D/'core';B=D/'build';B.mkdir(exist_ok=True)
if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")
sys.path.insert(0,str(C))
from verify_degree14 import layouts
V=range(14);Q=range(12);P=list(combinations(Q,2));T=list(combinations(Q,3));R=[(v,) for v in Q]+P+T; RS=list(map(set,R)); BS=list(map(set,combinations(Q,5)))

def py(p,*args,cwd=None):
    subprocess.run([sys.executable,str(p),*args],cwd=cwd or p.parent,check=True)
def compile_all():
    for p in sorted(C.glob('*.cpp')):
        subprocess.run([os.environ.get('CXX','g++'),'-O3','-std=c++17',str(p),'-o',str(B/p.stem)],check=True)
def run(name,inp=None,args=(),out=None):
    dest=B/(out or name+'.log')
    print('RUN',name,*args,flush=True)
    with dest.open('w') as f:
        if inp is None:subprocess.run([str(B/name),*map(str,args)],stdout=f,check=True,cwd=B)
        else:
            with Path(inp).open() as fin:subprocess.run([str(B/name),*map(str,args)],stdin=fin,stdout=f,check=True,cwd=B)
    a=dest.read_text().splitlines();assert a
    print(a[-1],flush=True);return a,dest

def extract_reps(a,p):
    rr=[l[4:] for l in a if l.startswith('REP ')]
    p.write_text(str(len(rr))+'\n'+'\n'.join(rr)+'\n');return rr

def is_removable(link):
    P=[list(combinations([v for v in V if b>>v&1],2)) for b in link];c=Counter(p for pp in P for p in pp)
    return any(all(c[p]>=2 for p in pp) for pp in P)

def check_local(r):
    w,*_=r;w=r[:12];a=r[12:];assert len(a)==11
    L=[(1<<12)|(7<<(3*i)) for i in range(4)]+a
    assert len(L)==len(set(L))==15 and all(b.bit_count()==4 for b in L)
    d=Counter(v for b in L for v in range(13) if b>>v&1);p=Counter(t for b in L for t in combinations([v for v in range(13) if b>>v&1],2));assert set(p)==set(combinations(range(13),2));assert [d[v] for v in range(13)]==[4+x for x in w]+[4]
    assert max(w)<=3
    if max(w)<=2:
        for t,n in p.items():
            if n>=5:assert n==5 and sorted(x for x in w if x)==[1,1,1,1,2,2] and all(d[v]==6 for v in t)
    return is_removable(L)

def incidence_rows(F,partner=None,high=None):
    # Columns: all 792 residual 5-sets on the nonroot points. Rows: integer inequalities.
    regular=partner is not None
    if regular:
        Z=[z for z in V if z not in (13,partner)];F=[sum(1<<i for i,v in enumerate(Z) if b>>v&1) for b in F]
    f=[sum((b&m)==m for b in F) for m in [sum(1<<v for v in s) for s in R]]
    lo=[max(0,a-b) for a,b in zip([15]*12+[4]*66+[1]*220,f)]
    missing=[t for t,z in zip(T,lo[78:]) if z];hp=Counter(p for t in missing for p in combinations(t,2));hv=Counter(v for t in missing for v in t)
    lo[12:78]=[max(z,(hp[p]+2)//3) for p,z in zip(P,lo[12:78])]
    incid=Counter()
    for p,z in zip(P,lo[12:78]):
        for v in p:incid[v]+=z
    lo[:12]=[max(z,(hv[v]+5)//6,(incid[v]+3)//4) for v,z in enumerate(lo[:12])]
    if high is not None:assert not regular and len(high)==2;lo[:12]=[max(z,15+(v in high)-f[v]) for v,z in enumerate(lo[:12])]
    rows=[(s,1,b) for s,b in zip(RS,lo)]
    rows.extend((RS[i],-1,f[i]-(15 if regular else (15+(i in high) if high is not None else 17))) for i in Q)
    if regular:rows.extend((RS[i],-1,f[i]-(6 if i<78 else 4)) for i in range(12,len(R)))
    return rows

def certificate(c,rows):
    w=c['weights'];assert w and len({i for i,v in w})==len(w) and all(type(i)==type(v)==int and 0<=i<len(rows) and v>0 for i,v in w)
    terms=[(rows[i][0],rows[i][1]*v,rows[i][2]*v) for i,v in w]
    rhs=sum(r for s,a,r in terms);worst=max(sum(a for s,a,r in terms if s<=b) for b in BS)
    assert rhs==c['rhs'] and worst==c['worst'] and rhs>18*worst
    return rhs-18*worst

def check_union(F,y,regular):
    assert len(F)==len(set(F)) and all(0<b<1<<14 and b.bit_count()==5 for b in F)
    d=Counter(v for b in F for v in V if b>>v&1);t=Counter(t for b in F for t in combinations([v for v in V if b>>v&1],3))
    assert 0<=y<13 and all(b & ((1<<13)|(1<<y)) for b in F)
    assert d[13]==15 and d[y]==(15 if regular else 13)
    codeg=sum(bool(b&(1<<13)) and bool(b&(1<<y)) for b in F)
    assert len(F)==d[13]+d[y]-codeg
    assert codeg in ((5,6) if regular else (4,))
    assert all(t[a]>=1 for a in combinations(V,3) if 13 in a or y in a)
    if not regular:assert all(t[a]==1 for a in combinations(V,3) if y in a)

def verify_rep_results(a,expected):
    n,c,s=expected
    reps=[l.split() for l in a if l.startswith('REPRESULT ')]
    assert [int(r[1]) for r in reps]==list(range(n))
    assert all(r[-2:]==['timed','0'] for r in reps)
    assert sum(int(r[r.index('completions')+1]) for r in reps)==c
    assert sum(int(r[r.index('survivors')+1]) for r in reps)==s
    reported=Counter()
    for l in a:
        if l.startswith('SURV '):
            i,y=map(int,l.split()[1:3]);reported[i,y]+=1
    expected_counts=Counter({(int(r[1]),int(r[r.index('partner')+1])):int(r[r.index('survivors')+1]) for r in reps})
    assert reported==expected_counts

def check_stage(a,expected):
    verify_rep_results(a,expected)
    # TOTAL n ... survivors s timed 0
    s=a[-1].split();assert s[0]=='TOTAL' and int(s[1])==expected[0] and s[-2:]==['timed','0'];assert int(s[s.index('completions')+1])==expected[1] and int(s[s.index('survivors')+1])==expected[2],s
    cases=[tuple(map(int,l.split()[1:])) for l in a if l.startswith('SURV ')];assert len(cases)==expected[2]
    for i,y,*F in cases:check_union(F,y,True)
    return cases

def main(mode):
    if mode in ('all','prior'):
        print('I. Removable-block lemma and previous two-low exclusions',flush=True)
        py(C/'verify_degree14.py')
        for s in ('verify_new.py','verify_local.py','direct_local.py','compat_all.py'):py(D/'two_low'/s)
        for n in ('1','3'):py(D/'two_low'/'verify_all_subsets.py',n,'--fresh')
        py(D/'regular_pair7'/'verify.py');py(D/'regular_triple5'/'rare_triple.py')
        if mode=='prior':return
    compile_all()
    print('II. Complete normalized degree-15 link enumeration',flush=True)
    py(C/'one_low_input.py',cwd=B)
    raw=(B/'one_low_input.txt').read_text().splitlines();nt,nl=map(int,raw[0].split());assert (nt,nl)==(72,143)
    assert {tuple(map(int,l.split())) for l in raw[nt+1:]}==set(layouts(8))
    part={name:[] for name in ('high','2222','11222','111122','1111112','11111111')}
    def profile(w):return 'high' if max(w)>=3 else ''.join(map(str,sorted(x for x in w if x)))
    for l in raw[nt+1:]:part[profile(list(map(int,l.split())))].append(l)
    expected={'high':(98,208,10),'2222':(4,0,0),'11222':(12,840,29),'111122':(16,5228,161),'1111112':(9,13100,333),'11111111':(4,44328,219)}
    reps={};removable={};local_cache={}
    for k,L in part.items():
        assert len(L)==expected[k][0];p=B/f'input_{k}.txt';p.write_text('\n'.join([f'{nt} {len(L)}',*raw[1:nt+1],*L])+'\n')
        a,_=run('enum_reps',p,out=f'enum_{k}.log');s=a[-1].split();assert s[:2]==['FINAL','EXHAUSTED'] and int(s[s.index('local')+1])==expected[k][1] and int(s[s.index('reps')+1])==expected[k][2]
        reps[k]=B/f'reps_{k}.txt';rr=extract_reps(a,reps[k]);assert len(rr)==expected[k][2]
        removable[k]=sum(check_local(list(map(int,r.split()))) for r in rr)
    assert removable=={'high':0,'2222':0,'11222':29,'111122':117,'1111112':143,'11111111':53},removable
    print('PASS: 63,704 normalized-layout labelled links, 752 representatives; 342 removable.',flush=True)
    if mode in ('all','core','low'):
        print('III. Exclude one exact low-degree point',flush=True)
        a,_=run('one_low_all',B/'one_low_input.txt');s=a[-1].split();assert s[:2]==['FINAL','EXHAUSTED'] and int(s[s.index('reps')+1])==752 and int(s[s.index('tests')+1])==54144 and int(s[s.index('survivors')+1])==26432
        count=Counter();kept=defaultdict(list);known={}
        for l in a:
            if not l.startswith('survivor '):continue
            h,rest=l.split(' local ');local,td=rest.split(' td ');w=list(map(int,h.split(' weights ')[1].split()));k=''.join(map(str,sorted(x for x in w if x)));count[k]+=1
            F=[(1<<12)|(1<<13)|(7<<(3*i)) for i in range(4)]+[(1<<13)|int(x) for x in local.split()]+[(1<<12)|int(x) for x in td.split()];check_union(F,12,False)
            L=tuple(sorted(b^(1<<13) for b in F if b>>13&1))
            if L not in known:known[L]=is_removable(L)
            if not known[L]:kept[k].append(F)
        assert count==Counter({'11111111':9657,'1111112':12151,'111122':4298,'111113':221,'11123':10,'11222':95}),count
        assert {k:len(v) for k,v in kept.items()}=={'11111111':7426,'1111112':7168,'111122':1516,'111113':221,'11123':10}
        p=B/'all_low_nonrem.log';ix=0
        with p.open('w') as f:
            for k in sorted(kept):
                for F in kept[k]:print('SURV',ix,12,*F,file=f);ix+=1
        a,_=run('signature_all',p,args=[reps[k] for k in ('high','111122','1111112','11111111')]);line=[l for l in a if l.startswith('TOTAL ')];assert len(line)==1 and line[0]=='TOTAL 16341 excluded 16333 remaining 8 signatures 352008',line
        certs=json.loads((D/'data'/'last_eight_cert.json').read_text());lookup={(tuple(sorted(c['F'])),tuple(sorted(c['high']))):c for c in certs};seen=set()
        for l in a:
            if not l.startswith('OPEN '):continue
            pre,post=l.split(' SURV ');hi=tuple(sorted(map(int,pre.split()[4:])));i,y,*F=map(int,post.split());assert len(hi)==2 and y==12;key=(tuple(sorted(F)),hi);c=lookup[key];certificate(c,incidence_rows(F,high=hi));seen.add(key)
        assert seen==set(lookup) and len(seen)==8
        print('PASS: all one-low cases excluded; 8 exact integer certificates.',flush=True)
        if mode=='low':return
    print('IV. Exclude regular case with codegree six',flush=True)
    a,_=run('regular_double3',reps['11222'],out='reg3.log');check_stage(a,(29,2792,0))
    a,_=run('regular_double3',reps['111122'],out='reg2.log');cases=check_stage(a,(161,15792,57));certs=json.loads((D/'data'/'regular_111122_dual.json').read_text());lookup={(c['partner'],tuple(sorted(c['F']))):c for c in certs};seen=set()
    for i,y,*F in cases:
        k=(y,tuple(sorted(F)));c=lookup[k];certificate(c,incidence_rows(F,partner=y));seen.add(k)
    assert seen==set(lookup) and len(cases)==len(certs)==57
    print('PASS: regular profile with two doubles; 57 integer certificates.',flush=True)
    a,p=run('regular_matching',reps['1111112']);check_stage(a,(333,29708,2335))
    a,_=run('propagate',p,args=['matching'],out='propagate_matching.log');assert a[-1].startswith('TOTAL 2335 excluded 1863 unresolved 472 ')
    op=B/'matching_open.log';op.write_text(''.join('SURV '+l.split(' SURV ',1)[1]+'\n' for l in a if l.startswith('OPEN ')))
    assert len(op.read_text().splitlines())==472
    a,_=run('propagate_search',op,args=['matching']);assert a[-1].startswith('TOTAL 472 excluded 472 unresolved 0 ') and a[-1].endswith('timed 0') and not any(l.startswith('COVER ') for l in a)
    print('PASS: no codegree six in a regular covering.',flush=True)
    print('V. Exclude regular case with all codegrees 4 or 5',flush=True)
    a,p=run('regular_simple',reps['11111111']);check_stage(a,(219,2544816,6306))
    a,_=run('propagate_simple',p);assert a[-1].startswith('TOTAL 6306 excluded 6289 unresolved 17 ')
    op=B/'simple_open.log';op.write_text(''.join('SURV '+l.split(' SURV ',1)[1]+'\n' for l in a if l.startswith('OPEN ')))
    assert len(op.read_text().splitlines())==17
    a,_=run('search_simple',op);assert a[-1].startswith('TOTAL 17 excluded 17 unresolved 0 ') and a[-1].endswith('timed 0') and not any(l.startswith('COVER ') for l in a)
    print('PASS: all regular cases excluded.',flush=True)
    if mode=='all':print('THEOREM (see PROOF.md): C(14,5,3)=43. All verification stages completed.',flush=True)
    else:print('Core verification passed. Run without flags to include all prior stages.',flush=True)
if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'all';assert mode in ('all','prior','core','low','regular');main(mode)
