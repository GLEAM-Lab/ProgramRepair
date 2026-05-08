#!/usr/bin/env python3
"""Build benchmark comparability artifacts from the 66-system audit sheet.

The goal is deliberately conservative: identify small protocol-aligned
comparison windows, and mark all other rows as protocol snapshots rather than
leaderboard entries.
"""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "taxonomy_assignment_audit.csv"
BY_SYSTEM = ROOT / "benchmark_protocol_comparability_by_system.csv"
WINDOWS = ROOT / "benchmark_protocol_comparability_windows.csv"
GROUPS = ROOT / "benchmark_protocol_coverage_groups.csv"
PASSK_BY_YEAR = ROOT / "benchmark_passk_distribution_by_year.csv"
PASSK_BY_K = ROOT / "benchmark_passk_distribution_by_k.csv"
REPORT = ROOT / "benchmark_protocol_comparability.md"


# Publication years are taken from screening_reference_labels_474.csv. The
# benchmark audit sheet uses system names rather than paper titles, so this map
# keeps the benchmark metric analysis aligned with the final 66-system corpus.
SYSTEM_YEAR = {
    "Huang et al.": 2023,
    "Jiang et al.": 2023,
    "VulMaster": 2024,
    "RepairCAT": 2024,
    "RepairLLaMA": 2025,
    "MORepair": 2025,
    "Luo et al.": 2025,
    "Li et al.": 2024,
    "Ruiz et al.": 2025,
    "KNOD": 2023,
    "DistiLRR": 2025,
    "NARRepair": 2024,
    "RePair": 2024,
    "SecRepair": 2024,
    "SWE-RL": 2025,
    "AdaPatcher": 2025,
    "Vul-R2": 2025,
    "TraceFixer": 2023,
    "InferFix": 2023,
    "PyTy": 2024,
    "NTR": 2025,
    "AlphaRepair": 2022,
    "Prenner et al.": 2022,
    "Fan et al.": 2023,
    "Tian et al.": 2023,
    "Xia et al.": 2023,
    "Gao et al.": 2023,
    "Ahmed et al.": 2023,
    "CEDAR": 2023,
    "Ehsani et al.": 2025,
    "RLCE": 2024,
    "DsRepair": 2025,
    "D4C": 2025,
    "Appatch": 2025,
    "TracePrompt": 2025,
    "ChatRepair": 2024,
    "ThinkRepair": 2024,
    "REx": 2024,
    "ContrastRepair": 2025,
    "CREF": 2024,
    "HULA": 2025,
    "DRCodePilot": 2024,
    "Agentless": 2025,
    "PATCH": 2025,
    "KGCompass": 2025,
    "Repilot": 2023,
    "SAN2PATCH": 2025,
    "PredicateFix": 2026,
    "LLM4CVE": 2025,
    "SWE-Agent": 2024,
    "SWE-Agent M": 2025,
    "OpenHands": 2025,
    "AutoCodeRover": 2024,
    "RepairAgent": 2025,
    "LANTERN": 2026,
    "VulDebugger": 2025,
    "Abstain and Validate": 2026,
    "TSAPR": 2025,
    "SpecRover": 2025,
    "MAGIS": 2024,
    "SWE-Search": 2025,
    "Learn-by-Interact": 2025,
    "PailGen": 2026,
    "ACFix": 2025,
    "Dr.Fix": 2026,
    "IntDiagSolver": 2026,
}


def norm_model(value: str) -> str:
    text = (value or "").strip().lower().replace("-", " ")
    text = re.sub(r"\s+", " ", text)
    if "claude" in text and "3.5" in text and "sonnet" in text:
        return "Claude 3.5 Sonnet"
    if "deepseek" in text and "coder" in text and "7b" in text:
        return "DeepSeek-Coder 7B"
    if "codellama" in text and "13b" in text:
        return "CodeLlama 13B"
    if "codellama" in text and "7b" in text:
        return "CodeLlama 7B"
    if "gpt 4o" in text or "gpt-4o" in text:
        return "GPT-4o"
    if "gpt 4 turbo" in text or "gpt-4 turbo" in text:
        return "GPT-4 Turbo"
    if text == "gpt 4" or text == "gpt-4":
        return "GPT-4"
    return (value or "").strip()


