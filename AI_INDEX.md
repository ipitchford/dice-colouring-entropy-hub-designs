# AI index: Which dice colourings make the number of colours seen most uncertain? (v0.1.0-candidate)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What
this is about") and the paper [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex); Section 1 is
a plain introduction with a roadmap). DOI 10.5281/zenodo.24519025 (concept 10.5281/zenodo.24519024). Status:
unrefereed candidate; internal AI-assisted review only.

## Normalisation

A design (painting) is a multi-hypergraph on n vertices (colours) with m edges (dice), each edge a set of r distinct
vertices; colours may repeat across dice and edges may repeat. Rolling orients each edge to a uniform vertex; X = number
of vertices hit (colours seen). H = Shannon entropy in nats, H_2 = H / log 2 in bits. r = 2: coins, designs are loopless
multigraphs. Evenly spread = all degrees differ by at most one; with m = n these are the r-regular designs. Doubly
stochastic model: P = (p_iv) n×n doubly stochastic, Y_i drawn from row i independently, X = |{Y_1..Y_n}|,
d_i = 1 − Σ_v p_iv², S = Σ_i d_i = 2 E(number of colliding pairs), σ² = Var X, κ_3 = third cumulant.
Star G*_{n,t}: one hub joined once to every other vertex, plus t = m − n + 1 extra edges on spokes (t ≤ 3: distinct
spokes; t ≥ 4: one spoke). Hub design H_{n,r,s}: c = r − s hubs on every edge, blocks of s leaves, edge multiplicity s
(first block s + c + ι). V(s,r) = q(1−q) + (s−1)q²(τ^s − 1), q = (1 − 1/r)^s; V_max(r) = maximal variance per vertex of
regular designs. Statement numbers follow the manuscript (Theorems A–C in Section 1; one shared counter per section).
Pelekis = Pelekis (2019), Le Matematiche 74(1) 119–130, arXiv:1808.04166; tt = trureturing research records (release
7e88bc61b4ae); DM = D'yakonova and Mikhailov, doi:10.1515/dma.1992.2.3.325; GK = Gavalakis and Kontoyiannis,
doi:10.1016/j.spa.2023.104294.

## Claims and where they are proved

| ID | Claim | Location | Status / credit |
|---|---|---|---|
| A (main) | Absolute n_0: for n ≥ n_0 and m ≥ n the unique entropy maximiser among loopless multigraphs (up to relabelling) is G*_{n,m−n+1} | Theorem A; Theorem 9.3 | written proof; n_0 ineffective |
| A1 | Fixed surplus t: G*_{n,t} unique maximiser for large n, H = ½ log(2πe((n−1)/4 − f(t))) + O_t(n^−2), f(t) = min{t/16, ¼(1−2^−t)²}; others lose ≥ c_t/n | Theorem 9.1 | written proof |
| A2 | Two-hub comparison: placing all leaves on one hub beats any nontrivial split | Proposition 9.2 | written proof; checked by check_twohubs.py |
| A3 | n_0 ≥ 10: at n = 9, m = 11 one quadrupled spoke beats three doubled spokes by about 5.03e−5 nats | Section 9 "The threshold" | exact certificate (check_threshold.py) |
| A4 | Three colours, every m ≥ 3: optimum two pairs with multiplicities 1, m−1, except 2, 2 at m = 4; law (ε, ½+ε, ½−2ε), ε = 2^−m | Section 9 "The three-colour family" | written proof; proves the candidate proposed in tt |
| B (main) | Every r ≥ 2, m = n: some hub design beats every evenly spread design by ≥ ½ log 1.5 − o(1) nats | Theorem B; Proposition 7.1, Lemma 7.2, Theorem 7.3 | written proof; entropy limit via GK Theorem 1.1 |
| B1 | Pelekis's Conjecture 1.3 (even spread) and cycle / circular maximality fail for every r ≥ 2 and all large n (r = 2: also every m ≥ n) | Corollary 7.4 | written proof; earlier single small counterexamples in tt |
| B2 | Finite certificates: for r = 2..8 the hub design beats every evenly spread design for every n from 6, 10, 16, 20, 26, 31, 38 to 120; smallest margin 0.012 nats | Corollary 7.4 | exact rationals, 60-digit logarithms (check_hubs.py part 3) |
| B3 | V(s,r) ≥ 1.5 V_max(r) for every r ≥ 2 (best ratio ≥ 1.539 for r ≤ 199; analytic for r ≥ 200) | Lemma 7.2 | exact computation plus written proof (check_hubs.py parts 1–2) |
| C (main) | For every doubly stochastic P: cS ≤ σ² ≤ S/2, sup_k P(X=k) ≤ C(1+S)^−½, H = ½ log(1+S) + O(1); local limit theorem with error C/√S (optimal); every fixed order of the lattice Edgeworth expansion; H = ½ log(2πeσ²) − κ_3²/(12σ⁶) + O(S^−2); saddlepoint formula | Theorem C; Lemmas 3.1–3.2, 4.1–4.2, Theorem 5.1, Proposition 5.2 | written proof; CLT itself due to DM (credited) |
| D | Pelekis's Conjecture 4.1: every r-regular design has H_2 = ½ log_2 n + O(1) with an absolute constant; circular design ≥ ½ log_2(n/r) − O(1) | Corollary 1.1; Section 6 | written proof; fixed-r case also follows from a short window argument, as stated |
| E | Regular designs: exact variance formula; eventual entropy maximisers among regular designs of ranks two and three (Table 1: residual defects 0, 120, 192) | Proposition 6.1, Theorem 6.2 | written proof; Table 1 checked by check_rank3.py |
| F | Diffuse and near-permutation regimes (Poisson approximation of empty cells) | Section 8 | written proof; compared with Mikhailov Theorem 1, no improvement claimed |
| G | Open: explicit n_0; optimal designs for r ≥ 3; sharp inf σ²/S; regular designs for r ≥ 4 | Section 10 | open |

