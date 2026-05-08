# Human Taxonomy Annotation Instructions

This package is for collecting human double-coding evidence for the current manuscript audit.

Primary files:

- `taxonomy_coding_guide.md`: operational definitions for the display paradigm, control subtype, and auxiliary tags
- `scenario_assignment_audit.csv`: the deployment-scenario scheme used in the current manuscript
- `human_taxonomy_annotation_template.csv`: the blank sheet to fill independently and then adjudicate
- `compute_annotation_agreement.py`: agreement script to run after both coders finish

## What each coder should label

Each coder should work independently and fill only their own columns:

- `coder_1_*` for coder 1
- `coder_2_*` for coder 2

Required fields per system:

- `display_paradigm`: the compact display-paradigm label used in the public CSV files; one of `Fine-Tuning`, `Prompting`, `Procedural`, `Agentic`
- `control_subtype`: use the current survey's control labels where possible
- `retrieval_tag`: `yes` or `no`
- `analysis_tag`: `yes` or `no`
- `deployment_scenario`: one of
  - `Localized benchmark repair`
  - `Repository-level issue resolution`
  - `Vulnerability repair`
  - `Educational tutoring`
  - `Industrial / practitioner workflow`
- `evidence_location`: where the coder found the supporting evidence
- `rationale`: one short sentence explaining the coding decision

## Suggested independence rules

To keep the coding defensible:

1. Each coder should complete the sheet without seeing the other coder's labels.
2. Coders should not edit the `adjudicated_*` fields.
3. If a paper looks borderline, the coder should still commit to one label and explain the uncertainty in the `rationale` field.
4. Adjudication should happen only after both coder columns are complete.

## Minimal process

1. Read `taxonomy_coding_guide.md`.
2. Fill the full `human_taxonomy_annotation_template.csv` independently.
3. Run `python3 artifact/compute_annotation_agreement.py artifact/human_taxonomy_annotation_template.csv`.
4. Review the disagreement rows printed by the script.
5. Fill the `adjudicated_*`, `adjudicator`, and `adjudication_basis` fields after discussion or third-author review.
6. Re-run the script if you want an updated disagreement report.

## Practical reading order

To accelerate coding without losing consistency:

1. Read `taxonomy_coding_guide.md`.
2. Re-open the original paper PDF for the target system.
3. Use the current survey text only as a navigation aid, not as the ground truth to copy.
4. For borderline systems, inspect the method section first, then the evaluation setting, then the implementation loop.

## Suggested agreement outputs

The script reports:

- Cohen's kappa for the display-paradigm field `display_paradigm`
- Cohen's kappa for `retrieval_tag`
- Cohen's kappa for `analysis_tag`
- raw agreement and disagreement counts for `deployment_scenario`
- the list of systems where the two coders disagree on at least one tracked field

## Scope note

- This package supports an independent human reliability audit for the current taxonomy.
- Screening-agreement evidence is reported separately in `selection_reference_474_final_adjudicated.csv` and `selection_reference_474_final_adjudicated_summary.json`.
