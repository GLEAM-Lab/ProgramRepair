#!/usr/bin/env python3
"""Reproduce the screening counts reported in the survey.

The base screening counts are counted from frozen stage files exported from
the repository history. The April 2026 update is folded into the same table
using the title-refined update CSV and the full-text decision note, so the
script emits the final single-stage table used by the paper.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FROZEN = ARTIFACT / "frozen_results_2025-10-31"


def count_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_update_decisions(path: Path) -> tuple[int, int]:
    add_core = 0
    published_non_core = 0
    row_re = re.compile(r"^\| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|")
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            match = row_re.match(line.strip())
            if not match:
                continue
            decision = match.group(1).strip()
            if decision == "Decision":
                continue
            if decision == "Add/core":
                add_core += 1
            elif decision in {
                "Related Work only",
                "Boundary/RQ3 only",
                "Exclude/boundary",
                "Benchmark/protocol only",
                "Evaluation only",
                "Exclude",
            }:
                published_non_core += 1
    return add_core, published_non_core


def main() -> None:
    base_counts = {
        "search_query_hits": count_lines(FROZEN / "stage1.jsonl"),
        "repair_related_filter": count_lines(FROZEN / "stage2.jsonl"),
        "llm_related_filter": count_lines(FROZEN / "stage3.jsonl"),
        "benchmark_related_filter": count_lines(FROZEN / "stage4.jsonl"),
        "snowballing": count_lines(FROZEN / "stage5.jsonl"),
        "representative_works": count_lines(FROZEN / "stage6.jsonl"),
    }

    update_rows = read_csv_rows(
        ARTIFACT / "latest_venue_update_candidates_2026-05-01_refined_title.csv"
    )
    title_screen_rows = [
        row
        for row in update_rows
        if row.get("title_refined_triage", "").startswith("must_screen_title")
        or row.get("title_refined_triage", "").startswith("manual_screen_title")
    ]
    add_core, published_non_core = parse_update_decisions(
        ARTIFACT / "published_only_update_decisions_2026-05-01.md"
    )

    published_update_candidates = add_core + published_non_core

    update_increments = {
        "query_hits": len(update_rows),
        "title_screen_candidates": len(title_screen_rows),
        "published_full_text_candidates": published_update_candidates,
        "retained_additions": add_core,
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
                + update_increments["published_full_text_candidates"]
            ),
            "snowballing": (
                base_counts["snowballing"]
                + update_increments["published_full_text_candidates"]
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
