# Human Taxonomy Annotation Agreement Summary

This file summarizes the normalized taxonomy recoding audit for the 62-system core set. The current manuscript-level taxonomy assignment covers 66 retained systems in `taxonomy_assignment_audit.csv`; the pairwise and Fleiss-kappa statistics below are limited to the 62-system recoding sheet for which two external annotation files are available. The `display_paradigm` field in these files is the manuscript's compact display-paradigm label derived from the multidimensional codebook.

## Inputs

- `taxonomy_assignment_audit.csv` and `scenario_assignment_audit.csv`: released final coding tables. The agreement calculation uses the overlapping 62 systems for which external recodings were collected.
- `human_taxonomy_annotation_external_pair.csv`: normalized paired two-external-coder sheet compatible with `compute_annotation_agreement.py`; the missing `RepairCAT` row in one raw handoff sheet was filled using the same labels as the other external coder before this normalized public export was produced.
- `taxonomy_three_coder_audit.csv`: three-coder audit table combining the existing coding sheet with both external recodings; running `python3 artifact/compute_annotation_agreement.py artifact/taxonomy_three_coder_audit.csv` recomputes the pairwise Cohen-kappa and Fleiss-kappa values below.

## Pairwise Agreement

| Field | Pair | Agreement | Cohen kappa | Disagreements |
|---|---:|---:|---:|---:|
| display_paradigm | existing vs external coder 1 | 61/62 (98.4%) | 0.978 | 1 |
| display_paradigm | existing vs external coder 2 | 62/62 (100.0%) | 1.000 | 0 |
| display_paradigm | external coder 1 vs external coder 2 | 61/62 (98.4%) | 0.978 | 1 |
| control_subtype | existing vs external coder 1 | 53/62 (85.5%) | 0.841 | 9 |
| control_subtype | existing vs external coder 2 | 55/62 (88.7%) | 0.876 | 7 |
| control_subtype | external coder 1 vs external coder 2 | 60/62 (96.8%) | 0.964 | 2 |
| deployment_scenario | existing vs external coder 1 | 52/62 (83.9%) | 0.726 | 10 |
| deployment_scenario | existing vs external coder 2 | 52/62 (83.9%) | 0.726 | 10 |
| deployment_scenario | external coder 1 vs external coder 2 | 62/62 (100.0%) | 1.000 | 0 |

## Three-Coder Fleiss Kappa

| Field | Subjects | Fleiss kappa | Mean observed agreement |
|---|---:|---:|---:|
| display_paradigm | 62 | 0.985 | 98.9% |
| control_subtype | 62 | 0.894 | 90.3% |
| deployment_scenario | 62 | 0.818 | 89.2% |

## Display-Paradigm Disagreements

- PATCH: existing=Procedural; external1=Agentic; external2=Procedural

## Scenario-Label Adjudication Note

Deployment-scenario labels are descriptive deployment-scope labels. They are used for the manuscript's scenario-count table, but they do not define the display paradigm itself. The two external coders agreed with each other on all 62 scenario labels; however, the existing scenario sheet differed from the two external recodings for 10 systems, producing the lower three-coder Fleiss kappa reported above.

The 10 scenario-boundary cases were adjudicated against benchmark scope and full-text evidence before finalizing `scenario_assignment_audit.csv`. The final adjudicated sheet keeps scenario labels tied to the dominant benchmark/deployment scope:

| System | Final scenario used in `scenario_assignment_audit.csv` | Boundary source |
|---|---|---|
| InferFix | Localized benchmark repair | InferredBugs is treated as a localized benchmark setting, even though the method uses static analysis and retrieval. |
| Ehsani et al. | Localized benchmark repair | BugsInPy is treated as a localized benchmark setting rather than a vulnerability-repair setting. |
| RLCE | Repository-level issue resolution | RepoBugs evaluates repository-level context extraction for bug repair. |
| DsRepair | Localized benchmark repair | DS-1000 is treated as a data-science repair benchmark rather than a vulnerability dataset. |
| TracePrompt | Localized benchmark repair | HumanEval-Java is treated as a localized benchmark setting. |
| DRCodePilot | Industrial / practitioner workflow | The retained evidence is the Flink/practitioner workflow rather than a standard repository benchmark. |
| PATCH | Repository-level issue resolution | The BFP setting is retained as a repository/patch-assessment workflow rather than a localized benchmark. |
| VulDebugger | Vulnerability repair | The ExtractFix/ARVO evidence is vulnerability repair even though dynamic execution feedback is used. |
| Abstain and Validate | Industrial / practitioner workflow | The Google setting is retained as an industrial/practitioner workflow. |
| SpecRover | Repository-level issue resolution | SWE-bench Lite is treated as repository-level issue resolution rather than localized benchmark repair. |

## Scope Note

This audit assesses taxonomy coding stability for the 62-system core set. It should not be read as the screening-agreement statistic for all 474 current full-text candidates or as a new three-coder taxonomy-agreement calculation over all 66 retained systems. The four later corpus additions are classified in the final 66-system audit table using the same codebook, but they are not included in this three-coder kappa calculation because external recodings for those four systems were not collected.
