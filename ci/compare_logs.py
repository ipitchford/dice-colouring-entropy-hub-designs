# SPDX-License-Identifier: MIT
"""Compare fresh outputs of the eight check scripts with the recorded checks/*.log files.

Usage: python3 -I ci/compare_logs.py RECORDED_DIR NEW_DIR

Declared cross-platform policy (also in README.md, ENVIRONMENT.txt and REPLAY_RECEIPT.md):
- every log must have the same number of lines, and every token that is not a decimal number with a
  decimal point (words, integers, fractions, PASS, "explicit checks passed: N") must be equal exactly;
- decimal numbers (tokens with a decimal point or exponent) are float diagnostics printed from double-precision
  arithmetic; they must agree within relative tolerance 1e-6 in check_entropy.log (the publish brief notes
  last-digit differences across platforms there) and 1e-9 in every other log;
- check_hubs.log uses exact rationals and 60-digit Decimal logarithms and is compared with the same rule, which
  on the release platform reproduced it byte for byte.
Exit 0 if every log agrees, 1 otherwise. Explicit checks only (no assert), so it also works under python -O.
"""
import re
import sys
from pathlib import Path

NAMES = ['coins', 'entropy', 'models', 'polymers', 'rank3', 'threshold', 'twohubs', 'hubs']
NUM = re.compile(r'^[+-]?(\d+\.\d*|\.\d+|\d+(\.\d*)?[eE][+-]?\d+)$')


def tokens(line):
    return re.findall(r'[+-]?(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?|[+-]?\d+(?:[eE][+-]?\d+)?|[^\s\d+.-]+|[+.-]', line)


def compare(old, new, rel):
    a, b = old.splitlines(), new.splitlines()
    if len(a) != len(b):
        return f'{len(a)} recorded lines, {len(b)} new lines'
    for i, (x, y) in enumerate(zip(a, b), 1):
        tx, ty = tokens(x), tokens(y)
        if len(tx) != len(ty):
            return f'line {i}: token count differs'
        for s, t in zip(tx, ty):
            if s == t:
                continue
            if NUM.match(s) and NUM.match(t):
                u, v = float(s), float(t)
                if abs(u - v) <= rel * max(abs(u), abs(v), 1e-300):
                    continue
            return f'line {i}: {s!r} != {t!r}'
    return None


def main():
    rec, new = Path(sys.argv[1]), Path(sys.argv[2])
    bad = 0
    for n in NAMES:
        rel = 1e-6 if n == 'entropy' else 1e-9
        o = (rec / f'check_{n}.log').read_text()
        p = (new / f'check_{n}.log').read_text()
        err = compare(o, p, rel)
        exact = o == p
        if err:
            bad += 1
        print(f'check_{n}.log: ' + (f'DIFFERS ({err})' if err else ('identical' if exact else f'equal within declared tolerance {rel:g}')))
    print('ALL LOGS AGREE' if bad == 0 else f'{bad} LOG(S) DIFFER')
    sys.exit(0 if bad == 0 else 1)


if __name__ == '__main__':
    main()
