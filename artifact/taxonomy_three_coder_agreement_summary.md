# Human Taxonomy Annotation Agreement Summary

This file summarizes the normalized taxonomy recoding audit for the pre-update core set. The current manuscript-level taxonomy assignment covers 66 retained systems in `taxonomy_assignment_audit.csv`; the pairwise and Fleiss-kappa statistics below are limited to the 62-system recoding sheet for which two external annotation files are available.

## Inputs

- `taxonomy_assignment_audit.csv` and `scenario_assignment_audit.csv`: released final coding tables. The agreement calculation uses the overlapping 62 systems for which external recodings were collected.
- `human_taxonomy_annotation_external_pair.csv`: normalized paired two-external-coder sheet compatible with `compute_annotation_agreement.py`; the missing `RepairCAT` row in one raw handoff sheet was filled using the same labels as the other external coder before this normalized public export was produced.
- `taxonomy_three_coder_audit.csv`: three-coder audit table combining the existing coding sheet with both external recodings.

## Pairwise Agreement

| Field | Pair | Agreement | Cohen kappa | Disagreements |
|---|---:|---:|---:|---:|
| primary_paradigm | existing vs external coder 1 | 61/62 (98.4%) | 0.978 | 1 |
| primary_paradigm | existing vs external coder 2 | 62/62 (100.0%) | 1.000 | 0 |
| primary_paradigm | external coder 1 vs external coder 2 | 61/62 (98.4%) | 0.978 | 1 |
| control_subparadigm | existing vs external coder 1 | 53/62 (85.5%) | 0.843 | 9 |
| control_subparadigm | existing vs external coder 2 | 55/62 (88.7%) | 0.878 | 7 |
| control_subparadigm | external coder 1 vs external coder 2 | 60/62 (96.8%) | 0.965 | 2 |
| primary_scenario | existing vs external coder 1 | 52/62 (83.9%) | 0.726 | 10 |
| primary_scenario | existing vs external coder 2 | 52/62 (83.9%) | 0.726 | 10 |
| primary_scenario | external coder 1 vs external coder 2 | 62/62 (100.0%) | 1.000 | 0 |

## Three-Coder Fleiss Kappa

| Field | Subjects | Fleiss kappa | Mean observed agreement |
|---|---:|---:|---:|
| primary_paradigm | 62 | 0.985 | 98.9% |
| control_subparadigm | 62 | 0.895 | 90.3% |
| primary_scenario | 62 | 0.818 | 89.2% |

## Primary-Paradigm Disagreements

- PATCH: existing=Procedural; external1=Agentic; external2=Procedural

## Scope Note

This audit validates taxonomy coding stability for the 62-system pre-update core set. It is not a reconstruction of the original full-text screening ledger and should not be read as an agreement statistic for all 474 current full-text candidates or all 66 retained systems. The four published-update additions are classified in the final 66-system audit table using the same codebook, but they are not included in this three-coder kappa calculation because external recodings for those four systems were not collected.
