# Remote Screening Results

This directory contains the released retrieval and filtering artifacts used by the current survey manuscript.

## Files

- `pipeline.py`: executable retrieval/filtering pipeline used to construct the released stage snapshots.
- `requirements.txt`: Python dependencies for the pipeline.
- `stage4.jsonl`: released benchmark-related automatic-filter snapshot.
- `stage5.jsonl`: released snowballing/manual-supplement candidate snapshot.
- `stage6.jsonl`: released retained-work snapshot kept for traceability.

## Current Manuscript Counts

The current manuscript reports an integrated 66-system corpus. The reproducible screening-flow counts are computed by:

```bash
python3 artifact/reproduce_screening_counts.py
```

The expected output is also stored in `artifact/screening_count_reproduction_2026-05-01.json`.

The released `stage6.jsonl` file contains the 62 retained records from the released stage snapshot. The four archival-status additions and the final 66-system coding sheet are represented in `artifact/taxonomy_assignment_audit.csv`, `artifact/scenario_assignment_audit.csv`, and the 474-record adjudicated screening files under `artifact/`.
