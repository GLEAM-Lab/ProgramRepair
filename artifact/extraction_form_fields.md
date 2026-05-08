# Extraction Form Fields

This note documents the shared extraction form used to populate the current per-paper audit tables.

The form is designed to make the taxonomy, benchmark, and methodology claims auditable at the paper level. The populated outputs appear in `taxonomy_assignment_audit.csv` and `scenario_assignment_audit.csv`.

## Core fields

- `system`
  The canonical system or paper name used throughout the survey.
- `cited_version`
  The version cited in the current bibliography, for example the archival venue or retained preprint version.
- `venue_year`
  The year associated with the cited version used in the survey.
- `display_paradigm`
  The compact display-paradigm label used in the public CSV files; one of `Fine-Tuning`, `Prompting`, `Procedural`, `Agentic`.
- `control_subtype`
  The finer-grained control subtype within the display paradigm.
- `retrieval_tag`
  `yes` if explicit retrieval is a salient augmentation in the repair loop, otherwise `no`.
- `analysis_tag`
  `yes` if explicit analysis artifacts are a salient augmentation in the repair loop, otherwise `no`.
- `deployment_scenario`
  One of `Localized benchmark repair`, `Repository-level issue resolution`, `Vulnerability repair`, `Educational tutoring`, `Industrial / practitioner workflow`.
- `defect_scope`
  Broad scope such as general program repair, vulnerability repair, or both.
- `benchmark_family`
  Benchmark family used for corpus-level aggregation, for example `Defects4J`, `HumanEval-Java`, `SWE-bench Lite`.
- `benchmark`
  The concrete dataset or benchmark name reported by the paper.
- `base_model`
  The main backbone model used in the reported result.
- `adaptation_strategy`
  Short note such as full fine-tuning, LoRA, frozen prompting, judge-based loop, or tool-augmented agent.
- `metric_name`
  Primary reported metric, for example `pass@1`, `pass@10`, `F1`, `full match`, `accuracy`.
- `metric_value`
  Primary reported value corresponding to `metric_name`.
- `evaluation_assumptions`
  Major caveats or simplifying assumptions, such as perfect fault localization, single-function scope, train/test split, or human feedback.
- `code_release`
  `yes`, `no`, or `unclear` depending on whether implementation artifacts are publicly released.
- `data_release`
  `yes`, `no`, or `unclear` depending on whether evaluation data or benchmark artifacts are publicly released.
- `notes`
  Optional comments for borderline coding decisions.

## Scope note

- The released package preserves the finalized extraction outputs and the fields used to regenerate the manuscript tables.
- The purpose of this schema is transparency of what was extracted and how boundary fields are represented in the artifact.
