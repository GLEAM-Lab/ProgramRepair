#!/usr/bin/env python3
"""Audit evaluation-reliability evidence in the 66-system corpus.

This script is intentionally conservative. It scans the full-text cache for the
66 systems used in the manuscript and exports candidate evidence snippets for
three manuscript-facing reliability dimensions:

* explicit contamination / data-leakage discussion;
* active leakage mitigation or diagnostic control; and
* validation beyond public benchmark tests (e.g., hidden/additional tests,
  manual/expert review, sanitizer/exploit/static-analyzer validation).

The candidate snippets are not the final labels. Final labels should be based on
manual confirmation of these snippets and are recorded in
evaluation_reliability_by_system.csv.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifact" / "pdf_text_cache" / "manifest.csv"
SYSTEMS = ROOT / "artifact" / "benchmark_protocol_comparability_by_system.csv"
OUT = ROOT / "artifact" / "evaluation_reliability_candidate_snippets.csv"
FINAL_OUT = ROOT / "artifact" / "evaluation_reliability_by_system.csv"
SUMMARY_OUT = ROOT / "artifact" / "evaluation_reliability_risk_coding.csv"


SYSTEM_PDFS = {
    "Huang et al.": "Fine-Tuning Approaches/Supervised fine-tuning of Full Models/An_Empirical_Study_on_Fine-Tuning_Large_Language_Models_of_Code_for_Automated_Program_Repair.pdf",
    "Jiang et al.": "Fine-Tuning Approaches/Supervised fine-tuning of Full Models/Impact of Code Language Models on Automated.pdf",
    "VulMaster": "Fine-Tuning Approaches/Supervised fine-tuning of Full Models/Out of sight, out of mind Better automatic  vulnerability repair by broadening input ranges and sources..pdf",
    "RepairCAT": "Fine-Tuning Approaches/Supervised fine-tuning of Full Models/RepairCAT Applying Large Language Model to Fix Bugs in AI-Generated Programs..pdf",
    "RepairLLaMA": "Fine-Tuning Approaches/Parameter-Efficient Fine-Tuning/Repairllama Efficient representations and fine-tuned adapters  for program repair..pdf",
    "MORepair": "Fine-Tuning Approaches/Parameter-Efficient Fine-Tuning/MORepair Teaching LLMs to Repair Code via Multi-Objective Fine-tuning.pdf",
    "Luo et al.": "Fine-Tuning Approaches/Parameter-Efficient Fine-Tuning/When Fine-Tuning LLMs Meets Data Privacy An Empirical Study of Federated Learning in  LLM-Based Program Repair..pdf",
    "Li et al.": "Fine-Tuning Approaches/Parameter-Efficient Fine-Tuning/Exploring Parameter-Efficient Fine-Tuning of Large Language.pdf",
    "Ruiz et al.": "Fine-Tuning Approaches/Parameter-Efficient Fine-Tuning/The Art of Repair Optimizing Iterative Program Repair with Instruction-Tuned Models.pdf",
    "KNOD": "Fine-Tuning Approaches/Knowledge Distilling/KNOD_Domain_Knowledge_Distilled_Tree_Decoder_for_Automated_Program_Repair.pdf",
    "DistiLRR": "Fine-Tuning Approaches/Knowledge Distilling/DistiLRR Transferring Code Repair  for Low-Resource Programming Languages..pdf",
    "NARRepair": "Fine-Tuning Approaches/Knowledge Distilling/Narrepair Non-autoregressive code generation model for  automatic program repair.pdf",
    "RePair": "Fine-Tuning Approaches/Reinforcement Learning Fine-Tuning/Repair  Automated program repair with process-based feedback.pdf",
    "SecRepair": "Fine-Tuning Approaches/Reinforcement Learning Fine-Tuning/LLM-Powered Code Vulnerability Repair.pdf",
    "SWE-RL": "Fine-Tuning Approaches/Reinforcement Learning Fine-Tuning/Swe-rl Advancing llm reasoning via reinforcement learning on open software  evolution..pdf",
    "AdaPatcher": "Fine-Tuning Approaches/Reinforcement Learning Fine-Tuning/Less is More Adaptive Program Repair with Bug Localization and Preference Learning.pdf",
    "Vul-R2": "Fine-Tuning Approaches/Reinforcement Learning Fine-Tuning/Vul-R2 A Reasoning LLM for Automated Vulnerability Repair.pdf",
    "TraceFixer": "Fine-Tuning Approaches/Context-Enriched fine-tuning/TraceFixer Execution tracedriven program repair..pdf",
    "InferFix": "Fine-Tuning Approaches/Context-Enriched fine-tuning/Inferfix End-to-end program repair with llms.pdf",
    "PyTy": "Fine-Tuning Approaches/Context-Enriched fine-tuning/Pyty Repairing static type errors in python..pdf",
    "NTR": "Fine-Tuning Approaches/Context-Enriched fine-tuning/Template-guided program repair in the era of large  language models..pdf",
    "AlphaRepair": "Prompting Approaches/Zero-shot Prompting/Less training, more repairing please revisiting automated program repair via zero-shot learning.pdf",
    "Prenner et al.": "Prompting Approaches/Zero-shot Prompting/Can OpenAI’s Codex Fix Bugs.pdf",
    "Fan et al.": "Prompting Approaches/Zero-shot Prompting/Automated repair of programs  from large language models.pdf",
    "Tian et al.": "Prompting Approaches/Zero-shot Prompting/Is ChatGPT the ultimate programming assistant–how far is it.pdf",
    "Xia et al.": "Prompting Approaches/Few-shot Prompting/Automated_Program_Repair_in_the_Era_of_Large_Pre-trained_Language_Models.pdf",
    "Gao et al.": "Prompting Approaches/Few-shot Prompting/What_Makes_Good_In-Context_Demonstrations_for_Code_Intelligence_Tasks_with_LLMs.pdf",
    "Ahmed et al.": "Prompting Approaches/Few-shot Prompting/Majority Rule better patching via Self-Consistency.pdf",
    "CEDAR": "Prompting Approaches/Few-shot Prompting/Retrieval-Based_Prompt_Selection_for_Code-Related_Few-Shot_Learning.pdf",
    "Ehsani et al.": "Prompting Approaches/Retrieval-Augmented Generation Enhanced Prompting/Hierarchical Knowledge Injection for Improving LLM-based Program Repair.pdf",
    "RLCE": "Prompting Approaches/Retrieval-Augmented Generation Enhanced Prompting/When  large language models confront repository-level automatic program repair How well they done.pdf",
    "DsRepair": "Prompting Approaches/Retrieval-Augmented Generation Enhanced Prompting/Knowledge-Enhanced Program Repair for  Data Science.pdf",
    "D4C": "Prompting Approaches/Analysis-Augmented Generation Enhanced Prompting/Aligning the Objective of LLM-based Program Repair..pdf",
    "Appatch": "Prompting Approaches/Analysis-Augmented Generation Enhanced Prompting/APPATCH Automated Adaptive Prompting Large Language Models for Real-World Software Vulnerability Patching.pdf",
    "TracePrompt": "Prompting Approaches/Analysis-Augmented Generation Enhanced Prompting/Towards Effectively Leveraging  Execution Traces for Program Repair with Code LLMs..pdf",
    "ChatRepair": "Procedural Approaches/Test-in-the-Loop Pipelines/Automated program repair via conversation Fixing 162 out of 337  bugs for $0.42 each using ChatGPT.pdf",
    "ThinkRepair": "Procedural Approaches/Test-in-the-Loop Pipelines/Thinkrepair Self-directed  automated program repair..pdf",
    "REx": "Procedural Approaches/Test-in-the-Loop Pipelines/Code repair  with llms gives an exploration-exploitation tradeoff.pdf",
    "ContrastRepair": "Procedural Approaches/Test-in-the-Loop Pipelines/Contrastrepair Enhancing  conversation-based automated program repair via contrastive test case pairs.pdf",
    "CREF": "Procedural Approaches/Human-in-the-Loop Pipelines/Cref An llm-based conversational software repair framework for programming tutors..pdf",
    "HULA": "Procedural Approaches/Human-in-the-Loop Pipelines/Human-In-the-Loop Software Development Agents..pdf",
    "DRCodePilot": "Procedural Approaches/Human-in-the-Loop Pipelines/Enhancing LLM-Based Automated Program  Repair with Design Rationales..pdf",
    "Agentless": "Procedural Approaches/RAG-in-the-Loop Pipelines/Agentless Demystifying llm-based  software engineering agents..pdf",
    "PATCH": "Procedural Approaches/RAG-in-the-Loop Pipelines/PATCH Empowering Large Language Model with Programmer-Intent Guidance and Collaborative-Behavior Simulation for Automatic Bug Fixing.pdf",
    "KGCompass": "Procedural Approaches/RAG-in-the-Loop Pipelines/Enhancing Repository-Level  Software Repair via Repository-Aware Knowledge Graphs.pdf",
    "Repilot": "Procedural Approaches/AAG-in-the-Loop Pipelines/Copiloting the Copilots Fusing Large Language Models with Completion Engines for Automated Program Repair.pdf",
    "SAN2PATCH": "Procedural Approaches/AAG-in-the-Loop Pipelines/Logs In, Patches Out Automated Vulnerability Repair via Tree-of-Thought LLM Analysis.pdf",
    "PredicateFix": "Procedural Approaches/AAG-in-the-Loop Pipelines/PredicateFix  Repairing Static Analysis Alerts with Bridging Predicates.pdf",
    "LLM4CVE": "Procedural Approaches/AAG-in-the-Loop Pipelines/LLM4CVE Enabling Iterative Automated Vulnerability Repair with Large Language  Models..pdf",
    "SWE-Agent": "Agentic Approaches/Tool-Augmented Agents/Swe-agent Agent-computer interfaces enable automated software engineering..pdf",
    "SWE-Agent M": "Agentic Approaches/Tool-Augmented Agents/SWE-bench Multimodal Do AI Systems Generalize to Visual  Software Domains.pdf",
    "OpenHands": "Agentic Approaches/Tool-Augmented Agents/Openhands An open platform for ai software developers as generalist agents..pdf",
    "AutoCodeRover": "Agentic Approaches/Tool-Augmented Agents/Autocoderover Autonomous program  improvement..pdf",
    "RepairAgent": "Agentic Approaches/Tool-Augmented Agents/Repairagent An autonomous, llm-based agent for  program repair..pdf",
    "LANTERN": "Agentic Approaches/Tool-Augmented Agents/Unlocking LLM Repair Capabilities in Low-Resource Programming Languages Through Cross-Language Translation  and Multi-Agent Refinement..pdf",
    "VulDebugger": "Agentic Approaches/Tool-Augmented Agents/Agent That Debugs Dynamic State-Guided Vulnerability Repair..pdf",
    "Abstain and Validate": "Agentic Approaches/LLM-as-Judges/Abstain and Validate A Dual-LLM Policy for Reducing Noise in Agentic Program Repair.pdf",
    "TSAPR": "Agentic Approaches/LLM-as-Judges/TSAPR A Tree Search Framework For Automated Program Repair.pdf",
    "SpecRover": "Agentic Approaches/LLM-as-Judges/SpecRover Code Intent Extraction via LLMs.pdf",
    "MAGIS": "Agentic Approaches/Self-Controlled System/Magis-llm-based-multi-agent-framework-for-github-issue-resolution.pdf",
    "SWE-Search": "Agentic Approaches/Self-Controlled System/SWE-Search Enhancing Software Agents with Monte Carlo Tree Search and Iterative Refinement.pdf",
    "Learn-by-Interact": "Agentic Approaches/Self-Controlled System/Learn-by-Interact A Data-Centric Framework For Self-Adaptive Agents in Realistic Environments.pdf",
    "PailGen": "Prompting Approaches/Retrieval-Augmented Generation Enhanced Prompting/Fix Pattern-Aware Vulnerability Patch Generation via In-Context Learning.pdf",
    "ACFix": "Prompting Approaches/Analysis-Augmented Generation Enhanced Prompting/ACFix Guiding LLMs With Mined Common RBAC Practices for Context-Aware Repair of Access Control Vulnerabilities in Smart Contracts.pdf",
    "Dr.Fix": "Prompting Approaches/Analysis-Augmented Generation Enhanced Prompting/Identifying and Mitigating API Misuse in Large Language Models.pdf",
    "IntDiagSolver": "Procedural Approaches/AAG-in-the-Loop Pipelines/Exploring Large Language Models in Resolving Environment-Related Crash Bugs Localizing and Repairing.TOSEM.pdf",
}


PATTERNS = {
    "leakage": re.compile(
        r"(?i)(data[- ]?leak|leakage|contaminat|pre[- ]?training data|pretraining data|"
        r"train(?:ing)?[- ]?test overlap|benchmark overlap|leakage[- ]?free|decontaminat|deduplicat)"
    ),
    "extra_validation": re.compile(
        r"(?i)(hidden test|unseen test|held[- ]?out|hold[- ]?out|additional test|"
        r"generated test|EvalPlus|manual(?:ly)? (?:inspect|check|validat|evaluat|review)|"
        r"human (?:inspect|validat|evaluat|review)|expert|independent (?:test|validat|review)|"
        r"sanitizer|exploit|static analy|CodeQL|semgrep|unit test generation|"
        r"validity and effectiveness check|semantic check|runtime check)"
    ),
}


LEAKAGE_LABELS = {
    "Huang et al.": ("yes", "Data Leakage. Prior work AlphaRepair", "Discusses Defects4J/pretraining overlap and follows AlphaRepair-style leakage analysis."),
    "Jiang et al.": ("yes", "data leaking problem", "Introduces HumanEval-Java as a benchmark to avoid data leaking."),
    "VulMaster": ("yes", "hidden label leakage issue", "Identifies and corrects label leakage caused by duplicated vulnerability/fix samples."),
    "RepairLLaMA": ("yes", "suffers from less data leakage", "Uses recent GitBug-Java and discusses pretraining-cutoff leakage mitigation."),
    "MORepair": ("yes", "no overlap between the 45 programming tasks", "Verifies no task overlap between training and EvalRepair benchmark tasks."),
    "Luo et al.": ("yes", "preventing data leakage", "Chooses private/proprietary training data and EvalRepair-Java to reduce leakage risk."),
    "Li et al.": ("yes", "reduction of data leakage risks", "Notes HumanEval-Java as reducing pretraining/benchmark leakage risk."),
    "Ruiz et al.": ("yes", "potential data leakage from the bench", "Discusses benchmark leakage and mitigates with HumanEval-Java and newer models."),
    "NARRepair": ("yes", "To prevent data leakage", "Removes projects related to Defects4J and QuixBugs from training data."),
    "RePair": ("yes", "To prevent data leakage", "Splits CodeNet4Repair by problem ID to avoid train/test leakage."),
    "SWE-RL": ("yes", "Aggregate and decontaminate", "Reports decontamination during PR data curation and excludes SWE-bench repositories."),
    "AdaPatcher": ("yes", "avoid data leakage problems", "Splits data by programming problem so a problem appears in only one split."),
    "Vul-R2": ("yes", "temporally-aware data splitting", "Uses temporally aware PrimeVul splitting and SVEN as a separate test set."),
    "NTR": ("yes", "Data Leakage: The pre-training data", "Explicitly checks/mitigates leakage via StarCoder leakage-detection support."),
    "Prenner et al.": ("yes", "Data leakage", "Discusses possible Codex training-set leakage for the benchmark."),
    "Tian et al.": ("yes", "potential data leakage problem", "Uses unseen/common-problem benchmarks to mitigate leakage concerns."),
    "Xia et al.": ("yes", "potential data leak", "Analyzes whether generated Defects4J patches match developer/training-data patches."),
    "Gao et al.": ("yes", "Potential data leakage", "Discusses closed-source Codex/GPT training-set leakage as a threat."),
    "CEDAR": ("yes", "Potential data leakage", "Discusses Codex training-set leakage and uses same model/test set for controlled comparisons."),
    "Ehsani et al.": ("yes", "potential leakage", "Discusses leakage of proprietary LLM pretraining data and relative-effect design."),
    "RLCE": ("yes", "To minimize the risk of leakage", "Uses post-cutoff repository selection to reduce leakage risk in RepoBugs."),
    "DsRepair": ("yes", "constructed to mitigate concerns about data leakage", "Uses DS-1000, which applies perturbations to reduce memorization leakage."),
    "D4C": ("yes", "designed to counter data leakage", "Separates Defects4J leakage-prone comparison from DebugBench leakage-resistant validation."),
    "Appatch": ("yes", "data leakage and contamination issues", "Uses a zero-day dataset after LLM cutoff and checks older ExtractFix leakage risk."),
    "Dr.Fix": ("yes", "avoid data contamination issues", "Excludes The Stack subset used to train StarCoder."),
    "ChatRepair": ("yes", "without potential data leakage", "Adds ConDefect post-cutoff evaluation to address leakage of older benchmarks."),
    "ThinkRepair": ("yes", "potential data leakage", "Discusses developer-patch leakage and rechecks after excluding same-as-reference patches."),
    "ContrastRepair": ("yes", "potential data leak risk", "Uses HumanEval-Java as an unseen benchmark to mitigate ChatGPT leakage risk."),
    "CREF": ("yes", "challenge of data leakage", "Introduces an uncrawled TutorCode benchmark to evaluate realistic capability."),
    "Agentless": ("yes", "data leakage of ground truth developer patches", "Discusses possible GPT-4o leakage and compares pre/post knowledge-cutoff performance."),
    "KGCompass": ("yes", "To address data leakage", "Restricts knowledge graph artifacts to timestamps before each benchmark instance."),
    "PredicateFix": ("yes", "To avoid possible data leakage", "Drops clean-corpus code that precisely matches the patched code."),
    "IntDiagSolver": ("yes", "data contamination", "Adds an unseen dataset and discusses Stack Overflow benchmark contamination."),
    "VulDebugger": ("yes", "data leakage concerns", "Compares against conversation-only LLM patches to address leakage concerns."),
    "SpecRover": ("yes", "risk of data leak", "Counts syntactically identical ground-truth patches to evaluate memorization risk."),
    "SWE-Agent M": ("yes", "Temporal analysis does not reveal", "Performs temporal analysis for possible solution leakage."),
}


ACTIVE_LEAKAGE_CONTROL_SYSTEMS = {
    "Jiang et al.",
    "VulMaster",
    "RepairLLaMA",
    "MORepair",
    "Luo et al.",
    "Li et al.",
    "Ruiz et al.",
    "NARRepair",
    "RePair",
    "SWE-RL",
    "AdaPatcher",
    "Vul-R2",
    "NTR",
    "Tian et al.",
    "RLCE",
    "DsRepair",
    "D4C",
    "Appatch",
    "Dr.Fix",
    "ChatRepair",
    "ThinkRepair",
    "ContrastRepair",
    "CREF",
    "Agentless",
    "KGCompass",
    "PredicateFix",
    "IntDiagSolver",
    "SWE-Agent M",
}


EXTRA_VALIDATION_LABELS = {
    "Huang et al.": ("yes", "manual semantic patch check", "two authors manually check", "Manually checks plausible patches after test execution."),
    "Jiang et al.": ("yes", "manual semantic patch check", "manually check the correctness", "Manually checks plausible patches for semantic equivalence."),
    "RepairLLaMA": ("yes", "manual/expert semantic patch check", "manual assessment by an expert", "Uses AST matching and expert manual assessment for semantic-match patches."),
    "MORepair": ("yes", "additional generated tests", "additional test cases from EvalPlus", "Augments EvalRepair-C++/Java with EvalPlus-derived additional tests."),
    "Luo et al.": ("yes", "additional generated tests", "additional test cases from EvalPlus", "Uses EvalRepair-Java with EvalPlus-expanded tests."),
    "SWE-RL": ("yes", "human-verified benchmark", "human-verified collection", "Reports evaluation on SWE-bench Verified."),
    "InferFix": ("yes", "static-analysis/CI validation", "fixing and validation of candidate patches", "Describes deployment with Infer and candidate-patch validation in CI."),
    "PyTy": ("yes", "static type-checker validation", "checks candidate fixes with a gradual type checker", "Returns a fix only if the gradual type checker reports the target type error removed."),
    "NTR": ("yes", "manual semantic patch check", "plausible patches will be manually checked", "Manually checks plausible patches for semantic correctness."),
    "AlphaRepair": ("yes", "manual semantic patch check", "manually inspecting each plausible patch", "Manually inspects plausible patches for semantic equivalency."),
    "Prenner et al.": ("yes", "manual evaluation step", "evaluation involves a significant manual step", "Reports a significant manual step in evaluation."),
    "Fan et al.": ("yes", "held-out private tests", "held-out (private) tests", "Validates patched LeetCode solutions with public and held-out private tests."),
    "Xia et al.": ("yes", "manual semantic patch check", "manually inspect each plausible patch", "Manually inspects plausible patches for semantic equivalency."),
    "DsRepair": ("yes", "execution-semantic tests", "testing methods checking both execution semantics", "Uses DS-1000 tests that check execution semantics and surface constraints."),
    "D4C": ("yes", "manual and unseen-test validation", "manual validation for each plausible patch", "Adds manual validation and LeetCode validation for DebugBench patches."),
    "Appatch": ("yes", "manual semantic patch check", "manually check each generated patch", "Manually checks generated patches when automatic validation is unavailable."),
    "PailGen": ("yes", "functionality/security tests", "curated and validated test cases", "Uses CWEVAL-BENCH functionality and security test cases in additional evaluation."),
    "ACFix": ("yes", "expert human evaluation", "10 experts", "Conducts human-based evaluation with smart-contract auditing practitioners."),
    "ChatRepair": ("yes", "manual semantic patch check", "manual validation used to determine", "Manually validates plausible patches and releases correct patches."),
    "ThinkRepair": ("yes", "manual semantic patch check", "manual validation employed", "Manually validates plausible patches and discusses them."),
    "REx": ("yes", "formal solver validation", "Z3 solver", "Checks loop-invariant tasks with the Z3 solver."),
    "ContrastRepair": ("yes", "human inspection and generated tests", "further investigated by a human", "Uses human investigation of plausible patches and generated contrastive tests."),
    "HULA": ("yes", "human/tool validation gate", "compilers and linters", "Uses human agreement plus compiler/linter validation in the development workflow."),
    "Agentless": ("yes", "generated reproduction/regression tests", "generated reproduction test", "Uses generated reproduction tests and regression tests for patch selection."),
    "KGCompass": ("yes", "generated reproduction/regression tests", "Reproduction tests are specialized test cases", "Generates reproduction tests and validates with benchmark ground-truth tests."),
    "Repilot": ("yes", "manual semantic patch check", "manually examining each plausible patch", "Manually examines plausible patches for semantic equivalence."),
    "SAN2PATCH": ("yes", "manual validation and sanitizer evidence", "manual validation", "Uses sanitizer logs and manual validation categories for generated patches."),
    "PredicateFix": ("yes", "manual/static-analyzer validation", "manually inspected the patches", "Combines static-analysis alert disappearance with manual inspection for RQ1."),
    "LLM4CVE": ("yes", "human and compilation validation", "human-verified quality score", "Uses human quality scores and end-to-end compilation."),
    "IntDiagSolver": ("yes", "manual and unseen-data validation", "manually reviewed LLM", "Manually reviews responses and evaluates on an unseen dataset."),
    "SWE-Agent M": ("yes", "fail-to-pass/pass-to-pass tests", "fail-to-pass (F2P) tests", "Uses fail-to-pass and pass-to-pass test validation in SWE-bench multimodal."),
    "AutoCodeRover": ("yes", "manual semantic patch check", "cross-validated each patch", "At least two authors cross-validate plausible patches."),
    "RepairAgent": ("yes", "manual semantic patch check", "manually determine whether", "Manually checks non-syntactic matches for semantic consistency."),
    "VulDebugger": ("yes", "vulnerability reproduction/sanitizer validation", "validate them by trying to reproduce the vulnerability", "Validates patches by attempting to reproduce vulnerabilities and using sanitizer-derived constraints."),
    "Abstain and Validate": ("yes", "LLM/human/reproduction-test validation", "known reproduction tests", "Evaluates validation policy with fail-to-pass, human acceptance, and known reproduction tests."),
    "TSAPR": ("yes", "human and LLM/test judge validation", "further human inspection", "Retains plausible patches for human inspection and uses LLM-as-Judge/Test-as-Judge."),
    "SpecRover": ("yes", "reviewer-agent/manual validation", "evidence of correctness", "Uses a reviewer agent and manual comparison of test-passing patches."),
    "SWE-Search": ("yes", "concealed fail-to-pass tests", "fail-to-pass tests remain concealed", "Uses repository tests while keeping fail-to-pass tests concealed from the model."),
    "Learn-by-Interact": ("yes", "sample-specific evaluation scripts", "evaluation scripts", "Uses sample-specific scripts, file comparison, and execution-based verification."),
}


def load_manifest() -> dict[str, Path]:
    if not MANIFEST.exists():
        raise SystemExit(
            "Missing artifact/pdf_text_cache/manifest.csv. "
            "Run `python3 artifact/extract_pdf_text_cache.py` before this audit."
        )
    with MANIFEST.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {row["pdf_path"]: ROOT / row["text_cache"] for row in rows if row["status"] == "ok"}


def load_systems() -> list[str]:
    with SYSTEMS.open(newline="", encoding="utf-8") as f:
        return [row["system"] for row in csv.DictReader(f)]


def page_for(text: str, offset: int) -> str:
    prefix = text[:offset]
    matches = list(re.finditer(r"\[\[PAGE\s+(\d+)\]\]", prefix))
    return matches[-1].group(1) if matches else ""


def normalize_snippet(snippet: str) -> str:
    return re.sub(r"\s+", " ", snippet).strip()


def find_evidence(text: str, needle: str) -> tuple[str, str]:
    phrase_pattern = r"\s+".join(re.escape(part) for part in needle.split())
    match = re.search(phrase_pattern, text, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"Evidence phrase not found: {needle!r}")
    start = max(0, match.start() - 280)
    end = min(len(text), match.end() + 520)
    return page_for(text, match.start()), normalize_snippet(text[start:end])


def snippets(text: str, pattern: re.Pattern[str], max_hits: int = 6) -> list[tuple[str, str]]:
    hits: list[tuple[str, str]] = []
    seen = set()
    for match in pattern.finditer(text):
        start = max(0, match.start() - 360)
        end = min(len(text), match.end() + 520)
        snippet = normalize_snippet(text[start:end])
        key = snippet[:220]
        if key in seen:
            continue
        seen.add(key)
        hits.append((page_for(text, match.start()), snippet))
        if len(hits) >= max_hits:
            break
    return hits


def main() -> None:
    manifest = load_manifest()
    systems = load_systems()
    missing_systems = sorted(set(systems) - set(SYSTEM_PDFS))
    extra_mappings = sorted(set(SYSTEM_PDFS) - set(systems))
    missing_pdfs = sorted(pdf for pdf in SYSTEM_PDFS.values() if pdf not in manifest)
    if missing_systems or extra_mappings or missing_pdfs:
        raise SystemExit(
            "Mapping mismatch:\n"
            f"missing systems: {missing_systems}\n"
            f"extra mappings: {extra_mappings}\n"
            f"missing PDFs in manifest: {missing_pdfs}"
        )

    candidate_rows: list[dict[str, str]] = []
    final_rows: list[dict[str, str]] = []
    for system in systems:
        pdf = SYSTEM_PDFS[system]
        text = manifest[pdf].read_text(encoding="utf-8", errors="replace")
        for category, pattern in PATTERNS.items():
            hits = snippets(text, pattern)
            if not hits:
                candidate_rows.append(
                    {
                        "system": system,
                        "pdf_path": pdf,
                        "category": category,
                        "page": "",
                        "snippet": "",
                    }
                )
            else:
                for page, snippet in hits:
                    candidate_rows.append(
                        {
                            "system": system,
                            "pdf_path": pdf,
                            "category": category,
                            "page": page,
                            "snippet": snippet,
                        }
                    )

        leakage_label, leakage_query, leakage_note = LEAKAGE_LABELS.get(system, ("no", "", "No explicit contamination/data-leakage discussion found in the audited full text."))
        if leakage_label == "yes":
            leakage_page, leakage_evidence = find_evidence(text, leakage_query)
        else:
            leakage_page, leakage_evidence = "", ""

        validation_label, validation_type, validation_query, validation_note = EXTRA_VALIDATION_LABELS.get(
            system,
            (
                "no",
                "",
                "",
                "No hidden/additional tests, manual/expert review, static/runtime validation, or independent validation beyond ordinary benchmark/public tests found in the audited full text.",
            ),
        )
        if validation_label == "yes":
            validation_page, validation_evidence = find_evidence(text, validation_query)
        else:
            validation_page, validation_evidence = "", ""

        final_rows.append(
            {
                "system": system,
                "pdf_path": pdf,
                "leakage_discussion_or_control": leakage_label,
                "leakage_evidence_page": leakage_page,
                "leakage_evidence": leakage_evidence,
                "leakage_notes": leakage_note,
                "active_leakage_mitigation_or_control": "yes"
                if system in ACTIVE_LEAKAGE_CONTROL_SYSTEMS
                else "no",
                "extra_validation_beyond_public_tests": validation_label,
                "validation_type": validation_type,
                "validation_evidence_page": validation_page,
                "validation_evidence": validation_evidence,
                "validation_notes": validation_note,
            }
        )

    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["system", "pdf_path", "category", "page", "snippet"])
        writer.writeheader()
        writer.writerows(candidate_rows)

    final_fields = [
        "system",
        "pdf_path",
        "leakage_discussion_or_control",
        "leakage_evidence_page",
        "leakage_evidence",
        "leakage_notes",
        "active_leakage_mitigation_or_control",
        "extra_validation_beyond_public_tests",
        "validation_type",
        "validation_evidence_page",
        "validation_evidence",
        "validation_notes",
    ]
    with FINAL_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=final_fields)
        writer.writeheader()
        writer.writerows(final_rows)

    leakage_count = sum(row["leakage_discussion_or_control"] == "yes" for row in final_rows)
    active_leakage_count = sum(row["active_leakage_mitigation_or_control"] == "yes" for row in final_rows)
    validation_count = sum(row["extra_validation_beyond_public_tests"] == "yes" for row in final_rows)

    existing_rows: list[dict[str, str]] = []
    if SUMMARY_OUT.exists():
        with SUMMARY_OUT.open(newline="", encoding="utf-8") as f:
            existing_rows = [
                row
                for row in csv.DictReader(f)
                if row["risk_factor"]
                not in {
                    "explicit_contamination_or_leakage_discussion_or_control",
                    "explicit_contamination_or_leakage_discussion",
                    "active_leakage_mitigation_or_control",
                    "hidden_manual_or_independent_validation_beyond_public_tests",
                }
            ]

    existing_rows.extend(
        [
            {
                "risk_factor": "explicit_contamination_or_leakage_discussion",
                "coding_criterion": "The paper explicitly discusses possible data contamination, leakage, benchmark overlap, or related mitigation concerns.",
                "count": str(leakage_count),
                "denominator": str(len(systems)),
                "source": "evaluation_reliability_by_system.csv",
                "interpretation": "Counts explicit reporting about contamination or leakage risk; active mitigation or diagnostic controls are counted separately.",
            },
            {
                "risk_factor": "active_leakage_mitigation_or_control",
                "coding_criterion": "The paper reports a concrete leakage-mitigation or diagnostic control, such as decontamination, temporal or train/test split design, benchmark construction to avoid overlap, dataset exclusion, or explicit leakage analysis tied to the reported evaluation.",
                "count": str(active_leakage_count),
                "denominator": str(len(systems)),
                "source": "evaluation_reliability_by_system.csv",
                "interpretation": "Subset of the explicit-reporting row; excludes papers that only acknowledge leakage risk without a concrete mitigation or diagnostic check.",
            },
            {
                "risk_factor": "hidden_manual_or_independent_validation_beyond_public_tests",
                "coding_criterion": "The evaluation uses hidden/held-out/additional tests, manual or expert review, LLM/human review, static or runtime validation, sanitizer/exploit reproduction, or a comparable independent validation signal beyond ordinary public benchmark tests.",
                "count": str(validation_count),
                "denominator": str(len(systems)),
                "source": "evaluation_reliability_by_system.csv",
                "interpretation": "Counts heterogeneous extra validation signals; it does not imply a shared oracle or directly comparable validation strength.",
            },
        ]
    )
    with SUMMARY_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["risk_factor", "coding_criterion", "count", "denominator", "source", "interpretation"],
        )
        writer.writeheader()
        writer.writerows(existing_rows)

    print(f"Wrote {OUT.relative_to(ROOT)} with candidate snippets for {len(systems)} systems")
    print(f"Wrote {FINAL_OUT.relative_to(ROOT)}")
    print(f"Leakage discussion: {leakage_count}/{len(systems)}")
    print(f"Active leakage mitigation/control: {active_leakage_count}/{len(systems)}")
    print(f"Extra validation beyond public tests: {validation_count}/{len(systems)}")


if __name__ == "__main__":
    main()
