#!/usr/bin/env python3
"""Verify the minor-revision taxonomy and statistical artifact supplement."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "minor_revision_artifact_verification.md"

REQUIRED_FILES = (
    "protocol_comparability_attrition.csv",
    "protocol_comparability_pairwise.csv",
    "protocol_comparability_evidence.md",
    "auxiliary_evidence_value_by_system.csv",
    "auxiliary_evidence_value_tests.csv",
    "auxiliary_evidence_value_audit.md",
)

EXPECTED_PARADIGMS = {
    "Fine-Tuning": 21,
    "Prompting": 17,
    "Procedural": 15,
    "Agentic": 13,
}
EXPECTED_SUBTYPES = {
    "Full Tuning",
    "Adapter Tuning",
    "Knowledge Distillation",
    "RL Tuning",
    "Zero-shot",
    "Few-shot",
    "Zero-/few-shot",
    "Test-Feedback Loop",
    "Human-in-the-Loop",
    "Scripted Tool Loop",
    "Tool-Augmented Agent",
    "LLM-Gated Review",
    "Self-Controlled System",
}
LEGACY_SUBTYPES = {
    "Full Fine-Tuning",
    "PEFT",
    "RLFT",
    "Zero-Shot",
    "Few-Shot",
    "Zero-/Few-Shot",
    "Test-in-the-Loop",
    "Tool-Augmented",
    "LLM-as-Judges",
}
TAGS = {"retrieval_tag", "analysis_tag", "retrieval_or_analysis_tag"}
OUTCOMES = {
    "repository_or_industrial_scenario",
    "vulnerability_repair_scenario",
    "active_leakage_control_confirmed",
    "additional_validation_confirmed",
    "independent_validation_confirmed_lower_bound",
    "correctness_threat_confirmed_lower_bound",
    "generalization_threat_confirmed_lower_bound",
}
JUDGE_SYSTEMS = {"Abstain and Validate", "TSAPR", "SpecRover"}


def read_csv(name: str) -> list[dict[str, str]]:
    path = ROOT / name
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    failures: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    for name in REQUIRED_FILES:
        path = ROOT / name
        require(path.is_file() and path.stat().st_size > 0, f"missing or empty: {name}")

    assignments = read_csv("taxonomy_assignment_audit.csv")
    assignment_by_system = {row["system"]: row for row in assignments}
    require(len(assignments) == len(assignment_by_system) == 66, "taxonomy assignment must contain 66 unique systems")
    require(
        Counter(row["display_paradigm"] for row in assignments) == Counter(EXPECTED_PARADIGMS),
        "display-paradigm counts changed",
    )
    observed_subtypes = {row["control_subtype"] for row in assignments}
    require(observed_subtypes == EXPECTED_SUBTYPES, f"current subtype vocabulary changed: {sorted(observed_subtypes)}")
    require(not observed_subtypes & LEGACY_SUBTYPES, "legacy subtype labels remain in taxonomy assignment")

    reaudited = {
        row["system"]
        for row in assignments
        if row.get("classification_reaudit", "").strip()
    }
    require(reaudited == JUDGE_SYSTEMS, f"focused judge re-audit rows changed: {sorted(reaudited)}")
    for system in JUDGE_SYSTEMS:
        row = assignment_by_system.get(system, {})
        require(row.get("control_subtype") == "LLM-Gated Review", f"{system} is not LLM-Gated Review")
        require("gates" in row.get("classification_reaudit", ""), f"{system} lacks explicit gate evidence")

    taxonomy = read_csv("taxonomy_independent_pair_66_audit.csv")
    taxonomy_by_system = {row["system"]: row for row in taxonomy}
    require(len(taxonomy) == len(taxonomy_by_system) == 66, "independent taxonomy must contain 66 unique systems")
    require(set(taxonomy_by_system) == set(assignment_by_system), "taxonomy sheets do not cover the same systems")
    require(
        Counter(row["final_display_paradigm"] for row in taxonomy) == Counter(EXPECTED_PARADIGMS),
        "independent-taxonomy paradigm counts changed",
    )
    for field_1, field_2, label in (
        ("coder_1_retrieval_tag", "coder_2_retrieval_tag", "retrieval"),
        ("coder_1_analysis_tag", "coder_2_analysis_tag", "analysis"),
        ("coder_1_deployment_scenario", "coder_2_deployment_scenario", "deployment scenario"),
    ):
        require(all(row[field_1] == row[field_2] for row in taxonomy), f"independent coders disagree on {label}")

    scenarios = read_csv("scenario_assignment_audit.csv")
    scenario_by_system = {row["system"]: row for row in scenarios}
    require(len(scenarios) == len(scenario_by_system) == 66, "scenario audit must contain 66 unique systems")
    require(set(scenario_by_system) == set(taxonomy_by_system), "scenario and taxonomy systems do not align")
    require(
        all(
            row["final_deployment_scenario"]
            == scenario_by_system[row["system"]]["deployment_scenario"]
            for row in taxonomy
        ),
        "final taxonomy scenarios do not match scenario_assignment_audit.csv",
    )
    final_scenario_updates = sum(
        row["final_deployment_scenario"] != row["coder_1_deployment_scenario"]
        for row in taxonomy
    )
    require(
        final_scenario_updates == 10,
        f"scenario adjudication count changed to {final_scenario_updates}",
    )

    pailgen = taxonomy_by_system.get("PailGen", {})
    require(
        pailgen.get("coder_1_retrieval_tag")
        == pailgen.get("coder_2_retrieval_tag")
        == "no"
        and pailgen.get("final_retrieval_tag") == "yes",
        "PailGen raw/final retrieval provenance is inconsistent",
    )
    require(
        "BM25 + DPR" in pailgen.get("adjudication_note", ""),
        "PailGen retrieval correction lacks its full-text evidence note",
    )
    final_retrieval_updates = {
        row["system"]
        for row in taxonomy
        if row["final_retrieval_tag"] != row["coder_1_retrieval_tag"]
    }
    final_analysis_updates = {
        row["system"]
        for row in taxonomy
        if row["final_analysis_tag"] != row["coder_1_analysis_tag"]
    }
    require(final_retrieval_updates == {"PailGen"}, f"final retrieval updates changed: {sorted(final_retrieval_updates)}")
    require(not final_analysis_updates, f"final analysis updates changed: {sorted(final_analysis_updates)}")

    retrieval = {
        row["system"] for row in taxonomy if row["final_retrieval_tag"] == "yes"
    }
    raw_retrieval = {
        row["system"] for row in taxonomy if row["coder_1_retrieval_tag"] == "yes"
    }
    analysis = {
        row["system"] for row in taxonomy if row["final_analysis_tag"] == "yes"
    }
    require(len(retrieval) == 29, f"final retrieval count changed to {len(retrieval)}")
    raw_analysis = {
        row["system"] for row in taxonomy if row["coder_1_analysis_tag"] == "yes"
    }
    require(len(raw_retrieval) == 28, f"raw retrieval count changed to {len(raw_retrieval)}")
    require(len(analysis) == len(raw_analysis) == 59, "final/raw analysis count changed")
    require(len(retrieval | analysis) == 63, "final retrieval/analysis union count changed")
    require(len(raw_retrieval | raw_analysis) == 62, "raw retrieval/analysis union count changed")

    broad_scenarios = {
        "Repository-level issue resolution",
        "Industrial / practitioner workflow",
    }
    primary_table = (
        sum(row["system"] in retrieval and row["final_deployment_scenario"] in broad_scenarios for row in taxonomy),
        sum(row["system"] in retrieval and row["final_deployment_scenario"] not in broad_scenarios for row in taxonomy),
        sum(row["system"] not in retrieval and row["final_deployment_scenario"] in broad_scenarios for row in taxonomy),
        sum(row["system"] not in retrieval and row["final_deployment_scenario"] not in broad_scenarios for row in taxonomy),
    )
    require(primary_table == (15, 14, 1, 36), f"primary retrieval/scenario table changed to {primary_table}")
    raw_scenario_table = (
        sum(row["system"] in raw_retrieval and row["coder_1_deployment_scenario"] in broad_scenarios for row in taxonomy),
        sum(row["system"] in raw_retrieval and row["coder_1_deployment_scenario"] not in broad_scenarios for row in taxonomy),
        sum(row["system"] not in raw_retrieval and row["coder_1_deployment_scenario"] in broad_scenarios for row in taxonomy),
        sum(row["system"] not in raw_retrieval and row["coder_1_deployment_scenario"] not in broad_scenarios for row in taxonomy),
    )
    require(
        raw_scenario_table == (13, 15, 1, 37),
        f"raw-scenario sensitivity table changed to {raw_scenario_table}",
    )

    auxiliary = read_csv("auxiliary_evidence_value_by_system.csv")
    auxiliary_by_system = {row["system"]: row for row in auxiliary}
    require(len(auxiliary) == len(auxiliary_by_system) == 66, "auxiliary system table must contain 66 unique systems")
    require(set(auxiliary_by_system) == set(taxonomy_by_system), "auxiliary and taxonomy systems do not align")
    for system, row in auxiliary_by_system.items():
        tax = taxonomy_by_system[system]
        require(row["retrieval_tag"] == tax["final_retrieval_tag"], f"{system}: retrieval tag drift")
        require(row["analysis_tag"] == tax["final_analysis_tag"], f"{system}: analysis tag drift")
        require(row["deployment_scenario"] == tax["final_deployment_scenario"], f"{system}: scenario drift")

    assurance = read_csv("evaluation_assurance_corrected_by_system.csv")
    assurance_by_system = {row["system"]: row for row in assurance}
    require(len(assurance) == len(assurance_by_system) == 66, "assurance table must contain 66 unique systems")
    require(set(assurance_by_system) == set(taxonomy_by_system), "assurance and taxonomy systems do not align")
    for field in OUTCOMES - {"repository_or_industrial_scenario", "vulnerability_repair_scenario"}:
        require(all(row[field] in {"yes", "no"} for row in assurance), f"non-binary assurance field: {field}")

    tests = read_csv("auxiliary_evidence_value_tests.csv")
    observed_family = {(row["tag"], row["outcome"]) for row in tests}
    require(len(tests) == len(observed_family) == 21, "auxiliary test family must contain 21 unique tests")
    require(observed_family == {(tag, outcome) for tag in TAGS for outcome in OUTCOMES}, "auxiliary test family is not the documented 3 x 7 product")
    lead = [
        row for row in tests
        if row["tag"] == "retrieval_tag"
        and row["outcome"] == "repository_or_industrial_scenario"
    ]
    require(len(lead) == 1, "primary auxiliary test is missing or duplicated")
    if lead:
        row = lead[0]
        require(row["table"] == "15/14 vs 1/36", "primary auxiliary test table changed")
        require(abs(float(row["odds_ratio"]) - 38.571) < 0.001, "primary odds ratio changed")
        require(abs(float(row["fisher_p_value"]) - 3.4340276e-06) < 1e-12, "primary Fisher p-value changed")
        require(abs(float(row["bh_q_value"]) - 7.2114579e-05) < 1e-12, "primary BH q-value changed")
    require(
        sum(float(row["bh_q_value"]) < 0.05 for row in tests) == 1,
        "the number of BH-significant auxiliary tests is not one",
    )

    attrition = read_csv("protocol_comparability_attrition.csv")
    attrition_lookup = {(row["scope"], row["measure"]): int(row["count"]) for row in attrition}
    expected_attrition = {
        ("all_system_pairs", "all possible pairs among 66 systems"): 2145,
        ("same_benchmark_pairs", "pairs sharing the exact recorded benchmark label"): 100,
        ("same_benchmark_pairs", "pairs retained in a protocol-aligned comparison window"): 32,
        ("sequential_attrition", "protocol-aligned pairs also sharing a normalized base model"): 4,
        ("sequential_attrition", "same-model aligned pairs meeting the model-controlled definition"): 1,
    }
    for key, value in expected_attrition.items():
        require(attrition_lookup.get(key) == value, f"protocol attrition changed for {key}: {attrition_lookup.get(key)}")

    pairs = read_csv("protocol_comparability_pairwise.csv")
    require(len(pairs) == 100, f"same-benchmark pair table changed to {len(pairs)} rows")
    model_controlled = [
        row for row in pairs
        if row["protocol_aligned_window"] == "yes"
        and row["same_normalized_base_model"] == "yes"
        and row["comparability_tier"] == "A_model_controlled_comparison"
    ]
    require(len(model_controlled) == 1, f"model-controlled pair count changed to {len(model_controlled)}")
    if model_controlled:
        pair = model_controlled[0]
        require(
            {pair["system_a"], pair["system_b"]} == {"MORepair", "Luo et al."}
            and pair["benchmark"] == "EvalRepair-Java",
            f"model-controlled pair changed: {pair}",
        )

    status_text = (ROOT / "version_status_audit.md").read_text(encoding="utf-8")
    try:
        arxiv_section = status_text.split("## Retained as arXiv in the current bibliography", 1)[1]
        arxiv_list = arxiv_section.split("Two retained systems have archival venue hints", 1)[0]
        arxiv_count = sum(line.startswith("- `") for line in arxiv_list.splitlines())
    except IndexError:
        arxiv_count = -1
    require(arxiv_count == 9, f"retained arXiv enumeration changed to {arxiv_count}")

    status = "PASS" if not failures else "FAIL"
    lines = [
        "# Minor-revision artifact verification",
        "",
        f"**Status:** {status}",
        "",
        "## Checked",
        "",
        "- Six response-letter artifact files exist and are non-empty.",
        "- The 66-system paradigm counts remain 21/17/15/13.",
        "- Current subtype terminology is synchronized, and exactly three LLM-Gated Review systems carry focused gate evidence.",
        "- Independent retrieval, analysis, and raw deployment-scenario labels agree for all 66 systems; final scenario labels match the separate adjudicated scenario audit.",
        "- Raw auxiliary labels are preserved; PailGen is the sole final retrieval update after the documented BM25 + DPR full-text recheck.",
        "- Final retrieval/analysis/union prevalence is 29/59/63 (raw: 28/59/62); final proportions are 15/29 versus 1/37, while the untouched raw-label sensitivity is 13/28 versus 1/38.",
        "- The complete 3 x 7 test family has 21 unique tests; only the primary retrieval/scenario association survives BH correction.",
        "- Protocol comparability reproduces 2,145 -> 100 -> 32 -> 4 -> 1, with MORepair versus Luo et al. as the sole model-controlled pair.",
        "- The version-status audit enumerates nine retained arXiv records.",
        "",
        "## Failures",
        "",
    ]
    lines.extend(f"- {failure}" for failure in failures)
    if not failures:
        lines.append("- None.")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"status={status}")
    print(f"failures={len(failures)}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
