"""Finite audits of fair-coin maximisers. Standard library, Python 3.11+.

Small graphs use exact integer entropy comparisons. Large stars use exact
integer outcome counts and outward-rounded intervals for the logarithms.
Run from any directory: python3 check_coins.py
"""
from collections import Counter
from decimal import Context, Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations
from math import comb, prod


_REQUIRE_COUNT = [0]


def require(condition, *info):
    """Explicit check that also runs under python -O (unlike assert)."""
    _REQUIRE_COUNT[0] += 1
    if not condition:
        raise SystemExit("CHECK FAILED: " + repr(info))


def occupancy_counts(n, edges):
    states = {0: 1}
    for u, v in edges:
        updated = {}
        for mask, weight in states.items():
            for vertex in (u, v):
                after = mask | (1 << vertex)
                updated[after] = updated.get(after, 0) + weight
        states = updated
    counts = [0] * (n + 1)
    for mask, weight in states.items():
        counts[mask.bit_count()] += weight
    require(sum(counts) == 1 << len(edges))
    return counts


def canonical(n, edges):
    return min(tuple(sorted((min(p[u], p[v]), max(p[u], p[v])) for u, v in edges))
               for p in permutations(range(n)))


def predicted(t):
    return (1,) * t if t <= 3 else (t,)


def candidate_edges(n, extras):
    return tuple((0, i + 1) for i in range(n-1)
                 for _ in range(1 + (extras[i] if i < len(extras) else 0)))


def describe_star(n, edges):
    for hub in range(n):
        if all(hub in e for e in edges):
            multiplicities = Counter(v if u == hub else u for u, v in edges)
            if len(multiplicities) == n - 1:
                return tuple(sorted((d-1 for d in multiplicities.values() if d > 1), reverse=True))
    return None


def enumerate_small():
    print("All labelled multigraphs. Winners are grouped up to vertex permutation.")
    print("n m labelled number_of_labelled_winners winner_orbits (star extra partitions) matches_eventual_prediction")
    for n in range(3, 6):
        simple_pairs = tuple(combinations(range(n), 2))
        for m in range(n, n + 3):
            total = 0
            winners = []
            best_score = None
            for edges in combinations_with_replacement(simple_pairs, m):
                total += 1
                counts = occupancy_counts(n, edges)
                score = prod(c ** c for c in counts if c)
                if best_score is None or score < best_score:
                    winners = [edges]
                    best_score = score
                elif score == best_score:
                    winners.append(edges)
            require(total == comb(len(simple_pairs) + m - 1, m))
            reps = sorted({canonical(n, g) for g in winners})
            extras = [describe_star(n, g) for g in reps]
            expected = predicted(m - n + 1)
            if len(expected) > n - 1:
                prediction = "unavailable at this n"
            else:
                goal = canonical(n, candidate_edges(n, expected))
                prediction = "yes" if reps == [goal] else "no"
            info = [extra if extra is not None else ("nonstar", graph)
                    for extra, graph in zip(extras, reps)]
            print(n, m, total, len(winners), len(reps), info, prediction)


def partitions(t, largest=None):
    if t == 0:
        yield ()
        return
    maximum = t if largest is None else min(t, largest)
    for a in range(maximum, 0, -1):
        for rest in partitions(t-a, a):
            yield (a,) + rest


def star_counts(n, extras):
    m = n - 1 + sum(extras)
    singleton_arms = n - 1 - len(extras)
    counts = [comb(singleton_arms, j) for j in range(singleton_arms+1)]
    for j in extras:
        weight = (1 << (j+1)) - 1
        updated = [0] * (len(counts)+1)
        for k, number in enumerate(counts):
            updated[k] += number
            updated[k+1] += number * weight
        counts = updated
    counts = [0] + counts
    counts[n] -= 1  # Every coin pointing away from the hub.
    counts[n-1] += 1
    require(len(counts) == n+1 and min(counts) >= 0 and sum(counts) == 1 << m)
    return counts


nearest = Context(prec=46, rounding=ROUND_HALF_EVEN)
lower = Context(prec=46, rounding=ROUND_FLOOR)
upper = Context(prec=46, rounding=ROUND_CEILING)


@lru_cache(maxsize=None)
def log_bounds(number):
    y = nearest.ln(Decimal(number))  # ln is correctly rounded to nearest.
    return nearest.next_minus(y), nearest.next_plus(y)


def entropy_interval(counts, m):
    # Bound H by m log(2) minus 2^-m times sum_c c log(c).
    lo = Decimal(0)
    hi = Decimal(0)
    for number in counts:
        if number <= 1:
            continue
        lb, ub = log_bounds(number)
        lo = lower.add(lo, lower.multiply(Decimal(number), lb))
        hi = upper.add(hi, upper.multiply(Decimal(number), ub))
    lb2, ub2 = log_bounds(2)
    den = Decimal(1 << m)
    hlo = lower.subtract(lower.multiply(Decimal(m), lb2), upper.divide(hi, den))
    hhi = upper.subtract(upper.multiply(Decimal(m), ub2), lower.divide(lo, den))
    return hlo, hhi


def check_stars():
    print("Exact star outcome polynomials and certified entropy rankings among all partitions.")
    print("n t winning_extra_partition matches_eventual_prediction gap_to_next_nats_lower_bound")
    for n in (5, 6, 8, 10, 20, 40, 100, 500):
        for t in range(1, 7):
            m = n-1+t
            by_partition = []
            for parts in partitions(t):
                if len(parts) > n-1:
                    continue
                c = star_counts(n, parts)
                if n <= 6:
                    require(c == occupancy_counts(n, candidate_edges(n, parts)))
                bounds = entropy_interval(c, m)
                by_partition.append((bounds, parts))
            by_partition.sort(reverse=True)
            (lb, ub), parts = by_partition[0]
            if len(by_partition) > 1:
                gap = lower.subtract(lb, max(x[0][1] for x in by_partition[1:]))
                require(gap > 0, (n, t, parts, gap))
                # Printed numeric value is a conservative rounded lower bound.
                rounded_gap = Context(prec=3, rounding=ROUND_FLOOR).plus(gap)
                gap_text = str(rounded_gap)
            else:
                gap_text = "only candidate"
            print(n, t, parts, parts == predicted(t), gap_text)


if __name__ == "__main__":
    enumerate_small()
    check_stars()
    print(f"explicit checks passed: {_REQUIRE_COUNT[0]}")
