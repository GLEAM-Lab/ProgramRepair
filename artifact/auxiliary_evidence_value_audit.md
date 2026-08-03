# Auxiliary-evidence value audit

## Provenance and prevalence

The two independent coders agree on all 66 raw retrieval tags, analysis tags, and deployment-scenario recodings. The raw fields remain unchanged in `taxonomy_independent_pair_66_audit.csv`.

The final auxiliary fields contain one documented update: PailGen changes from raw retrieval no/no to final_retrieval_tag=yes after a targeted full-text recheck confirmed query-time BM25 + DPR retrieval. No final analysis tag changes.

The final scenario field used below matches `scenario_assignment_audit.csv`; 10 older scenario labels were updated by the separate three-coder/full-text adjudication documented in `taxonomy_sensitivity_audit.md`. These fields cover only retrieval/RAG and program-analysis evidence; they do not exhaust test, human, or domain-knowledge context.

The five assurance outcomes are conservative second-pass lower-bound codings from `evaluation_assurance_corrected_by_system.csv`. They are not claimed to have independent-coder agreement and should not be read as an exhaustive audit of every assurance mechanism.

- Final retrieval tag: 29/66 (raw pair: 28/66).
- Final analysis tag: 59/66 (raw pair: 59/66).
- Final retrieval or analysis: 63/66 (raw pair: 62/66).
- Retrieval appears in: Agentic, Fine-Tuning, Procedural, Prompting.
- Analysis appears in: Agentic, Fine-Tuning, Procedural, Prompting.

## Association audit

The explicitly defined exploratory family is the Cartesian product of three auxiliary signals (retrieval, analysis, and their union) and seven outcomes (two deployment scenarios plus five assurance indicators), yielding 3 x 7 = 21 tests. All 21 tests are emitted before sorting and Benjamini-Hochberg correction.

The primary retrieval-by-repository/industrial table (15/29 versus 1/37) uses the final adjudicated retrieval and deployment-scenario labels. Its BH-adjusted q-value is specific to this explicitly defined 21-test exploratory family.

As a sensitivity check, replacing both final retrieval/scenario labels with the untouched raw independent-pair recodings leaves the same association as rank 1 (13/28 versus 1/38, OR=32.067, p=1.889743e-05, BH q=0.00039684603). Thus, the direction and corrected significance do not depend on the PailGen retrieval correction or the 10 scenario adjudications.

Associations surviving BH correction:

- retrieval_tag vs repository_or_industrial_scenario: 15/14 vs 1/36, OR=38.571, p=3.4340276e-06, q=7.2114579e-05.

## Interpretation boundary

The tags are useful as an orthogonal descriptive codebook because they preserve cross-cutting design information across display paradigms. This audit does not establish that a retrieval or analysis tag by itself improves repair quality, generalization, or evaluation rigor. The manuscript should therefore demonstrate their value through concrete mechanism-level examples or trade-offs, not by treating tag prevalence as an outcome.
