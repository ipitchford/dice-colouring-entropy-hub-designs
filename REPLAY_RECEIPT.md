# Replay receipt (0.1.0-candidate, 25 November 2026)

**Environment.** macOS arm64; CPython 3.14.7 (requested as `uv run --no-project --python 3.12 python3`, which a
`python3` shim resolves to 3.14.7 on this host; the version was printed inside the run). Standard library only. The
runs used a fresh copy of the approved candidate, cwd = package root, flags `-I -B -O`, `PYTHONDONTWRITEBYTECODE=1`.
Output went to a separate directory, never over the shipped logs.

| Command (all under `python3 -I -B -O`) | Exit | Time | Result |
|---|---|---|---|
| `checks/check_coins.py` | 0 | 1 s | explicit checks passed: 19718 |
| `checks/check_entropy.py` | 0 | 1 s | PASS; explicit checks passed: 1 |
| `checks/check_models.py` | 0 | 1 s | PASS; explicit checks passed: 48305 |
| `checks/check_polymers.py` | 0 | <1 s | 20 exact checks; explicit checks passed: 20 |
| `checks/check_rank3.py` | 0 | 12 s | PASS; explicit checks passed: 1441148 |
| `checks/check_threshold.py` | 0 | <1 s | PASS; explicit checks passed: 6 |
| `checks/check_twohubs.py` | 0 | <1 s | PASS; explicit checks passed: 1810 |
| `checks/check_hubs.py 120` | 0 | 32 s | PASS; explicit checks passed: 3984 |

Every fresh output was byte-identical to the shipped `checks/*.log` file.

**Negative control (under -O).** In a second fresh copy the polymer identity check in `checks/check_polymers.py` was
inverted (`actual == via_expansion` changed to `actual != via_expansion`); the script stopped with "CHECK FAILED", exit 1.
The lead's earlier mutation run also made an inverted two-hub comparison fail.

**After the replay** only the title-page DOI line of `manuscript.tex`, the rebuilt PDF (three pdflatex passes, 19
pages; a word-level text comparison with the approved PDF shows only the DOI line) and the release records changed;
the scripts and recorded logs are byte-identical to the replayed candidate.

**Cross-platform policy** (declared before tagging; see ENVIRONMENT.txt and `ci/compare_logs.py`): fresh logs must
match line by line with every word, integer, fraction and check count equal exactly; printed decimals may differ by a
relative 1e-6 in `check_entropy.log` and 1e-9 in the other logs. The GitHub Actions workflow
`.github/workflows/replay.yml` checks the manifest, reruns all eight scripts under `python -O` on Linux, compares under
this policy and runs the negative control (one blocking job, about a minute of computation).

**Scope.** The scripts check identities, constants and small cases (the exhaustive coin searches, the rank-3 table, the
nine-colour exception and the hub-design certificates up to 120 colours). The proofs carry the general theorems.