## Evidence

| Check | Script | Output | Scope |
|---|---|---|---|
| Switch construction, variance identities, Proposition 6.1 on 9,635 rational matrices and small designs | [checks/check_models.py](checks/check_models.py) | [checks/check_models.log](checks/check_models.log) (48305 checks) | exact rationals |
| Polymer identity of Lemma 4.1 | [checks/check_polymers.py](checks/check_polymers.py) | [checks/check_polymers.log](checks/check_polymers.log) (20 checks) | exact |
| Entropy correction of Theorem 5.1 on repeated 2×2 blocks; squared-skewness coefficient 0.0835 at 2048 blocks, within 3e−4 of 1/12 | [checks/check_entropy.py](checks/check_entropy.py) | [checks/check_entropy.log](checks/check_entropy.log) | double precision, declared tolerance |
| All 3-regular designs up to eight vertices; Table 1 | [checks/check_rank3.py](checks/check_rank3.py) | [checks/check_rank3.log](checks/check_rank3.log) (1441148 checks) | exact |
| All coin designs for n = 3, 4, 5, m ≤ n + 2 (19,333 labelled graphs); star rankings up to n = 500 | [checks/check_coins.py](checks/check_coins.py) | [checks/check_coins.log](checks/check_coins.log) (19718 checks) | outward-rounded intervals |
| Two-hub transfer law (260 exact laws) and 1,152 numerical comparisons | [checks/check_twohubs.py](checks/check_twohubs.py) | [checks/check_twohubs.log](checks/check_twohubs.log) (1810 checks) | exact laws; comparisons with tolerance 1e−12 |
| Nine-colour exception (n = 8, 9, 10) | [checks/check_threshold.py](checks/check_threshold.py) | [checks/check_threshold.log](checks/check_threshold.log) | signs certified by integer products |
| Lemma 7.2 and the finite ranges of Corollary 7.4 | [checks/check_hubs.py](checks/check_hubs.py) | [checks/check_hubs.log](checks/check_hubs.log) (3984 checks) | exact rationals, 60-digit Decimal logarithms |
| Log comparison under the declared policy | [ci/compare_logs.py](ci/compare_logs.py) | CI | tokens exact; decimals relative 1e−6 (entropy) or 1e−9 |

Numbers quoted on the release page and in the audio: threshold at least ten; the nine-colour exception; up to three
extra coins on distinct pairs, four or more on one pair; entropy gap at least half the log of 1.5; certified ranges for
2- to 8-sided dice up to 120 colours; three colours solved for every number of coins. All are proved or in the
recorded output.

## Limits

The coin theorem holds for all sufficiently large palettes with an ineffective threshold (only n_0 ≥ 10 is known).
For r ≥ 3 the hub designs beat evenly spread designs but the true optimum is not identified. Conjecture 4.1 for a fixed
r is the easy part; the contribution is uniformity and precision. The scripts check identities, constants and small
cases; the proofs carry the general claims. Prior-art searches were of limited scope.

## Replay and records

Replay commands and comparison policy: [README.md](README.md), [ENVIRONMENT.txt](ENVIRONMENT.txt),
[REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), CI [.github/workflows/replay.yml](.github/workflows/replay.yml). Review:
[REVIEW_SUMMARY.md](REVIEW_SUMMARY.md). Prior art and limitation triage: [RESEARCH_GATES.json](RESEARCH_GATES.json).
Bibliography: [refs.bib](refs.bib). Dependencies: [requirements.txt](requirements.txt). Licences:
[LICENSE.md](LICENSE.md). Citation: [CITATION.cff](CITATION.cff). Hashes: [MANIFEST.sha256](MANIFEST.sha256).