def assumption_bucket(value: str) -> str:
    text = (value or "").lower()
    buckets: list[str] = []
    if "perfect fault" in text:
        buckets.append("Perfect FL")
    if "single-function" in text:
        buckets.append("single-function")
    if "single-hunk" in text:
        buckets.append("single-hunk")
    if "train/test split" in text:
        buckets.append("train/test split")
    if "human" in text or "tutor" in text:
        buckets.append("human feedback")
    if "verified" in text or "execution validation" in text:
        buckets.append("explicit validation")
    if not buckets:
        buckets.append("not explicitly narrowed")
    return "; ".join(buckets)


def result_percent(value: str) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    frac = re.fullmatch(r"([0-9.]+)\s*/\s*([0-9.]+)", text)
    if frac:
        num = float(frac.group(1))
        den = float(frac.group(2))
        if den:
            return f"{100 * num / den:.2f}"
    pct = re.search(r"([+-]?[0-9.]+)\s*%", text)
    if pct:
        return f"{float(pct.group(1)):.2f}"
    num = re.fullmatch(r"([0-9.]+)", text)
    if num:
        return f"{float(num.group(1)):.2f}"
    return ""


def metric_family(value: str) -> str:
    text = (value or "").strip().lower()
    if re.search(r"pass@\s*1\b", text):
        return "pass@1"
    if re.search(r"pass@\s*5\b", text):
        return "pass@5"
    if re.search(r"pass@\s*10\b", text):
        return "pass@10"
    if re.search(r"pass@\s*\d+", text):
        return "other pass@k"
    if re.search(r"(top@k|accept@1)", text):
        return "single-candidate non-pass@k"
    return "non-pass@k"


def pct_range(rows: list[dict[str, str]]) -> str:
    vals = []
    for row in rows:
        pct = row.get("result_percent", "")
        if pct:
            vals.append(float(pct))
    if not vals:
        return "not normalized"
    return f"{min(vals):.2f}--{max(vals):.2f}%"


def system_list(rows: list[dict[str, str]]) -> str:
    def key(row: dict[str, str]) -> tuple[int, float, str]:
        pct = row.get("result_percent", "")
        if pct:
            return (0, float(pct), row["system"])
        return (1, 0.0, row["system"])

    return "; ".join(f"{r['system']} ({r['result']})" for r in sorted(rows, key=key))


def short_system_list(rows: list[dict[str, str]]) -> str:
    return "; ".join(f"{r['system']} ({r['metric']} {r['result']})" for r in rows)


def coverage_group(row: dict[str, str]) -> str:
    family = row["benchmark_family"]
    benchmark = row["benchmark"]
    metric = row["metric"]
    assumption = row["assumption"]
    system = row["system"]

    if family == "Defects4J":
        if "Perfect Fault Localization" in assumption:
            return "G1_Defects4J_PerfectFL_or_function_level"
        if "single-function" in assumption:
            return "G2_Defects4J_single_function"
        if system in {"RepairAgent", "TSAPR"}:
            return "G3_Defects4J_tool_or_search_no_explicit_FL"
        if "single-hunk" in assumption:
            return "G4_Defects4J_single_hunk"
        return "G5_Defects4J_other"

    if benchmark == "HumanEval-Java":
        if metric == "pass@10":
            return "G6_HumanEvalJava_pass10"
        return "G7_HumanEvalJava_other_metrics"

    if benchmark == "SWE-bench Lite" and metric == "pass@1":
        return "G8_SWEBench_Lite_pass1"
    if family in {"SWE-bench Verified", "SWE-bench Other"}:
        return "G9_SWEBench_other_variants"

    if family in {"Vulnerability repair datasets", "API misuse repair", "Crash bug repair"}:
        return "G10_security_api_crash_fragmented"

    return "G11_other_task_specific_or_singleton_benchmarks"


