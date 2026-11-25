"""Verify the repeat-count polymer identity with exact rational arithmetic."""
from fractions import Fraction as F
from functools import cache
from itertools import combinations, product
from math import prod


_REQUIRE_COUNT = [0]


def require(condition, *info):
    """Explicit check that also runs under python -O (unlike assert)."""
    _REQUIRE_COUNT[0] += 1
    if not condition:
        raise SystemExit("CHECK FAILED: " + repr(info))


def enumerate_repeat_weights(p, z):
    n = len(p)
    return sum(
        z**(n - len(set(result))) * prod(p[i][j] for i, j in enumerate(result))
        for result in product(range(n), repeat=n)
    )


def polymer_partition(p, z):
    n = len(p)
    vertices = list(range(n))
    polymers = []
    for j in vertices:
        for k in range(2, n + 1):
            coeff = (z - 1)**k / z + (1 - 1/z) * (-1)**k
            for rows in combinations(vertices, k):
                weight = coeff * prod(p[i][j] for i in rows)
                if weight:
                    mask = (1 << (n + j)) + sum(1 << i for i in rows)
                    polymers.append((mask, weight))

    @cache
    def visit(available):
        if available == 0:
            return 1
        v = available & -available
        result = visit(available ^ v)
        for mask, w in polymers:
            if mask & v and mask & available == mask:
                result += w * visit(available ^ mask)
        return result

    return visit((1 << (2*n)) - 1)


def main():
    # Mixtures of cyclic shifts give exact doubly stochastic inputs.
    tests = ((1, 2), (1, 2, 3), (1, 0, 2, 4), (1, 0, 1, 0, 1), (9, 0, 0, 0, 0))
    for amounts in tests:
        n = len(amounts)
        p = [[F(amounts[(j-i) % n], sum(amounts)) for j in range(n)] for i in range(n)]
        for z in (F(1), F(-2), F(1, 2), F(3, 2)):
            actual = enumerate_repeat_weights(p, z)
            via_expansion = polymer_partition(p, z)
            require(actual == via_expansion, (amounts, z, actual, via_expansion))
    print("Exact repeat generating function equals polymer partition sum in all 20 checks.")
    print("Supports include zeros, a permutation, dense unequal rows and cyclic triples.")


if __name__ == "__main__":
    main()
    print(f"explicit checks passed: {_REQUIRE_COUNT[0]}")
