#!/usr/bin/env python3
"""Check the two-hub leaf-split law by independent explicit orientation counts."""
from collections import Counter
from itertools import product
from math import comb, fsum, log, prod


_REQUIRE_COUNT = [0]


def require(condition, *info):
    """Explicit check that also runs under python -O (unlike assert)."""
    _REQUIRE_COUNT[0] += 1
    if not condition:
        raise SystemExit("CHECK FAILED: " + repr(info))


def formula(a,b,L):
    n=a+b
    def choose(m,k):
        return comb(m,k) if 0<=k<=m else 0
    def shifted(k):
        return choose(b,k-a)+choose(a,k-b)
    return tuple((2**L)*choose(n,k) + shifted(k+1)-shifted(k) for k in range(-1,n+1))


def orientations(a,b,L):
    edges = [(0,1)]*L+[(0,j+2) for j in range(a)]+[(1,a+j+2) for j in range(b)]
    count=Counter(len(set(v))-2 for v in product(*edges))
    return tuple(count[k] for k in range(-1,a+b+1))


def entropy(count):
    mass=sum(count)
    return -fsum((x/mass)*log(x/mass) for x in count if x)


def entropy_strictly_greater(first,second):
    # For equal denominators, H is decreasing in the product of c^c.
    require(sum(first)==sum(second))
    return prod(x**x for x in first if x)<prod(x**x for x in second if x)


def main():
    tested=0
    for n in range(2,10):
        for L in range(1,6):
            star=formula(0,n,L)
            base=(0,)+tuple(2**L*comb(n,k) for k in range(n+1))
            for a in range(n+1):
                counts=formula(a,n-a,L)
                require(orientations(a,n-a,L)==counts)
                if a and a<n:
                    require(entropy(counts) <= entropy(base)+1e-12)
                    if L>=2:
                        require(entropy(star)>entropy(counts))
                tested+=1
            if n<=5 and L==2:
                require(entropy_strictly_greater(star,base))
    print(f'Explicit orientation laws tested: {tested}; q=2..9, L=1..5, all leaf splits.')
    numerical=0
    for n in (2,3,4,5,6,7,8,16,20,32,100):
        for L in (2,3,5,8,12,15):
            star=formula(0,n,L)
            base=(0,)+tuple(2**L*comb(n,k) for k in range(n+1))
            require(entropy(star)>entropy(base))
            for a in range(1,n):
                require(entropy(formula(a,n-a,L))<=entropy(base)+1e-12)
                numerical+=1
    print(f'Additional numerical nontrivial-split comparisons: {numerical}.')
    print('PASS')


if __name__=='__main__':
    main()
    print(f"explicit checks passed: {_REQUIRE_COUNT[0]}")