def assign_windows(row: dict[str, str]) -> tuple[list[str], str, str]:
    family = row["benchmark_family"]
    benchmark = row["benchmark"]
    metric = row["metric"]
    model = row["normalized_base_model"]
    assumption = row["assumption_bucket"]
    system = row["system"]

    windows: list[str] = []
    tier = "D_snapshot_only"
    reason = "No protocol-aligned peer in the final 66-system audit; keep as a protocol snapshot only."

    if family == "SWE-bench Lite" and metric == "pass@1":
        windows.append("W1_SWE_BENCH_LITE_PASS1")
        tier = "B_protocol_aligned_stack_snapshot"
        reason = "Same benchmark variant and metric; comparable as whole system+model stacks, but not as isolated algorithm effects because base models and search budgets differ."
        if model == "Claude 3.5 Sonnet":
            windows.append("W1a_SWE_BENCH_LITE_CLAUDE35_PASS1")
            reason += " Also belongs to the Claude 3.5 Sonnet subwindow, where base-model family is controlled more tightly."

    if benchmark == "HumanEval-Java" and metric == "pass@10":
        windows.append("W4_HUMANEVAL_JAVA_PASS10_PEFT")
        tier = "C_limited_within_benchmark_comparison"
        reason = "Same benchmark and pass@10 metric, but base model and fault-localization reporting differ across rows."
        if model == "DeepSeek-Coder 7B" and "Perfect FL" in assumption:
            windows.append("W2_HUMANEVAL_JAVA_DEEPSEEK7B_PASS10_PERFECT_FL")
            tier = "A_model_controlled_comparison"
            reason = "Same benchmark, same pass@10 metric, same base model, and same Perfect-FL assumption; remaining differences mainly concern training data/objective and repair procedure."
        elif model == "CodeLlama 13B" and "Perfect FL" not in assumption:
            windows.append("W3_HUMANEVAL_JAVA_CODELLAMA13B_PASS10")
            tier = "A_model_controlled_comparison"
            reason = "Same benchmark, same pass@10 metric, and same base-model family; FL/oracle details are less explicit, so interpret as model-controlled but assumption-underreported."

    if family == "Defects4J":
        reason = "Defects4J rows mix benchmark versions/subsets, denominators, pass@k budgets, Perfect-FL assumptions, single-function/single-hunk settings, and repository-level execution."
    elif family in {"Vulnerability repair datasets", "API misuse repair", "Crash bug repair"}:
        reason = "Security/API/crash repair rows use disjoint datasets and metric families; they support fragmentation analysis, not cross-paper ranking."
    elif family == "SWE-bench Verified":
        reason = "Only one Verified row appears in the final audit, so it is a singleton protocol snapshot."
    elif family == "SWE-bench Other":
        reason = "Rows use different SWE-bench variants or additional environment/trajectory conditions, so they should not be merged with SWE-bench Lite pass@1."
    elif family == "Other":
        reason = "Rows use smaller or domain-specific datasets; apparent metric matches can occur across different benchmarks and should not be ranked."

    return windows, tier, reason


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def latex_escape(text: str) -> str:
    return (
        text.replace("\\", "\\textbackslash{}")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("_", "\\_")
    )


