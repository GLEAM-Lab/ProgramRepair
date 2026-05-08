#!/usr/bin/env python3
"""Reproduce the screening counts reported in the survey.

The released repository contains row-level snapshots for the downstream
benchmark, snowballing, and retained-paper stages, plus the final 474-record
adjudicated screening sheet. The two upstream automatic-filter counts are
recorded as metadata because those intermediate query-hit files are not needed
for per-paper auditing and are not part of the public artifact.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
REMOTE_RESULTS = ROOT / "remote_results"

UPSTREAM_BASE_COUNTS = {
    "search_query_hits": 1581,
    "repair_related_filter": 994,
    "llm_related_filter": 726,
}

UPSTREAM_SUPPLEMENT_COUNTS = {
    "query_hits": 736,
    "title_screen_candidates": 26,
}


def count_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    base_counts = {
        **UPSTREAM_BASE_COUNTS,
        "benchmark_related_filter": count_lines(REMOTE_RESULTS / "stage4.jsonl"),
        "snowballing": count_lines(REMOTE_RESULTS / "stage5.jsonl"),
        "representative_works": count_lines(REMOTE_RESULTS / "stage6.jsonl"),
    }

    adjudicated_rows = read_csv_rows(
        ARTIFACT / "selection_reference_474_final_adjudicated.csv"
    )
    supplement_rows = [row for row in adjudicated_rows if row["record_id"].startswith("U-")]
    retained_supplements = [
        row for row in supplement_rows if row["final_reference_decision"] == "include"
    ]

    update_increments = {
        **UPSTREAM_SUPPLEMENT_COUNTS,
        "archival_full_text_candidates": len(supplement_rows),
        "retained_additions": len(retained_supplements),
    }

    result = {
        "screening_flow": {
            "search_query_hits": (
                base_counts["search_query_hits"] + update_increments["query_hits"]
            ),
            "repair_related_filter": (
                base_counts["repair_related_filter"]
                + update_increments["title_screen_candidates"]
            ),
            "llm_related_filter": (
                base_counts["llm_related_filter"]
                + update_increments["title_screen_candidates"]
            ),
            "benchmark_related_filter": (
                base_counts["benchmark_related_filter"]
                + update_increments["archival_full_text_candidates"]
            ),
            "snowballing": (
                base_counts["snowballing"]
                + update_increments["archival_full_text_candidates"]
            ),
            "representative_works": (
                base_counts["representative_works"]
                + update_increments["retained_additions"]
            ),
        },
        "update_increments": update_increments,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
