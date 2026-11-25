"""Compare one quadrupled spoke with three doubled spokes by direct enumeration."""
from collections import Counter
from itertools import product
from math import fsum, log, prod


_REQUIRE_COUNT = [0]


def require(condition, *info):
    """Explicit check that also runs under python -O (unlike assert)."""
    _REQUIRE_COUNT[0] += 1
    if not condition:
        raise SystemExit("CHECK FAILED: " + repr(info))


def outcome_counts(n, extras):
    spokes = [(0, v) for v in range(1, n)]
    spokes += [(0, v) for v in extras]
    return Counter(len(set(oriented)) for oriented in product(*spokes))


def entropy(counts):
    total = sum(counts.values())
    return -fsum((k / total) * log(k / total) for k in counts.values())


for n in (8, 9, 10):
    spread = outcome_counts(n, (1, 2, 3))
    concentrated = outcome_counts(n, (1, 1, 1))
    require(sum(spread.values()) == sum(concentrated.values()) == 2 ** (n + 2))
    direct_order = prod(c**c for c in spread.values()) < prod(c**c for c in concentrated.values())
    require(direct_order == (n == 10))
    print(f"n={n}: three doubled minus one quadrupled, "
          f"{entropy(spread)-entropy(concentrated):+.12f} nats (sign certified exactly)")
print("PASS")
print(f"explicit checks passed: {_REQUIRE_COUNT[0]}")
