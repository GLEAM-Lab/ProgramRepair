# 66-System Taxonomy External-Coder Agreement Summary

This file reports the manuscript-facing taxonomy reliability audit over the final 66-system corpus. It combines the 62-system independent-pair recoding sheet with the four later-system independent recodings after normalizing all label names to the manuscript codebook.

## External-Coder Pair Agreement

| Field | Agreement | Cohen kappa |
|---|---:|---:|
| display_paradigm | 65/66 (98.5%) | 0.980 |
| control_subtype | 64/66 (97.0%) | 0.967 |
| retrieval_tag | 66/66 (100.0%) | 1.000 |
| analysis_tag | 66/66 (100.0%) | 1.000 |
| deployment_scenario | 66/66 (100.0%) | 1.000 |

## Boundary Notes

- The remaining display-paradigm disagreement is PATCH, where one external coder emphasized the agentic search structure and the other emphasized the procedural/scripted loop.
- The two remaining control-subtype disagreements are PATCH and TSAPR. These are boundary systems where search, judge, and scripted-loop evidence overlap.
- PailGen was a supplemental boundary case: both independent coders marked a fine-tuning-style label in the supplemental sheet, while the final adjudicated manuscript label is Prompting because the retained paper is centered on in-context, fix-pattern-aware generation rather than model-parameter adaptation as the display paradigm.
- The final coding sheet is `artifact/taxonomy_assignment_audit.csv`; deployment-scenario labels are in `artifact/scenario_assignment_audit.csv`.
