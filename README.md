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
- `artifact/screening_agreement_labels_474.csv`
- `artifact/compute_screening_agreement.py`
- `artifact/taxonomy_assignment_audit.csv`
- `artifact/taxonomy_independent_pair_66_audit.csv`
- `artifact/taxonomy_independent_pair_66_agreement_summary.md`
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
- Local submission-package folders, draft response files, temporary annotation handoff files, and generated text caches are excluded from Git tracking.
- The retained-paper full-text PDFs are included as auditable source material. The structured audit data, reproduction scripts, and table-to-file mappings under `artifact/` remain the authoritative interface for reproducing manuscript counts and labels.
