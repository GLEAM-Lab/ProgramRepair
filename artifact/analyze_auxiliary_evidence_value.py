#!/usr/bin/env python3
"""Audit whether retrieval/analysis tags yield defensible corpus-level insights."""

from __future__ import annotations

import csv
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TAXONOMY = ROOT / "taxonomy_independent_pair_66_audit.csv"
SCENARIOS = ROOT / "scenario_assignment_audit.csv"
ASSURANCE = ROOT / "evaluation_assurance_corrected_by_system.csv"
BY_SYSTEM = ROOT / "auxiliary_evidence_value_by_system.csv"
SUMMARY = ROOT / "auxiliary_evidence_value_summary.csv"
TESTS = ROOT / "auxiliary_evidence_value_tests.csv"
REPORT = ROOT / "auxiliary_evidence_value_audit.md"

TAGS = ("retrieval_tag", "analysis_tag", "retrieval_or_analysis_tag")
OUTCOMES = (
    "repository_or_industrial_scenario",
    "vulnerability_repair_scenario",
    "active_leakage_control_confirmed",
    "additional_validation_confirmed",
    "independent_validation_confirmed_lower_bound",
    "correctness_threat_confirmed_lower_bound",
    "generalization_threat_confirmed_lower_bound",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def yes(row: dict[str, str], field: str) -> bool:
    return row[field] == "yes"


def bh_adjust(values: list[float]) -> list[float]:
    count = len(values)
    order = sorted(range(count), key=values.__getitem__)
    adjusted = [1.0] * count
    running = 1.0
    for reverse_rank, index in enumerate(reversed(order), start=1):
        rank = count - reverse_rank + 1
        running = min(running, values[index] * count / rank)
        adjusted[index] = min(1.0, running)
    return adjusted


def fmt_or(value: float) -> str:
    return "inf" if math.isinf(value) else f"{value:.3f}"


def fmt_probability(value: float) -> str:
    return f"{value:.8g}"


def fisher_exact_two_sided(a: int, b: int, c: int, d: int) -> tuple[float, float]:
    """Return the odds ratio and two-sided Fisher exact p-value for a 2x2 table."""
    row_1 = a + b
    column_1 = a + c
    total = a + b + c + d
    denominator = math.comb(total, row_1)

    def probability(value: int) -> float:
        return (
            math.comb(column_1, value)
            * math.comb(total - column_1, row_1 - value)
            / denominator
        )

    observed_probability = probability(a)
    lower = max(0, row_1 - (total - column_1))
    upper = min(row_1, column_1)
    p_value = sum(
        probability(value)
        for value in range(lower, upper + 1)
        if probability(value) <= observed_probability * (1.0 + 1e-12)
    )
    if b * c:
        odds_ratio = (a * d) / (b * c)
    elif a * d:
        odds_ratio = math.inf
    else:
        odds_ratio = math.nan
    return odds_ratio, min(1.0, p_value)


def compute_test_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    test_rows: list[dict[str, object]] = []
    p_values: list[float] = []
    for tag in TAGS:
        for outcome in OUTCOMES:
            both = sum(yes(row, tag) and yes(row, outcome) for row in rows)
            tag_only = sum(yes(row, tag) and not yes(row, outcome) for row in rows)
            outcome_only = sum(not yes(row, tag) and yes(row, outcome) for row in rows)
            neither = sum(not yes(row, tag) and not yes(row, outcome) for row in rows)
            odds, p_value = fisher_exact_two_sided(both, tag_only, outcome_only, neither)
            test_rows.append(
                {
                    "tag": tag,
                    "outcome": outcome,
                    "table": f"{both}/{tag_only} vs {outcome_only}/{neither}",
                    "odds_ratio": fmt_or(odds),
                    "fisher_p_value": fmt_probability(p_value),
                    "bh_q_value": "",
                    "caveat": "Exploratory and non-causal; tags, paradigm, scenario, task, and year are confounded.",
                }
            )
            p_values.append(p_value)
    for row, q_value in zip(test_rows, bh_adjust(p_values)):
        row["bh_q_value"] = fmt_probability(q_value)
    test_rows.sort(key=lambda row: float(row["fisher_p_value"]))
    return test_rows


def main() -> None:
    taxonomy_rows = read_csv(TAXONOMY)
    scenario_rows = read_csv(SCENARIOS)
    assurance_rows = read_csv(ASSURANCE)
    taxonomy = {row["system"]: row for row in taxonomy_rows}
    scenarios = {row["system"]: row for row in scenario_rows}
    assurance = {row["system"]: row for row in assurance_rows}
    if (
        len(taxonomy_rows) != 66
        or len(scenario_rows) != 66
        or len(assurance_rows) != 66
        or len(taxonomy) != 66
        or len(scenarios) != 66
        or len(assurance) != 66
        or set(taxonomy) != set(scenarios)
        or set(taxonomy) != set(assurance)
    ):
        raise RuntimeError("Auxiliary audit requires three aligned 66-system inputs")
    scenario_mismatches = [
        system
        for system, row in taxonomy.items()
        if row["final_deployment_scenario"] != scenarios[system]["deployment_scenario"]
    ]
    if scenario_mismatches:
        raise RuntimeError(
            "Final taxonomy scenarios do not match scenario_assignment_audit.csv: "
            f"{scenario_mismatches}"
        )

    retrieval_disagreements = [
        system
        for system, row in taxonomy.items()
        if row["coder_1_retrieval_tag"] != row["coder_2_retrieval_tag"]
    ]
    analysis_disagreements = [
        system
        for system, row in taxonomy.items()
        if row["coder_1_analysis_tag"] != row["coder_2_analysis_tag"]
    ]
    scenario_disagreements = [
        system
        for system, row in taxonomy.items()
        if row["coder_1_deployment_scenario"] != row["coder_2_deployment_scenario"]
    ]
    if retrieval_disagreements or analysis_disagreements or scenario_disagreements:
        raise RuntimeError(
            "Independent taxonomy fields do not agree: "
            f"retrieval={retrieval_disagreements}, analysis={analysis_disagreements}, "
            f"scenario={scenario_disagreements}"
        )
    final_retrieval_updates = [
        system
        for system, row in taxonomy.items()
        if row["final_retrieval_tag"] != row["coder_1_retrieval_tag"]
    ]
    final_analysis_updates = [
        system
        for system, row in taxonomy.items()
        if row["final_analysis_tag"] != row["coder_1_analysis_tag"]
    ]
    if final_retrieval_updates != ["PailGen"] or final_analysis_updates:
        raise RuntimeError(
            "Final auxiliary-tag adjudications changed: "
            f"retrieval={final_retrieval_updates}, analysis={final_analysis_updates}"
        )

    output: list[dict[str, str]] = []
    for system in sorted(taxonomy):
        tax = taxonomy[system]
        assurance_row = assurance[system]
        retrieval = tax["final_retrieval_tag"] == "yes"
        analysis = tax["final_analysis_tag"] == "yes"
        scenario = tax["final_deployment_scenario"]
        output.append(
            {
                "system": system,
                "display_paradigm": tax["final_display_paradigm"],
                "deployment_scenario": scenario,
                "retrieval_tag": "yes" if retrieval else "no",
                "analysis_tag": "yes" if analysis else "no",
                "retrieval_or_analysis_tag": "yes" if retrieval or analysis else "no",
                "repository_or_industrial_scenario": (
                    "yes"
                    if scenario
                    in {"Repository-level issue resolution", "Industrial / practitioner workflow"}
                    else "no"
                ),
                "vulnerability_repair_scenario": (
                    "yes" if scenario == "Vulnerability repair" else "no"
                ),
                "active_leakage_control_confirmed": assurance_row[
                    "active_leakage_control_confirmed"
                ],
                "additional_validation_confirmed": assurance_row[
                    "additional_validation_confirmed"
                ],
                "independent_validation_confirmed_lower_bound": assurance_row[
                    "independent_validation_confirmed_lower_bound"
                ],
                "correctness_threat_confirmed_lower_bound": assurance_row[
                    "correctness_threat_confirmed_lower_bound"
                ],
                "generalization_threat_confirmed_lower_bound": assurance_row[
                    "generalization_threat_confirmed_lower_bound"
                ],
            }
        )
    write_csv(BY_SYSTEM, output)

    summary_rows: list[dict[str, object]] = []
    for tag in TAGS:
        count = sum(yes(row, tag) for row in output)
        summary_rows.append(
            {
                "scope": "all_systems",
                "group": "all",
                "signal": tag,
                "count": count,
                "denominator": 66,
                "percent": f"{100 * count / 66:.1f}%",
            }
        )
    for paradigm in ("Fine-Tuning", "Prompting", "Procedural", "Agentic"):
        subset = [row for row in output if row["display_paradigm"] == paradigm]
        for tag in TAGS:
            count = sum(yes(row, tag) for row in subset)
            summary_rows.append(
                {
                    "scope": "by_paradigm",
                    "group": paradigm,
                    "signal": tag,
                    "count": count,
                    "denominator": len(subset),
                    "percent": f"{100 * count / len(subset):.1f}%",
                }
            )
    for scenario in sorted({row["deployment_scenario"] for row in output}):
        subset = [row for row in output if row["deployment_scenario"] == scenario]
        for tag in TAGS:
            count = sum(yes(row, tag) for row in subset)
            summary_rows.append(
                {
                    "scope": "by_scenario",
                    "group": scenario,
                    "signal": tag,
                    "count": count,
                    "denominator": len(subset),
                    "percent": f"{100 * count / len(subset):.1f}%",
                }
            )
    write_csv(SUMMARY, summary_rows)

    test_rows = compute_test_rows(output)
    expected_lead_test = {
        "tag": "retrieval_tag",
        "outcome": "repository_or_industrial_scenario",
        "table": "15/14 vs 1/36",
        "odds_ratio": "38.571",
        "fisher_p_value": "3.4340276e-06",
        "bh_q_value": "7.2114579e-05",
    }
    observed_lead_test = {
        key: test_rows[0][key] for key in expected_lead_test
    }
    if len(test_rows) != 21 or observed_lead_test != expected_lead_test:
        raise RuntimeError(
            "Auxiliary-evidence test family changed: expected 21 tests with "
            "retrieval x repository/industrial as rank 1; found "
            f"{len(test_rows)} tests and {observed_lead_test}"
        )

    final_scenario_updates = sum(
        row["final_deployment_scenario"] != row["coder_1_deployment_scenario"]
        for row in taxonomy_rows
    )
    raw_scenario_output: list[dict[str, str]] = []
    for row in output:
        sensitivity_row = dict(row)
        raw_taxonomy = taxonomy[row["system"]]
        raw_retrieval = raw_taxonomy["coder_1_retrieval_tag"] == "yes"
        raw_analysis = raw_taxonomy["coder_1_analysis_tag"] == "yes"
        sensitivity_row["retrieval_tag"] = "yes" if raw_retrieval else "no"
        sensitivity_row["analysis_tag"] = "yes" if raw_analysis else "no"
        sensitivity_row["retrieval_or_analysis_tag"] = (
            "yes" if raw_retrieval or raw_analysis else "no"
        )
        raw_scenario = raw_taxonomy["coder_1_deployment_scenario"]
        sensitivity_row["repository_or_industrial_scenario"] = (
            "yes"
            if raw_scenario
            in {"Repository-level issue resolution", "Industrial / practitioner workflow"}
            else "no"
        )
        sensitivity_row["vulnerability_repair_scenario"] = (
            "yes" if raw_scenario == "Vulnerability repair" else "no"
        )
        raw_scenario_output.append(sensitivity_row)
    raw_scenario_tests = compute_test_rows(raw_scenario_output)
    expected_raw_scenario_lead = {
        "tag": "retrieval_tag",
        "outcome": "repository_or_industrial_scenario",
        "table": "13/15 vs 1/37",
        "odds_ratio": "32.067",
        "fisher_p_value": "1.889743e-05",
        "bh_q_value": "0.00039684603",
    }
    observed_raw_scenario_lead = {
        key: raw_scenario_tests[0][key] for key in expected_raw_scenario_lead
    }
    if (
        final_scenario_updates != 10
        or len(raw_scenario_tests) != 21
        or observed_raw_scenario_lead != expected_raw_scenario_lead
    ):
        raise RuntimeError(
            "Raw-scenario sensitivity changed: expected 10 adjudicated scenario "
            f"updates and {expected_raw_scenario_lead}, found "
            f"{final_scenario_updates} and {observed_raw_scenario_lead}"
        )

    write_csv(TESTS, test_rows)

    counts = {tag: sum(yes(row, tag) for row in output) for tag in TAGS}
    raw_counts = {
        "retrieval_tag": sum(
            row["coder_1_retrieval_tag"] == "yes" for row in taxonomy_rows
        ),
        "analysis_tag": sum(
            row["coder_1_analysis_tag"] == "yes" for row in taxonomy_rows
        ),
        "retrieval_or_analysis_tag": sum(
            "yes" in (row["coder_1_retrieval_tag"], row["coder_1_analysis_tag"])
            for row in taxonomy_rows
        ),
    }
    paradigm_presence = {
        tag: sorted(
            {
                row["display_paradigm"]
                for row in output
                if yes(row, tag)
            }
        )
        for tag in TAGS
    }
    significant = [row for row in test_rows if float(row["bh_q_value"]) < 0.05]
    report_lines = [
        "# Auxiliary-evidence value audit",
        "",
        "## Provenance and prevalence",
        "",
        "The two independent coders agree on all 66 raw retrieval tags, analysis tags, and deployment-scenario recodings. The raw fields remain unchanged in `taxonomy_independent_pair_66_audit.csv`.",
        "",
        "The final auxiliary fields contain one documented update: PailGen changes from raw retrieval no/no to final_retrieval_tag=yes after a targeted full-text recheck confirmed query-time BM25 + DPR retrieval. No final analysis tag changes.",
        "",
        "The final scenario field used below matches `scenario_assignment_audit.csv`; 10 older scenario labels were updated by the separate three-coder/full-text adjudication documented in `taxonomy_sensitivity_audit.md`. These fields cover only retrieval/RAG and program-analysis evidence; they do not exhaust test, human, or domain-knowledge context.",
        "",
        "The five assurance outcomes are conservative second-pass lower-bound codings from `evaluation_assurance_corrected_by_system.csv`. They are not claimed to have independent-coder agreement and should not be read as an exhaustive audit of every assurance mechanism.",
        "",
        f"- Final retrieval tag: {counts['retrieval_tag']}/66 (raw pair: {raw_counts['retrieval_tag']}/66).",
        f"- Final analysis tag: {counts['analysis_tag']}/66 (raw pair: {raw_counts['analysis_tag']}/66).",
        f"- Final retrieval or analysis: {counts['retrieval_or_analysis_tag']}/66 (raw pair: {raw_counts['retrieval_or_analysis_tag']}/66).",
        f"- Retrieval appears in: {', '.join(paradigm_presence['retrieval_tag'])}.",
        f"- Analysis appears in: {', '.join(paradigm_presence['analysis_tag'])}.",
        "",
        "## Association audit",
        "",
        "The explicitly defined exploratory family is the Cartesian product of three auxiliary signals (retrieval, analysis, and their union) and seven outcomes (two deployment scenarios plus five assurance indicators), yielding 3 x 7 = 21 tests. All 21 tests are emitted before sorting and Benjamini-Hochberg correction.",
        "",
        "The primary retrieval-by-repository/industrial table (15/29 versus 1/37) uses the final adjudicated retrieval and deployment-scenario labels. Its BH-adjusted q-value is specific to this explicitly defined 21-test exploratory family.",
        "",
        "As a sensitivity check, replacing both final retrieval/scenario labels with the untouched raw independent-pair recodings leaves the same association as rank 1 (13/28 versus 1/38, OR=32.067, p=1.889743e-05, BH q=0.00039684603). Thus, the direction and corrected significance do not depend on the PailGen retrieval correction or the 10 scenario adjudications.",
        "",
    ]
    if significant:
        report_lines.append("Associations surviving BH correction:")
        report_lines.append("")
        for row in significant:
            report_lines.append(
                f"- {row['tag']} vs {row['outcome']}: {row['table']}, "
                f"OR={row['odds_ratio']}, p={row['fisher_p_value']}, q={row['bh_q_value']}."
            )
    else:
        report_lines.append(
            "No tested association between retrieval/analysis tags and deployment or assurance outcomes survives BH correction."
        )
    report_lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "The tags are useful as an orthogonal descriptive codebook because they preserve cross-cutting design information across display paradigms. This audit does not establish that a retrieval or analysis tag by itself improves repair quality, generalization, or evaluation rigor. The manuscript should therefore demonstrate their value through concrete mechanism-level examples or trade-offs, not by treating tag prevalence as an outcome.",
        ]
    )
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Wrote {BY_SYSTEM.name} ({len(output)} rows)")
    print(f"Wrote {SUMMARY.name} ({len(summary_rows)} rows)")
    print(f"Wrote {TESTS.name} ({len(test_rows)} rows)")
    print(f"significant_after_bh={len(significant)}")
    print(f"paradigms={Counter(row['display_paradigm'] for row in output)}")


if __name__ == "__main__":
    main()
