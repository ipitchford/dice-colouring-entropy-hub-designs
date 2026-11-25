#!/usr/bin/env python3
"""Hub designs against balanced designs (Section 7). Standard library only; runs under python -O.

Part 1 (exact rationals): for every rank 2 <= r <= 199 there is a block size 1 <= s <= r-1 with
        V(s,r) >= 1.5 Vmax(r), where V(s,r) is the per-leaf variance of a hub design (Proposition 7.1)
        and Vmax(r) is the largest per-vertex variance of a regular design (Proposition 6.1).
Part 2 (directed decimal bounds): the numerical constants used in the proof of Lemma 7.2 for r >= 200.
Part 3 (finite certificates): for 2 <= r <= 8 and every n in [N_r, NMAX], an explicit hub design with
        n vertices and n edges has entropy strictly larger than the upper bound
        (1/2) log(2 pi e (n Vmax(r) + 1/12)) valid for every balanced (= regular) design.
        Entropies are evaluated from exact rational laws with 60-digit decimal logarithms; the
        smallest certified margin is printed and must exceed 1e-6 nats.
"""
from decimal import Decimal, getcontext
from fractions import Fraction as F
from math import comb

_REQUIRE_COUNT = [0]


def require(condition, *info):
    """Explicit check that also runs under python -O."""
    _REQUIRE_COUNT[0] += 1
    if not condition:
        raise SystemExit("CHECK FAILED: " + repr(info))


getcontext().prec = 60
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494")
E1 = Decimal(1).exp()


def tau(r):
    return F(r - 2, r) / F(r - 1, r) ** 2


def V(s, r):
    """Per-leaf variance of s leaves sharing s copies of one edge (Proposition 7.1)."""
    q = F(r - 1, r) ** s
    return q * (1 - q) + (s - 1) * q * q * (tau(r) ** s - 1)


def vmax(r):
    q = F(r - 1, r) ** r
    return q * (1 - q) - q * q * (r - 1) * (1 - tau(r) ** r)


def part1():
    print("Part 1: best hub block size against the regular-design maximum, exact rationals, 2 <= r <= 199")
    worst = None
    for r in range(2, 200):
        candidates = range(1, r) if r <= 40 else range(int(0.3 * r), int(0.55 * r) + 2)
        best_s = max(candidates, key=lambda s: V(s, r))
        ratio = V(best_s, r) / vmax(r)
        require(ratio >= F(3, 2), r, best_s)
        require(vmax(r) == V(r, r), r)                       # regular blocks are the s = r case
        require((r - 1) * (1 - tau(r) ** r) >= 1, r)         # inequality used in Lemma 7.2
        worst = ratio if worst is None else min(worst, ratio)
        if r <= 12 or r % 20 == 0:
            print(f"r={r:3d}  Vmax={float(vmax(r)):.6f}  best s={best_s:3d}  V={float(V(best_s, r)):.6f}  ratio={float(ratio):.4f}")
    print(f"minimum ratio over 2<=r<=199: {float(worst):.4f}")


def part2():
    print("Part 2: constants for r >= 200 with s = ceil(0.42 r), 60-digit decimal evaluation")
    q200 = F(199, 200) ** 200                                 # q_r = (1-1/r)^r increases in r
    q200d = Decimal(q200.numerator) / Decimal(q200.denominator)
    require(q200d > Decimal(1) / 4)
    vbound = q200d - 2 * q200d ** 2                           # Vmax(r) <= q_r - 2 q_r^2 <= this
    q_hi = Decimal("-0.42").exp()                             # q_s <= exp(-s/r) <= exp(-0.42)
    q_lo = (Decimal("0.425") * q200d.ln()).exp()              # q_s >= q_r^(s/r) >= q_200^(0.425)
    require(q_lo >= Decimal(1) / 2)                           # so q(1-q) >= q_hi (1 - q_hi)
    qq = q_hi * (1 - q_hi)
    sq = Decimal("-0.84").exp()                               # q^2 <= exp(-2 s/r)
    ratio2 = (Decimal("0.425") * 200 / 199) ** 2              # s^2/(r-1)^2 with s <= 0.425 r, r >= 200
    hub_low = qq - sq * ratio2
    margin = hub_low - Decimal("1.5") * vbound
    require(margin > Decimal("0.00005"), margin)
    print(f"Vmax(r) <= {float(vbound):.6f}; hub variance >= {float(hub_low):.6f}; "
          f"hub - 1.5 Vmax >= {float(margin):.6f}")


def block_law(r, s, k):
    """Law of the number of hit leaves in a block of s leaves carried by k copies of one r-edge."""
    c = r - s
    return [comb(s, j) * sum((-1) ** i * comb(j, i) * F(c + j - i, r) ** k for i in range(j + 1))
            for j in range(s + 1)]


def convolve(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out


def dlog(x):
    return Decimal(x.numerator).ln() - Decimal(x.denominator).ln()


def entropy(law):
    return -sum(Decimal(p.numerator) / Decimal(p.denominator) * dlog(p) for p in law if p)


def binary_entropy(p):
    return entropy([p, 1 - p]) if 0 < p < 1 else Decimal(0)


def hub_lower_bound(n, r, s):
    """Lower bound H(W) - H(N_hub) for the hub design with c = r - s hubs (proof of Theorem 7.3)."""
    c = r - s
    b, e = divmod(n - c, s)
    if b < 1:
        return None
    law = block_law(r, s, s + c + e)
    base = block_law(r, s, s)
    for _ in range(b - 1):
        law = convolve(law, base)
    require(sum(law) == 1, n, r, s)
    missed = F(r - 1, r) ** n
    return entropy(law) - c * binary_entropy(missed)


def part3(nmax):
    print(f"Part 3: finite certificates, every n from N_r to {nmax}")
    starts = {2: 6, 3: 10, 4: 16, 5: 20, 6: 26, 7: 31, 8: 38}
    for r, start in starts.items():
        margin_min = None
        for n in range(start, nmax + 1):
            upper = (2 * PI * E1 * (n * Decimal(vmax(r).numerator) / Decimal(vmax(r).denominator) + Decimal(1) / 12)).ln() / 2
            best = None
            for s in range(1, r):
                low = hub_lower_bound(n, r, s)
                if low is not None and (best is None or low > best[0]):
                    best = (low, s)
            margin = best[0] - upper
            require(margin > Decimal("1e-6"), r, n, margin)
            margin_min = margin if margin_min is None else min(margin_min, margin)
        # the start is sharp within this family: n = N_r - 1 is not certified
        n = start - 1
        upper = (2 * PI * E1 * (n * Decimal(vmax(r).numerator) / Decimal(vmax(r).denominator) + Decimal(1) / 12)).ln() / 2
        lows = [hub_lower_bound(n, r, s) for s in range(1, r)]
        require(max(x for x in lows if x is not None) <= upper, r, n)
        print(f"r={r}: hub design beats every balanced design for {start} <= n <= {nmax}; "
              f"smallest margin {float(margin_min):.6f} nats; n={start - 1} not certified by this bound")


if __name__ == "__main__":
    import sys
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    part1()
    part2()
    part3(nmax)
    print("PASS")
    print(f"explicit checks passed: {_REQUIRE_COUNT[0]}")
