# Which dice colourings make the number of colours seen most uncertain?

**Fair coins, hub designs and a local limit theorem for doubly stochastic occupancy**

Author: Anonymous. Text CC0-1.0; code MIT. Unrefereed research candidate, version 0.1.0-candidate.

DOI [10.5281/zenodo.24519025](https://doi.org/10.5281/zenodo.24519025) (all versions: [10.5281/zenodo.24519024](https://doi.org/10.5281/zenodo.24519024)).
Release page: https://evidencepress.org/releases/dice-colouring-entropy-hub-designs/

## What this is about

Take some dice and some colours. Paint each die's faces with different colours (a colour may be reused on other dice), roll every die once, and count how many different colours show up. How should the dice be painted so that this count is as unpredictable as possible, in the sense of largest Shannon entropy? Christos Pelekis posed this question in 2019. It is a clean test of how the shape of the dependence between random events affects a random count.

Pelekis proved an upper bound of about half the logarithm of the number of colours. He conjectured that the colours should be spread as evenly as possible over the dice, that a cycle (for coins) or a "circular" design (for dice) is optimal, and that the circular design reaches the right order (his Conjecture 4.1). Research records of the trureturing project had refuted the even-spread and circular conjectures at one small size each by exact computation, and proposed, without proof, the answer for three colours.

What this paper shows:

- **Coins, exactly.** For every large enough palette and any number of coins at least the number of colours, the unique best design puts one shared colour on every coin and pairs it once with each other colour. Up to three leftover coins repeat three different pairs; four or more leftover coins should all repeat the same pair. The palette threshold is not explicit; it is at least ten, because a nine-colour exception is certified exactly. With three colours the optimum is found for every number of coins, which proves the trureturing proposal.
- **Dice with any number of faces.** "Hub" designs, in which a few shared colours sit on every die, beat every evenly spread design once there are many colours, by at least half the logarithm of 1.5 (in nats). So the even-spread conjecture and the cycle and circular conjectures fail for every die size, not only at small cases. For 2- to 8-sided dice the comparison is certified exactly from small sizes up to 120 colours. The best design for dice with three or more faces is not identified.
- **Conjecture 4.1 holds,** with a constant that does not depend on the die size. For a fixed die size this part follows from a short argument; the contribution is the uniformity and the precision.
- **The engine.** A local limit theorem (a precise bell-curve law for individual values) for the number of distinct values when each row of any doubly stochastic matrix is sampled once, with every error measured by the expected number of collisions, plus Edgeworth expansions, the first entropy correction and a saddlepoint formula. The central limit theorem in this setting is due to D'yakonova and Mikhailov.

The general theorems rest on the proofs in `manuscript.pdf`. The scripts check identities, constants and small cases only.

## Contents

- `manuscript.tex`, `manuscript.pdf`: the paper (19 pages).
- `checks/`: eight Python 3.10+ standard-library scripts and their recorded output (`.log`). Every check is explicit and stays active under `python -O`; each script prints the number of checks passed and exits with an error if one fails.
  - `check_models.py`: the switch construction, variance identities and the variance formula for regular designs on 9,635 rational matrices and small designs, in exact arithmetic.
  - `check_polymers.py`: the polymer identity behind the cumulant bounds (Lemma 4.1), exactly.
  - `check_entropy.py`: the entropy correction of Theorem 5.1 against exact entropies for repeated 2×2 blocks (squared-skewness coefficient near 1/12).
  - `check_rank3.py`: all 3-regular designs up to eight vertices (Table 1).
  - `check_coins.py`: every coin design for n = 3, 4, 5 and m ≤ n + 2, and rankings of star designs up to n = 500 with outward-rounded entropy intervals.
  - `check_twohubs.py`: the two-hub transfer law and comparisons (Proposition 9.2).
  - `check_threshold.py`: the nine-colour exception that shows the palette threshold is at least ten.
  - `check_hubs.py`: the hub-design variance gap (Lemma 7.2) and the finite certificates of Corollary 7.4 for 2- to 8-sided dice up to 120 colours.
- `ci/compare_logs.py`: compares fresh output with the recorded logs under the policy below.

## Reproduce

From the package root (no network needed):

```sh
for f in coins entropy models polymers rank3 threshold twohubs; do python3 -O checks/check_$f.py > new_$f.log; done
python3 -O checks/check_hubs.py 120 > new_hubs.log
```

Every script ends with `PASS` or a summary line followed by `explicit checks passed: N`, with N = 19718 (coins), 1 (entropy), 48305 (models), 20 (polymers), 1441148 (rank3), 6 (threshold), 1810 (twohubs) and 3984 (hubs). The whole run takes about a minute on a laptop. To compare with the recorded logs, put the new files in a directory under the names `check_<name>.log` and run `python3 ci/compare_logs.py checks <directory>`.

To typeset the paper, run `pdflatex manuscript.tex` twice.

### Cross-platform comparison

The decisive checks use exact arithmetic (integers, fractions, outward-rounded or 60-digit decimal arithmetic), except two declared float tolerances inside the scripts (3e-4 in `check_entropy.py`, 1e-12 in the additional comparisons of `check_twohubs.py`). Fresh logs must match the recorded logs line by line, with every word, integer, fraction and check count equal exactly; printed decimals may differ by a relative 1e-6 in `check_entropy.log` and 1e-9 elsewhere. On the release platform every log was reproduced byte for byte. The GitHub Actions workflow `.github/workflows/replay.yml` runs all eight scripts under `python -O` on Linux, makes this comparison and runs a negative control (an inverted polymer identity must be rejected).

## Release records

- `AI_INDEX.md`: machine-oriented map of claims, evidence and limits.
- `REVIEW_SUMMARY.md`: the internal review, its objections and their dispositions.
- `RESEARCH_GATES.json`: dated literature checks, sources read and limitation triage.
- `REPLAY_RECEIPT.md`, `ENVIRONMENT.txt`: the release replay and its environment.
- `refs.bib`: the bibliography. `CITATION.cff`, `.zenodo.json`: citation metadata. `LICENSE.md`: licences.
- `requirements.txt`: Python 3.10+ standard library only.
- `MANIFEST.sha256`: SHA-256 sums of every file.

## AI use

The mathematics, scripts and text were produced with substantial help from AI systems. They were checked by internal AI-assisted review and by the scripts above (see `REVIEW_SUMMARY.md`). No external peer review has taken place.
