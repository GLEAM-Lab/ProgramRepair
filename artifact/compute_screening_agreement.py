#!/usr/bin/env python3
"""Compute decision-agreement statistics for the 474-record screening audit."""

from __future__ import annotations

import csv
import math
import sys
from collections import Counter
from pathlib import Path


def normalize(value: str) -> str:
    return value.strip()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def cohens_kappa(left: list[str], right: list[str]) -> float:
    if len(left) != len(right):
        raise ValueError("paired vectors must have the same length")
    total = len(left)
    if total == 0:
        return math.nan
    observed = sum(a == b for a, b in zip(left, right)) / total
    left_counts = Counter(left)
    right_counts = Counter(right)
    labels = set(left_counts) | set(right_counts)
    expected = sum((left_counts[label] / total) * (right_counts[label] / total) for label in labels)
    if math.isclose(expected, 1.0):
        return 1.0 if math.isclose(observed, 1.0) else math.nan
    return (observed - expected) / (1 - expected)


def print_pair(name: str, left: list[str], right: list[str]) -> None:
    matches = sum(a == b for a, b in zip(left, right))
    total = len(left)
    rate = matches / total if total else math.nan
    print(f"- {name}: {matches}/{total} agreement ({rate:.2%}), Cohen's kappa = {cohens_kappa(left, right):.4f}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 artifact/compute_screening_agreement.py <screening_agreement_labels_csv>", file=sys.stderr)
        return 2

    rows = load_rows(Path(argv[1]))
    second_decisions = [normalize(row["second_coder_decision"]) for row in rows]
    third_raw_decisions = [normalize(row["third_coder_raw_decision"]) for row in rows]
    third_after_decisions = [normalize(row["third_coder_after_adjudication_decision"]) for row in rows]
    final_decisions = [normalize(row["final_reference_decision"]) for row in rows]

    print("Screening agreement summary")
    print("===========================")
    print_pair("second coder vs third coder raw include/exclude", second_decisions, third_raw_decisions)
    print_pair("third coder after adjudication vs final reference", third_after_decisions, final_decisions)

    print()
    disagreements = [
        row for row in rows if normalize(row["second_coder_decision"]) != normalize(row["third_coder_raw_decision"])
    ]
    print(f"Raw second/third coder disagreements: {len(disagreements)}")
    for row in disagreements:
        print(
            f"- {row['record_id']}: second={row['second_coder_decision']}, "
            f"third_raw={row['third_coder_raw_decision']} | {row.get('adjudication_note', '')}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
