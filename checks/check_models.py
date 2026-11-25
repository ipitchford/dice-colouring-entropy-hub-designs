#!/usr/bin/env python3
"""Finite exact-arithmetic tests for heterogeneous occupancy. Run with Python 3."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from math import log2, prod


_REQUIRE_COUNT = [0]


def require(condition, *info):
    """Explicit check that also runs under python -O (unlike assert)."""
    _REQUIRE_COUNT[0] += 1
    if not condition:
        raise SystemExit("CHECK FAILED: " + repr(info))


def weak_compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for head in range(total + 1):
        for tail in weak_compositions(total - head, length - 1):
            yield (head,) + tail


def square_tables(n, denominator):
    rows = tuple(weak_compositions(denominator, n))
    def fill(prefix, available):
        if len(prefix) == n - 1:
            yield prefix + (available,)
            return
        for row in rows:
            if all(x <= y for x, y in zip(row, available)):
                yield from fill(prefix + (row,), tuple(y-x for x, y in zip(row, available)))
    yield from fill((), (denominator,) * n)


def occupancy(rows):
    masks = {0: 1}
    for row in rows:
        nxt = Counter()
        for mask, mass in masks.items():
            for j, weight in enumerate(row):
                if weight:
                    nxt[mask | (1 << j)] += mass * weight
        masks = nxt
    counts = Counter()
    for mask, mass in masks.items():
        counts[mask.bit_count()] += mass
    return counts


def exact_variance(counts):
    mass = sum(counts.values())
    mean = F(sum(k*w for k, w in counts.items()), mass)
    return F(sum(k*k*w for k, w in counts.items()), mass) - mean**2


def product_variance(rows):
    # j is empty iff every row chooses outside j. Similarly for a pair.
    n = len(rows)
    q = sum(rows[0])
    denominator = q**n
    single = [prod(q-row[j] for row in rows) for j in range(n)]
    double = sum(prod(q-row[j]-row[k] for row in rows) for j,k in combinations(range(n),2))
    total = sum(single)
    return F(total+2*double, denominator) - F(total,denominator)**2


def dispersion(rows):
    q = sum(rows[0])
    return F(len(rows)*q*q - sum(w*w for row in rows for w in row),q*q)


def expected_private_switches(rows, delta_den=576):
    # A row chooses a passive endpoint, or an unordered pair of distinct
    # endpoints. An active pair cannot touch either endpoint of a private pair.
    n = len(rows)
    q = sum(rows[0])
    den = q*q*delta_den
    law = []
    for row in rows:
        states = [((j,), row[j]*((delta_den-1)*q+row[j])) for j in range(n)]
        states.extend(((j,k), 2*row[j]*row[k]) for j,k in combinations(range(n),2))
        law.append([(s,m) for s,m in states if m])
        require(sum(m for s,m in law[-1]) == den)
    answer = 0
    for i, states in enumerate(law):
        for edge, weight in states:
            if len(edge) != 2:
                continue
            a,b = edge
            miss_a, miss_b, miss_both = 1,1,1
            for k, other_states in enumerate(law):
                if k == i:
                    continue
                base = at_a = at_b = 0
                for other, mass in other_states:
                    if len(other) == 1 and other[0] == a:
                        at_a += mass
                    elif len(other) == 1 and other[0] == b:
                        at_b += mass
                    elif a not in other and b not in other:
                        base += mass
                miss_a *= base + at_b
                miss_b *= base + at_a
                miss_both *= base
            answer += weight*(miss_a + miss_b - 2*miss_both)
    return F(answer, den**n)


def check_tables():
    # Every labelled grid point, without quotienting by permutations.
    total = switches = 0
    for n, denominators in ((2, range(1,17)), (3,range(1,7)), (4,range(1,4)), (5,range(1,3))):
        best_min = best_max = None
        for q in denominators:
            num = 0
            for rows in square_tables(n,q):
                counts = occupancy(rows)
                require(sum(counts.values()) == q**n)
                v = exact_variance(counts)
                require(product_variance(rows) == v)
                s = dispersion(rows)
                require(2*sum(sum(F(x*y,q*q) for x,y in zip(row, other))
                             for row,other in combinations(rows,2)) == s)
                require(s/331776 <= v <= s/2)
                if s:
                    ratio = v/s
                    best_min = ratio if best_min is None else min(best_min,ratio)
                    best_max = ratio if best_max is None else max(best_max,ratio)
                if n<=3 or (n==4 and q<=2):
                    ek = expected_private_switches(rows)
                    # a=(1-exp(-1/2))/24 >= 1/72 and delta=1/576.
                    require(ek >= s/82944)
                    require(ek/4 <= v)
                    switches += 1
                num += 1
            total += num
            print(f'{n}x{n} denominator {q}: {num} labelled matrices')
        print(f'{n}x{n} min/max Var/S on these grids (S>0): {best_min}, {best_max}')
    for q in (100,10000,10**12):
        rows = ((q-1,1,0),(0,q-1,1),(1,0,q-1))
        counts = occupancy(rows)
        s,v=dispersion(rows),exact_variance(counts)
        require(counts == {2:3*q*(q-1),3:(q-1)**3+1})
        require(s/331776 <= expected_private_switches(rows)/4 <= v <= s/2)
        print(f'cyclic near-permutation q={q}: S={s}, Var/S={v/s}')
    print(f'Labelled rational matrices checked: {total}; exact switch expectations checked: {switches+3}.')


def rows_from_edges(edges,n):
    return tuple(tuple(int(j in e) for j in range(n)) for e in edges)


def cycle(n,r):
    return tuple(tuple((i+k)%n for k in range(r)) for i in range(n))


def blocks(n,r):
    return tuple(tuple(range(i//r*r,i//r*r+r)) for i in range(n))


def codegree_stats(edges,n,r):
    a = F(r-1,r)**r
    theta = 1-F(1,(r-1)**2)
    codes = [sum(i in e and j in e for e in edges) for i,j in combinations(range(n),2)]
    require(2*sum(codes) == n*r*(r-1))
    v = n*a*(1-a) + 2*a*a*sum(theta**c-1 for c in codes)
    upper = n*a*(1-a) + a*a*n*(r-1)*(theta**r-1)
    lower = n*a*(1-a) + a*a*n*r*(r-1)*(theta-1)
    require(lower <= v <= upper)
    require((v == upper) == all(c in (0,r) for c in codes))
    require((v == lower) == all(c in (0,1) for c in codes))
    return v, lower, upper


def check_hypergraphs():
    # Edge multisets include repeated edges and disconnected examples.
    for n,r in ((3,2),(4,2),(5,2),(4,3),(5,3),(5,4),(6,3)):
        opts = tuple(combinations(range(n),r))
        used = 0
        for edges in combinations_with_replacement(opts,n):
            if any(sum(i in e for e in edges)!=r for i in range(n)):
                continue
            rows = rows_from_edges(edges,n)
            v,lo,hi = codegree_stats(edges,n,r)
            require(exact_variance(occupancy(rows)) == v)
            used += 1
        print(f'{n} vertices, rank {r}: {used} labelled regular edge multisets checked')
    for n,r in ((6,2),(6,3),(8,4),(9,3),(12,3),(12,4),(12,6)):
        results = []
        for label,edges in (('circle',cycle(n,r)),('blocks',blocks(n,r))):
            rows = rows_from_edges(edges,n)
            counts = occupancy(rows)
            denom = r**n
            v,lo,hi = codegree_stats(edges,n,r)
            require(v == exact_variance(counts) == product_variance(rows))
            entropy = sum(-(w/denom)*log2(w/denom) for w in counts.values())
            print(f'{label}, n={n}, r={r}: Var/n={v/n}, Shannon bits={entropy:.10f}')
            results.append((v,counts))
        require(results[1][0]>results[0][0])
        if n==6 and r==3:
            # Same denominator, so exact entropy ordering follows by integer products.
            concentration = [prod(m**m for m in counts.values()) for _,counts in results]
            require(concentration[0] > concentration[1])
            print('Strict entropy order (6,3) repeated blocks > circle, certified by integer products.')


def check_martingale(rows):
    n, q = len(rows), sum(rows[0])
    support = [[(j,w) for j,w in enumerate(row) if w] for row in rows]
    # Enumerate complete allocations and every conditional quadratic variation.
    sum_q = sum_q2 = F(0)
    for outcome in product(*support):
        seen, bracket = set(), F(0)
        for i, (j, _) in enumerate(outcome):
            values = [F(prod(q-r[k] for r in rows[i+1:]),q**(n-i-1)) if k not in seen else F(0)
                      for k in range(n)]
            m = sum(F(w,q)*values[k] for k,w in support[i])
            v = sum(F(w,q)*values[k]**2 for k,w in support[i]) - m*m
            bracket += v
            seen.add(j)
        probability = F(prod(w for _,w in outcome),q**n)
        sum_q += probability*bracket
        sum_q2 += probability*bracket**2
    require(sum_q == exact_variance(occupancy(rows)))
    require(sum_q2-sum_q**2 <= 18*dispersion(rows))


def check_binomial_mixture(rows, delta_den=3):
    # Reconstruct the entire occupancy law via private switches, then compare
    # with a separate direct computation. Use delta=1/3 for this identity.
    from math import comb
    n, q = len(rows), sum(rows[0])
    den = delta_den*q*q
    laws = []
    for row in rows:
        law = [((j,), row[j]*((delta_den-1)*q+row[j])) for j in range(n)]
        law.extend(((j,k),2*row[j]*row[k]) for j,k in combinations(range(n),2))
        laws.append([(s,w) for s,w in law if w])
    mixed = Counter()
    for outcome in product(*laws):
        edges = [e for e,w in outcome if len(e)==2]
        passive = {e[0] for e,w in outcome if len(e)==1}
        frequency = Counter(k for e in edges for k in e)
        other = []
        k_private = 0
        for a,b in edges:
            if frequency[a]==frequency[b]==1 and ((a in passive) != (b in passive)):
                k_private += 1
            else:
                other.append((a,b))
        numerator = prod(w for e,w in outcome) * 2**(n-len(edges))
        for chosen in product(*other):
            offset = len(passive.union(chosen))
            for h in range(k_private+1):
                mixed[offset+h] += numerator*comb(k_private,h)
    require({k:F(w,(2*den)**n) for k,w in mixed.items()} == {
        k:F(w,q**n) for k,w in occupancy(rows).items()})


def check_representations():
    models = [
        ((1,0),(0,1)), ((1,1),(1,1)), ((7,1,0),(0,7,1),(1,0,7)),
        ((3,1,0),(1,1,2),(0,2,2)), ((1,1,1),(1,1,1),(1,1,1)),
        ((2,1,0,0),(1,1,1,0),(0,1,0,2),(0,0,2,1))
    ]
    for rows in models:
        check_martingale(rows)
        check_binomial_mixture(rows)
    print(f'Exact conditional binomial mixtures and martingale brackets: {len(models)} models.')


if __name__=='__main__':
    check_representations()
    check_tables()
    check_hypergraphs()
    print('PASS')
    print(f"explicit checks passed: {_REQUIRE_COUNT[0]}")
