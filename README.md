# ProgramRepair

This repository contains the reproducibility artifact for:

**A Survey of LLM-based Automated Program Repair: Taxonomies, Design Paradigms, and Applications**

## Artifact Entry Point

Start from `artifact/README.md`.

The main auditable files for the current 66-system corpus are:

- `artifact/search_keywords_and_filters.md`
- `artifact/screening_transparency.md`
- `artifact/selection_reference_474_final_adjudicated.csv`
- `artifact/selection_reference_474_final_adjudicated_summary.json`
- `artifact/taxonomy_assignment_audit.csv`
- `artifact/taxonomy_three_coder_audit.csv`
- `artifact/taxonomy_three_coder_agreement_summary.md`
- `artifact/scenario_assignment_audit.csv`
- `artifact/benchmark_protocol_summary.md`
- `artifact/version_status_audit.md`
- `artifact/reproduce_screening_counts.py`
- `artifact/screening_count_reproduction_2026-05-01.json`
- `remote_results/pipeline.py`
- `remote_results/stage4.jsonl`
- `remote_results/stage5.jsonl`
- `remote_results/stage6.jsonl`

## Notes

- The public artifact focuses on auditable metadata, screening decisions, taxonomy assignments, benchmark summaries, and the released retrieval/filtering stages.
- Local submission-package folders, review-response drafts, Overleaf snapshots, raw full-text PDFs, and temporary annotation handoff files are excluded from Git tracking.
- The old full-text PDF library is intentionally not part of the public artifact; the auditable corpus is represented through metadata and coding tables under `artifact/`.
