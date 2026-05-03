#!/usr/bin/env python3
"""Compute agreement statistics from the human taxonomy annotation sheet."""

from __future__ import annotations

import csv
import math
import sys
from collections import Counter
from pathlib import Path


TRACKED_FIELDS = [
    ("primary_paradigm", "kappa"),
    ("retrieval_tag", "kappa"),
    ("analysis_tag", "kappa"),
    ("primary_scenario", "raw"),
]


def normalize(value: str) -> str:
    return value.strip()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def paired_values(rows: list[dict[str, str]], field: str) -> list[tuple[str, str, str]]:
    pairs = []
    for row in rows:
        left = normalize(row.get(f"coder_1_{field}", ""))
        right = normalize(row.get(f"coder_2_{field}", ""))
        if left and right:
            pairs.append((row["system"], left, right))
    return pairs


def raw_agreement(pairs: list[tuple[str, str, str]]) -> tuple[int, int, float]:
    matches = sum(1 for _, left, right in pairs if left == right)
    total = len(pairs)
    rate = matches / total if total else math.nan
    return matches, total, rate


def cohens_kappa(pairs: list[tuple[str, str, str]]) -> float:
    if not pairs:
        return math.nan
    total = len(pairs)
    observed = sum(1 for _, left, right in pairs if left == right) / total
    left_counts = Counter(left for _, left, _ in pairs)
    right_counts = Counter(right for _, _, right in pairs)
    categories = set(left_counts) | set(right_counts)
    expected = sum((left_counts[c] / total) * (right_counts[c] / total) for c in categories)
    if math.isclose(1.0, expected):
        return 1.0 if math.isclose(observed, 1.0) else math.nan
    return (observed - expected) / (1 - expected)


def disagreement_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    flagged = []
    for row in rows:
        disagreements = []
        for field, _ in TRACKED_FIELDS:
            left = normalize(row.get(f"coder_1_{field}", ""))
            right = normalize(row.get(f"coder_2_{field}", ""))
            if left and right and left != right:
                disagreements.append(field)
        if disagreements:
            flagged.append(
                {
                    "system": row["system"],
                    "fields": ", ".join(disagreements),
                    "coder_1_primary_paradigm": row.get("coder_1_primary_paradigm", ""),
                    "coder_2_primary_paradigm": row.get("coder_2_primary_paradigm", ""),
                    "coder_1_primary_scenario": row.get("coder_1_primary_scenario", ""),
                    "coder_2_primary_scenario": row.get("coder_2_primary_scenario", ""),
                }
            )
    return flagged


def print_summary(rows: list[dict[str, str]]) -> None:
    print("Agreement summary")
    print("=================")
    for field, mode in TRACKED_FIELDS:
        pairs = paired_values(rows, field)
        matches, total, rate = raw_agreement(pairs)
        if total == 0:
            print(f"- {field}: no paired labels yet")
            continue
        if mode == "kappa":
            kappa = cohens_kappa(pairs)
            print(f"- {field}: {matches}/{total} agreement ({rate:.1%}), Cohen's kappa = {kappa:.3f}")
        else:
            print(f"- {field}: {matches}/{total} agreement ({rate:.1%})")

    flagged = disagreement_rows(rows)
    print()
    print(f"Rows with at least one disagreement: {len(flagged)}")
    if not flagged:
        return

    print()
    print("Disagreement details")
    print("====================")
    for row in flagged:
        print(
            f"- {row['system']}: {row['fields']} | "
            f"paradigm [{row['coder_1_primary_paradigm']}] vs [{row['coder_2_primary_paradigm']}] | "
            f"scenario [{row['coder_1_primary_scenario']}] vs [{row['coder_2_primary_scenario']}]"
        )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 artifact/compute_annotation_agreement.py <annotation_csv>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    rows = load_rows(path)
    print_summary(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
