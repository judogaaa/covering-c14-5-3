#!/usr/bin/env python3
"""Run the original full proof and additional independent consistency checks.
--generated-only is for auditing freshly generated build logs in the same run;
it is not a substitute for running verify.py from a clean archive.
"""
from pathlib import Path
from collections import Counter
import subprocess,sys,json
import verify as v
D=Path(__file__).resolve().parent; B=D/'build'
if not __debug__:
    raise SystemExit("Verification requires Python assertions; do not use -O or PYTHONOPTIMIZE.")
def check_generated():
    expected={'reg3.log':(29,2792,0),'reg2.log':(161,15792,57),'regular_matching.log':(333,29708,2335),'regular_simple.log':(219,2544816,6306)}
    for name,e in expected.items():
        a=(B/name).read_text().splitlines();cases=v.check_stage(a,e)
        if name.startswith('regular_'):
            mode='matching' if name=='regular_matching.log' else 'simple'
            assert len(cases)==e[2]
            with (B/name).open() as fin:
                s=subprocess.run([str(B/'independent_residual'),mode],stdin=fin,stdout=subprocess.PIPE,text=True,check=True)
            assert s.stdout.startswith(f'PASS {mode} cases {e[2]} nodes '),s.stdout
            print(s.stdout.strip(),flush=True)
    # The 1-based witness must agree exactly with the bitmask witness.
    masks=list(map(int,(D/'two_low/upper43_masks.txt').read_text().split()))
    blocks=[tuple(map(int,l.split())) for l in (D/'upper43_blocks.txt').read_text().splitlines() if l.strip() and not l.startswith('#')]
    assert len(blocks)==43 and all(len(b)==5 and len(set(b))==5 and all(1<=x<=14 for x in b) for b in blocks)
    assert {sum(1<<(x-1) for x in b) for b in blocks}==set(masks)
    from itertools import combinations
    assert {t for b in blocks for t in combinations(sorted(b),3)}==set(combinations(range(1,15),3))
    print('PASS: 1-based and mask witnesses agree; 364 triples.',flush=True)
    print('PASS: all per-representative logs and independent residual checks.',flush=True)
if __name__=='__main__':
    if '--generated-only' not in sys.argv:
        subprocess.run([sys.executable,'-u',str(D/'verify.py')],cwd=D,check=True)
    check_generated()
    if '--local' in sys.argv:
        subprocess.run([sys.executable,'-u',str(D/'audit_local.py')],cwd=D,check=True)
    if '--generated-only' in sys.argv:
        print('AUDIT PASS: generated-data checks completed (not a fresh full proof run).',flush=True)
    else:
        print('AUDIT PASS: full proof verification and additional checks completed.',flush=True)
