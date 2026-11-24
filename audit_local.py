#!/usr/bin/env python3
"""Cross-check all normalized 15-links with a separate Python enumerator.
Run after verify.py has produced build/reps_*.txt. No numerical solver.
"""

if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")

from collections import defaultdict, Counter
from pathlib import Path
import sys
D=Path(__file__).resolve().parent
sys.path.insert(0,str(D/'regular_pair7'))
from classify_degree15 import partitions,layouts
from degree15_full_links import enumerate_links,group_perms
B=Path(sys.argv[1]) if len(sys.argv)>1 else D/'build'
by=defaultdict(list)
for file in sorted(B.glob('reps_*.txt')):
    if file.stem not in {'reps_high','reps_2222','reps_11222','reps_111122','reps_1111112','reps_11111111'}:continue
    lines=file.read_text().strip().splitlines();assert int(lines[0])==len(lines)-1
    for l in lines[1:]:
        v=list(map(int,l.split()));assert len(v)==23
        g=tuple(tuple(v[i:i+3]) for i in range(0,12,3))
        # C++ marks 12; Python marks 0 and shifts labels 0..11 by one.
        fixed=[(0,1+3*i,2+3*i,3+3*i) for i in range(4)]
        a=tuple(sorted(fixed+[tuple(i+1 for i in range(12) if b>>i&1) for b in v[12:]]))
        by[g].append(a)
assert sum(map(len,by.values()))==752
count=Counter();seen=set()
for p in partitions(8):
    for g in layouts(p):
        actual,_=enumerate_links(g)
        seen.add(g);count['layouts']+=1;count['links']+=len(actual)
        pending=set(actual)
        if pending:
            perms=list(group_perms(g))
            for a in by[g]:
                orbit={tuple(sorted(tuple(sorted(q[x] for x in b)) for b in a)) for q in perms}
                assert orbit<=pending,(g,a)
                pending-=orbit;count['reps']+=1
        assert not pending and (bool(actual)==bool(by[g])),g
    print('profile',p,'cumulative',dict(count),flush=True)
assert set(by)<=seen and count==Counter(layouts=143,links=63704,reps=752),count
print('PASS: Python enumerator and C++ representatives give exactly the same full labelled sets in every layout.',flush=True)
