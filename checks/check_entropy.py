#!/usr/bin/env python3
"""Check the first entropy correction in a balanced 2-by-2 block family."""
from math import comb, exp, fsum, lgamma, log, pi


_REQUIRE_COUNT = [0]


def require(condition, *info):
    """Explicit check that also runs under python -O (unlike assert)."""
    _REQUIRE_COUNT[0] += 1
    if not condition:
        raise SystemExit("CHECK FAILED: " + repr(info))

# Each 2-by-2 block has diagonal 9/10, off-diagonal 1/10.
# One box is empty with probability 2*(9/10)*(1/10)=9/50.
# For B independent blocks, vacancies therefore have exactly Bin(B,9/50).
p, q = 9/50, 41/50
for b in (32,64,128,256,512,1024,2048):
    # Exact integer probabilities, converted to doubles for entropy.
    den = 50**b
    probs=[comb(b,k)*9**k*41**(b-k)/den for k in range(b+1)]
    entropy = fsum(-mass*log(mass) for mass in probs if mass)
    var = b*p*q
    skewness_squared = (1-2*p)**2/var
    normal = .5*log(2*pi*exp(1)*var)
    predicted = normal-skewness_squared/12
    coefficient = (normal-entropy)/skewness_squared
    print(f'blocks {b:4d}: entropy nats {entropy:.12f}, deficit/skewness^2 {coefficient:.8f}, B^2*(prediction-entropy) {(predicted-entropy)*b*b:.7f}')
require(abs(coefficient-1/12)<0.0003)
print('PASS')
print(f"explicit checks passed: {_REQUIRE_COUNT[0]}")
