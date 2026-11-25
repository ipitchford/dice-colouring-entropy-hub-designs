# Review summary (public, 0.1.0-candidate)

This records the internal review of the candidate: who looked, what they raised, and what was done. It is
AI-assisted internal review, not peer review or independent reproduction.

## What ran

1. **Panel (round 1).** Five Claude reviewer roles: methodology (a line-by-line check of every proof) and devil's
   advocate as separate reviewers, and editor, domain (literature, attribution and novelty) and perspective
   (readability and significance) in one combined pass. The reviewers recomputed constants and identities
   independently, ran their own exhaustive and randomised searches over small coin designs, and checked the rank-3
   table and the three-colour family by brute force. No critical issue and no mathematical error was found.
2. **Lead proof audit.** The switch construction, the polymer bound, the entropy correction, the coin proofs, the
   rank-3 table and the three-colour family were checked again by the lead.
3. **Revision round.** One round addressed every item (table below) and added an extension: the hub designs of
   Section 7, which refute the even-spread and circular conjectures for every die size, with exact finite
   certificates for 2- to 8-sided dice up to 120 colours.
4. **Verification.** A re-review checked every first-round item against the revised text, and a proof audit checked
   every new or rewritten proof (Lemmas 2.1-2.3, 3.1 and 3.2 and all of Section 7). All were found correct; its
   minor wording, hypothesis and typesetting items were applied.
5. **Computation.** Eight standard-library scripts with explicit checks that stay active under `python -O` were
   replayed by the lead and again at release, with byte-identical output; negative controls (an inverted polymer
   identity, an inverted two-hub comparison) make the scripts fail.

No second-model (Astra/Codex) adversarial review took place for this release.

## Sources

Every cited work was obtained and read where the paper relies on it: Pelekis (2019) in the journal and arXiv
versions, the two trureturing research records, D'yakonova and Mikhailov (1992), Mikhailov (1998, read in the
Russian original), Hwang and Janson, Gavalakis and Kontoyiannis, Bobkov, Chistyakov and Götze, Vilenkin and
D'yachkov, Mirakhmedov and Mirakhmedov, Mirakhmedov, Jammalamadaka and Mohamed, Khakimullin and Enatskaya,
Barbour, Braunsteins and Ross, Pelekis (2016) and Sokal. The two classical inequalities the paper uses (Efron-Stein
and a martingale Bernstein inequality) are proved in Section 2, so the paper does not rely on outside statements
of them.

## Main objections and dispositions

| Objection | Disposition |
|---|---|
| Correctness | No error was found in round 1, in the lead's audit, in the re-review or in the proof audit. |
| "Circular-hypergraph entropy conjecture" is ambiguous and oversold: for a fixed die size Conjecture 4.1 follows from a short window argument (devil's advocate) | Now named "Conjecture 4.1 (the lower bound)"; the paper says the fixed-r case is easy and that the contribution is the absolute constant, uniformity over all doubly stochastic matrices, the sharp local rate and the entropy correction. |
| Consequences for Pelekis's other conjectures proved but not stated | Theorem B and Corollary 7.4 state them: the even-spread conjecture and cycle and circular maximality fail for every die size and all large palettes. |
| The regular-design maximisers do not answer the question for three or more faces | Said explicitly; the new hub designs show the optimum is unbalanced; the true optimum for r ≥ 3 is listed as open. |
| The palette threshold is ineffective | Stated in the abstract and Theorem A ("at least ten", with a certified nine-colour exception) and listed as the first open problem. An explicit threshold was attempted and judged beyond one revision round. |
| Three-colour family already proposed by trureturing | Credited; the paper now proves the candidate proposed there. |
| Central limit theorem attribution and the occupancy literature | The CLT is credited to D'yakonova and Mikhailov; Mikhailov's Poisson bounds, Khakimullin and Enatskaya, Barbour, Braunsteins and Ross, and Pelekis (2016) added and compared. |
| Check scripts used bare `assert`, so checks vanished under `python -O` | Every check raises explicitly, prints its count and fails under `-O` when an identity is inverted. |
| Readability and signposting | New title and context-first introduction (question, what was known, main results, literature, roadmap); every section opens with what it does; symbol clashes removed; compressed steps expanded. |

## Limits that remain

The coin theorem needs a sufficiently large palette with no explicit threshold (only "at least ten" is known). For dice
with three or more faces the hub designs beat evenly spread designs, but the optimum is not identified. The scripts
check identities, constants and small cases; the proofs carry the general theorems. Literature searches were of
limited scope (arXiv, Semantic Scholar, Crossref and web searches).
