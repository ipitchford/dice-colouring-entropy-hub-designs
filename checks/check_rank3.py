#!/usr/bin/env python3
"""Enumerate labelled cubic triple multisets by completing each vertex in turn."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement


_REQUIRE_COUNT = [0]


def require(condition, *info):
    """Explicit check that also runs under python -O (unlike assert)."""
    _REQUIRE_COUNT[0] += 1
    if not condition:
        raise SystemExit("CHECK FAILED: " + repr(info))


def regular_triples(n):
    def complete(v,degree,edges):
        if v==n:
            yield edges
            return
        pairs = [(a,b) for a,b in combinations(range(v+1,n),2)
                 if degree[a] < 3 and degree[b] < 3]
        for tail in combinations_with_replacement(pairs,3-degree[v]):
            updated=degree.copy()
            updated[v]=3
            for a,b in tail:
                updated[a]+=1
                updated[b]+=1
            if max(updated)>3:
                continue
            yield from complete(v+1,updated,edges+tuple((v,a,b) for a,b in tail))
    yield from complete(0,[0]*n,())


def check(n):
    pairs=tuple(combinations(range(n),2))
    min_defect=None
    n_min=0
    total=0
    for edges in regular_triples(n):
        codeg=Counter(ab for edge in edges for ab in combinations(edge,2))
        blocks=sum(cnt==3 for cnt in Counter(edges).values())
        b=n-3*blocks
        twins=sum(codeg[p]==3 for p in pairs)-3*blocks
        d=2*sum((0,11,10,0)[codeg[p]] for p in pairs)
        require(twins<=b//3)
        require(d>=30*b-18*twins)
        if min_defect is None or d<min_defect:
            min_defect=d
            n_min=1
        elif d==min_defect:
            n_min+=1
        total+=1
    expected=(0,120,192)[n%3]
    require(min_defect==expected)
    # Ordered-pair difference from the block variance is D/2187 exactly.
    vmax=F(26*n,243)-F(expected,2187)
    print(f'n={n}: {total} labelled cubic triple multisets, minimum scaled defect {min_defect}, {n_min} labelled maximisers, max variance {vmax}')


if __name__=='__main__':
    for n in range(3,9):
        check(n)
    print('PASS')
    print(f"explicit checks passed: {_REQUIRE_COUNT[0]}")