def main() -> None:
    rows = list(csv.DictReader(INPUT.open(newline="")))
    enriched: list[dict[str, str]] = []
    for row in rows:
        row = dict(row)
        row["year"] = str(SYSTEM_YEAR[row["system"]])
        row["normalized_base_model"] = norm_model(row["base_model"])
        row["assumption_bucket"] = assumption_bucket(row["assumption"])
        row["result_percent"] = result_percent(row["result"])
        row["metric_family"] = metric_family(row["metric"])
        windows, tier, reason = assign_windows(row)
        row["comparison_windows"] = "; ".join(windows) if windows else "None"
        row["comparability_tier"] = tier
        row["comparability_reason"] = reason
        row["coverage_group"] = coverage_group(row)
        enriched.append(row)

    write_csv(
        BY_SYSTEM,
        enriched,
        [
            "system",
            "year",
            "display_paradigm",
            "control_subtype",
            "benchmark_family",
            "benchmark",
            "metric",
            "result",
            "result_percent",
            "base_model",
            "normalized_base_model",
            "assumption",
            "assumption_bucket",
            "comparison_windows",
            "coverage_group",
            "comparability_tier",
            "comparability_reason",
            "metric_family",
        ],
    )

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in enriched:
        for window in row["comparison_windows"].split("; "):
            if window != "None":
                groups[window].append(row)

    window_meta = {
        "W1_SWE_BENCH_LITE_PASS1": (
            "B_protocol_aligned_stack_snapshot",
            "SWE-bench Lite, pass@1, repository-level issue repair.",
            "Benchmark variant and metric.",
            "Base model, cost budget, search depth, validation strategy, and publication snapshot.",
            "Whole-system stacks vary from 16.67% to 46.00%; repository context selection and search/validation design materially affect results.",
        ),
        "W1a_SWE_BENCH_LITE_CLAUDE35_PASS1": (
            "B_protocol_aligned_stack_snapshot",
            "SWE-bench Lite, pass@1, Claude 3.5 Sonnet family.",
            "Benchmark variant, metric, and base-model family.",
            "Tool interface, retrieval/search policy, validation depth, and exact model snapshot.",
            "Even under the same base-model family, reported pass@1 spans 26.00%--46.00%, supporting analysis of orchestration/context design.",
        ),
        "W2_HUMANEVAL_JAVA_DEEPSEEK7B_PASS10_PERFECT_FL": (
            "A_model_controlled_comparison",
            "HumanEval-Java, pass@10, DeepSeek-Coder 7B, Perfect FL.",
            "Benchmark, metric, base model, and FL assumption.",
            "Training data, adaptation objective, and iterative repair details.",
            "Ruiz et al. reports 78.53% versus Li et al. 68.10%, showing that training/evaluation design matters even with the same base model and FL assumption.",
        ),
        "W3_HUMANEVAL_JAVA_CODELLAMA13B_PASS10": (
            "A_model_controlled_comparison",
            "HumanEval-Java, pass@10, CodeLlama 13B.",
            "Benchmark, metric, and base-model family.",
            "FL/oracle assumptions are underreported; training objective differs.",
            "Luo et al. (76.88%) and MORepair (77.90%) are close, so this window supports only a narrow comparison of PEFT variants.",
        ),
        "W4_HUMANEVAL_JAVA_PASS10_PEFT": (
            "C_limited_within_benchmark_comparison",
            "HumanEval-Java, pass@10, PEFT-oriented systems.",
            "Benchmark and metric.",
            "Base model, training data, adaptation objective, and FL/oracle assumptions.",
            "The five pass@10 rows range from 67.28% to 78.53%; useful for a bounded discussion, not for broad paradigm ranking.",
        ),
    }

    window_rows: list[dict[str, str]] = []
    for window, members in sorted(groups.items()):
        tier, criteria, controlled, confounders, interpretation = window_meta[window]
        window_rows.append(
            {
                "window_id": window,
                "tier": tier,
                "criteria": criteria,
                "n": str(len(members)),
                "systems": system_list(members),
                "result_range": pct_range(members),
                "controlled_factors": controlled,
                "remaining_confounders": confounders,
                "supported_interpretation": interpretation,
            }
        )

    write_csv(
        WINDOWS,
        window_rows,
        [
            "window_id",
            "tier",
            "criteria",
            "n",
            "systems",
            "result_range",
            "controlled_factors",
            "remaining_confounders",
            "supported_interpretation",
        ],
    )

    coverage_meta = {
        "G1_Defects4J_PerfectFL_or_function_level": (
            "Defects4J with Perfect-FL/function-level assumptions",
            "Same benchmark family; all six rows use localized Java APR settings with Perfect-FL or comparable localized inputs.",
            "pass@1/top@k/pass@5/pass@10/pass@200/pass@1000 budgets, denominators, benchmark versions, and base models differ.",
            "Useful for showing how headline Defects4J scores depend on FL hints and sampling budget; not a direct ranking.",
        ),
        "G2_Defects4J_single_function": (
            "Defects4J single-function variants",
            "Same benchmark family and single-function scope.",
            "pass@10/pass@25/pass@500 budgets and denominators differ.",
            "Useful for comparing how much extra generation/test feedback is reported under a narrowed scope.",
        ),
        "G3_Defects4J_tool_or_search_no_explicit_FL": (
            "Defects4J tool/search systems without explicit Perfect-FL control",
            "Same broad benchmark family and GPT-3.5-class repair systems.",
            "pass@1 versus pass@16, tool autonomy, search policy, and FL assumptions differ.",
            "Useful as end-to-end or search-heavy protocol evidence, not a direct score ranking.",
        ),
        "G4_Defects4J_single_hunk": (
            "Defects4J single-hunk snapshot",
            "Same benchmark family but singleton scope.",
            "No peer with the same single-hunk protocol in the retained set.",
            "Used as evidence of subset specialization.",
        ),
        "G6_HumanEvalJava_pass10": (
            "HumanEval-Java pass@10",
            "Same benchmark and pass@10 metric.",
            "Base model, training data, PEFT objective, and FL reporting differ.",
            "Supports bounded comparison of PEFT-oriented repair systems; two smaller subwindows control base model more tightly.",
        ),
        "G7_HumanEvalJava_other_metrics": (
            "HumanEval-Java non-pass@10 rows",
            "Same benchmark.",
            "pass@100, pass@40, and accuracy are different metrics.",
            "Used to show metric heterogeneity rather than ranked against pass@10.",
        ),
        "G8_SWEBench_Lite_pass1": (
            "SWE-bench Lite pass@1",
            "Same benchmark variant and pass@1 metric.",
            "Base model, exact snapshot, cost budget, search depth, retrieval policy, and validation depth differ.",
            "Largest protocol-aligned whole-stack comparison window in the corpus.",
        ),
        "G9_SWEBench_other_variants": (
            "SWE-bench Verified, Multimodal, and full/conditioned variants",
            "Same repository-level benchmark family.",
            "Different benchmark variants and additional environment, multimodal, or trajectory conditions.",
            "Kept separate from Lite pass@1 while still contributing to repository-level protocol analysis.",
        ),
        "G10_security_api_crash_fragmented": (
            "Vulnerability, API-misuse, and crash-repair datasets",
            "Security or robustness-oriented repair tasks.",
            "Datasets and metrics are disjoint: EM, F1, CodeBLEU, success rate, repair accuracy, and pass@k.",
            "Supports the conclusion that security/API/crash repair lacks a consolidated benchmark.",
        ),
        "G11_other_task_specific_or_singleton_benchmarks": (
            "Other task-specific or singleton benchmarks",
            "Each row is retained in the corpus-level audit.",
            "The 24 rows span non-overlapping or singleton benchmarks, including APR Competition, QuixBugs, BugsInPy, RepoBugs, DS-1000, TutorCode, Flink, and Google accept@1.",
            "Used for coverage and protocol-diversity analysis, not cross-paper ranking.",
        ),
    }

    coverage_rows: list[dict[str, str]] = []
    by_group: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in enriched:
        by_group[row["coverage_group"]].append(row)

    for group_id, members in sorted(by_group.items()):
        label, shared_basis, noncomparable, interpretation = coverage_meta[group_id]
        coverage_rows.append(
            {
                "coverage_group": group_id,
                "label": label,
                "n": str(len(members)),
                "systems": short_system_list(members),
                "normalized_result_range": pct_range(members),
                "shared_basis": shared_basis,
                "noncomparable_dimensions": noncomparable,
                "safe_interpretation": interpretation,
            }
        )

    write_csv(
        GROUPS,
        coverage_rows,
        [
            "coverage_group",
            "label",
            "n",
            "systems",
            "normalized_result_range",
            "shared_basis",
            "noncomparable_dimensions",
            "safe_interpretation",
        ],
    )

    metric_cols = [
        "pass@1",
        "pass@5",
        "pass@10",
        "other pass@k",
        "single-candidate non-pass@k",
        "non-pass@k",
    ]
    by_year: dict[str, Counter[str]] = defaultdict(Counter)
    by_metric: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in enriched:
        by_year[row["year"]][row["metric_family"]] += 1
        by_year[row["year"]]["total"] += 1
        by_metric[row["metric_family"]].append(row)

    passk_year_rows = []
    for year in sorted(by_year):
        total = by_year[year]["total"]
        pass1 = by_year[year]["pass@1"]
        single_like = pass1 + by_year[year]["single-candidate non-pass@k"]
        passk_year_rows.append(
            {
                "year": year,
                "total": str(total),
                "pass@1": str(pass1),
                "pass@5": str(by_year[year]["pass@5"]),
                "pass@10": str(by_year[year]["pass@10"]),
                "other_pass@k": str(by_year[year]["other pass@k"]),
                "single_candidate_non_pass@k": str(by_year[year]["single-candidate non-pass@k"]),
                "non_pass@k": str(by_year[year]["non-pass@k"]),
                "pass@1_share": f"{100 * pass1 / total:.1f}%",
                "pass@1_or_single_candidate_share": f"{100 * single_like / total:.1f}%",
            }
        )

    write_csv(
        PASSK_BY_YEAR,
        passk_year_rows,
        [
            "year",
            "total",
            "pass@1",
            "pass@5",
            "pass@10",
            "other_pass@k",
            "single_candidate_non_pass@k",
            "non_pass@k",
            "pass@1_share",
            "pass@1_or_single_candidate_share",
        ],
    )

    passk_metric_rows = []
    for metric in metric_cols:
        members = by_metric[metric]
        passk_metric_rows.append(
            {
                "metric_family": metric,
                "n": str(len(members)),
                "systems": "; ".join(f"{row['system']} ({row['year']}, {row['metric']})" for row in members),
            }
        )
    write_csv(PASSK_BY_K, passk_metric_rows, ["metric_family", "n", "systems"])

    tier_counts = Counter(row["comparability_tier"] for row in enriched)
    family_counts = Counter(row["benchmark_family"] for row in enriched)
    metric_counts = Counter(row["metric"] for row in enriched)
    group_counts = Counter(row["coverage_group"] for row in enriched)
    snapshot_only = [row for row in enriched if row["comparability_tier"] == "D_snapshot_only"]

    report = []
    report.append("# Benchmark Protocol Comparability Analysis\n")
    report.append("Generated from `artifact/taxonomy_assignment_audit.csv`.\n")
    report.append("This audit covers all 66 retained systems. It separates bounded protocol-aligned comparison windows from same-benchmark/family coverage groups. The former can be compared only within narrow windows; the latter ensures every paper contributes to the benchmark-protocol analysis without turning heterogeneous protocols into a leaderboard.\n")
    report.append("## Coverage\n")
    report.append(f"- Rows analyzed: {len(enriched)} / 66\n")
    report.append("- Rows assigned to at least one comparison window: " + str(sum(1 for r in enriched if r["comparison_windows"] != "None")) + "\n")
    report.append("- Rows retained as snapshot-only under the bounded-window criterion: " + str(len(snapshot_only)) + "\n")
    report.append("- Rows assigned to same-benchmark/family coverage groups: " + str(sum(group_counts.values())) + " / 66\n")
    report.append("\n## Comparability tiers\n")
    for tier, count in sorted(tier_counts.items()):
        report.append(f"- `{tier}`: {count}\n")
    report.append("\n## Benchmark-family counts\n")
    for family, count in family_counts.most_common():
        report.append(f"- {family}: {count}\n")
    report.append("\n## Metric-family counts\n")
    for metric, count in metric_counts.most_common():
        report.append(f"- {metric}: {count}\n")
    report.append("\n## pass@k reporting distribution by year\n")
    for row in passk_year_rows:
        report.append(
            "- {year}: total={total}, pass@1={pass1}, pass@5={pass5}, "
            "pass@10={pass10}, other pass@k={other}, non-pass@k or related={nonpass}, "
            "pass@1 share={share}\n".format(
                year=row["year"],
                total=row["total"],
                pass1=row["pass@1"],
                pass5=row["pass@5"],
                pass10=row["pass@10"],
                other=row["other_pass@k"],
                nonpass=str(int(row["single_candidate_non_pass@k"]) + int(row["non_pass@k"])),
                share=row["pass@1_share"],
            )
        )
    report.append("\n## Protocol-aligned windows\n")
    for row in window_rows:
        report.append(f"\n### {row['window_id']}\n")
        for key in [
            "tier",
            "criteria",
            "n",
            "systems",
            "result_range",
            "controlled_factors",
            "remaining_confounders",
            "supported_interpretation",
        ]:
            report.append(f"- **{key.replace('_', ' ').title()}**: {row[key]}\n")
    report.append("\n## Same-benchmark/family protocol coverage groups\n")
    for row in coverage_rows:
        report.append(f"\n### {row['coverage_group']}: {row['label']}\n")
        for key in [
            "n",
            "systems",
            "normalized_result_range",
            "shared_basis",
            "noncomparable_dimensions",
            "safe_interpretation",
        ]:
            report.append(f"- **{key.replace('_', ' ').title()}**: {row[key]}\n")
    report.append("\n## Non-comparable families and why\n")
    report.append("- **Defects4J**: 12 rows can all be used in same-family protocol analysis. They split into Perfect-FL/function-level, single-function, tool/search, and single-hunk groups, but the rows still mix benchmark versions/subsets, denominators, pass@k budgets from 1 to 5000, and FL assumptions. A global ranking remains unsupported by the reported protocols.\n")
    report.append("- **HumanEval-Java non-pass@10 rows**: NTR uses pass@100, ContrastRepair uses pass@40, and TracePrompt reports accuracy; these should remain protocol snapshots rather than being ranked against pass@10 PEFT rows.\n")
    report.append("- **SWE-bench Verified/Other**: SWE-RL is a singleton Verified row, while SWE-Agent M and Learn-by-Interact use different SWE-bench variants or extra environment/trajectory conditions.\n")
    report.append("- **Vulnerability/API/crash repair**: rows use disjoint datasets and metric families, including exact match, F1, CodeBLEU, EM, success rate, repair accuracy, and pass@k.\n")
    report.append("- **Other benchmark family**: rows use smaller or domain-specific datasets; apparent metric matches can occur across different datasets and should not be ranked.\n")
    report.append("\n## Manuscript consistency checks\n")
    report.append("- The current SWE-bench table uses `MAGIS` for the SWE-bench Lite `pass@1: 16.67%` row and keeps `TSAPR` only in the Defects4J table, matching `taxonomy_assignment_audit.csv` and the detailed system table.\n")
    report.append("- The current Defects4J table records `KNOD` with base model `Not specified`, matching the audit value `/`.\n")
    report.append("- The current Defects4J table does not mark `TSAPR` as a Perfect-FL row, matching the final audit.\n")
    report.append("- The current fragmented security/API table uses `EM` for `PailGen` and `Dr.Fix`, and records `Dr.Fix` with base model `GPT-4o`, matching the final audit.\n")
    REPORT.write_text("".join(report))


if __name__ == "__main__":
    main()
