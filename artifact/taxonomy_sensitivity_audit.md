# Taxonomy Sensitivity Audit

This file records a post-hoc sensitivity check for the taxonomy coding rules.

Purpose:

- test whether the released coding guide yields stable primary-paradigm assignments for the 62-system audit subset
- make the remaining hybrid edge cases explicit

This audit is a taxonomy robustness check. It is separate from the 474-record screening-agreement audit documented in `screening_transparency.md`.

## Procedure

1. Mask the published primary-paradigm labels in `taxonomy_assignment_audit.csv`.
2. Re-apply `taxonomy_coding_guide.md` to the same 62-system audit subset.
3. Use a deliberately stricter control-first reading for hybrid cases:
   - if a system exposes a fixed outer controller, prefer `Procedural` unless the LLM clearly selects the next action or branch
   - if a system combines adaptation and autonomous control, explicitly test whether the paper's empirical emphasis is on model adaptation or on runtime control
4. Compare the recoding pass against the released primary-paradigm labels.

## Result

- Exact agreement: `58 / 62 = 93.5%`
- Cohen's kappa on the four-way primary-paradigm label: `0.91`
- Number of disagreements: `4`

## Borderline cases

| System | Released label | Sensitivity-pass label | Why this case is borderline |
|---|---|---|---|
| `HULA` | `Procedural` | `Agentic` | The planner/coder-agent framing can look agentic, but the released guide keeps it procedural because the overall human-in-the-loop workflow remains scripted. |
| `RepairAgent` | `Agentic` | `Procedural` | The outer controller is a finite-state scaffold, but the released guide assigns agentic because the model chooses actions at runtime. |
| `TSAPR` | `Agentic` | `Procedural` | Monte Carlo tree search supplies strong outer control, but the released guide treats the LLM judge as runtime branch control. |
| `Learn-by-Interact` | `Agentic` | `Fine-Tuning` | The paper includes both trajectory-driven adaptation and self-controlled runtime behavior; the released guide prioritizes runtime control for the reported system behavior. |

## Interpretation

The main consequence of this audit is that the taxonomy is reasonably stable at the top level, but hybrid systems are exactly where disagreements concentrate. This supports the revised manuscript's decision to:

- keep one primary paradigm for corpus-level aggregation
- record retrieval, analysis, and deployment scenario separately
- document the explicit hybrid edge cases rather than pretending the boundaries are perfectly crisp

## Follow-up path

If later human double-coding is collected, this file can be superseded by a true inter-rater audit without changing the paper structure. The companion template is `human_taxonomy_annotation_template.csv`.
