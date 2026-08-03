# 66-System Taxonomy Independent-Coder Agreement Summary

This file reports the manuscript-facing taxonomy reliability audit over the final 66-system corpus. It combines the 62-system independent-pair recoding sheet with the four later-system independent recodings after normalizing all label names to the manuscript codebook.

## Independent-Coder Pair Agreement

| Field | Agreement evidence |
|---|---:|
| display_paradigm | 65/66 (98.5%), Cohen kappa 0.980 |
| control_subtype | 64/66 (97.0%), Cohen kappa 0.967 |
| retrieval_tag | complete raw agreement, 66/66 (100.0%) |
| analysis_tag | complete raw agreement, 66/66 (100.0%) |
| deployment_scenario | complete raw agreement, 66/66 (100.0%) |

## Boundary Notes

- The remaining display-paradigm disagreement is PATCH, where one independent coder emphasized the agentic search structure and the other emphasized the procedural/scripted loop.
- The two remaining control-subtype disagreements are PATCH and TSAPR. These are boundary systems where search, judge, and scripted-loop evidence overlap.
- PailGen was a supplemental boundary case: both independent coders marked a fine-tuning-style label in the supplemental sheet, while the final adjudicated manuscript label is Prompting because the retained paper is centered on in-context, fix-pattern-aware generation rather than model-parameter adaptation as the display paradigm.
- Both raw retrieval coders marked PailGen as retrieval-negative. A targeted full-text recheck (Approach Sections 3.1-3.2, p. 5) confirmed query-time BM25 + DPR retrieval, so the raw no/no fields are preserved while `final_retrieval_tag` records the adjudicated yes label.
- The final coding sheet is `artifact/taxonomy_assignment_audit.csv`; deployment-scenario labels are in `artifact/scenario_assignment_audit.csv`.
