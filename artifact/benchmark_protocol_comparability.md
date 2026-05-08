# Benchmark Protocol Comparability Analysis
Generated from `artifact/taxonomy_assignment_audit.csv`.
This audit covers all 66 retained systems. It separates bounded protocol-aligned comparison windows from same-benchmark/family coverage groups. The former can be compared only within narrow windows; the latter ensures every paper contributes to the benchmark-protocol analysis without turning heterogeneous protocols into a leaderboard.
## Coverage
- Rows analyzed: 66 / 66
- Rows assigned to at least one comparison window: 13
- Rows retained as snapshot-only under the bounded-window criterion: 53
- Rows assigned to same-benchmark/family coverage groups: 66 / 66

## Comparability tiers
- `A_model_controlled_comparison`: 4
- `B_protocol_aligned_stack_snapshot`: 8
- `C_limited_within_benchmark_comparison`: 1
- `D_snapshot_only`: 53

## Benchmark-family counts
- Other: 24
- Defects4J: 12
- Vulnerability repair datasets: 9
- HumanEval-Java: 8
- SWE-bench Lite: 8
- SWE-bench Other: 2
- SWE-bench Verified: 1
- API misuse repair: 1
- Crash bug repair: 1

## Metric-family counts
- pass@1: 21
- pass@10: 10
- pass@5: 7
- full match: 5
- pass@1000: 2
- F1: 2
- EM: 2
- pass@100: 1
- top@k (5h): 1
- pass@200: 1
- pass@30: 1
- accuracy: 1
- pass@500: 1
- pass@25: 1
- pass@300: 1
- pass@40: 1
- avg@5: 1
- merged PRs: 1
- pass@5000: 1
- CodeBLEU: 1
- accept@1: 1
- pass@16: 1
- success rate: 1
- repair accuracy: 1

## pass@k reporting distribution by year
- 2022: total=2, pass@1=1, pass@5=0, pass@10=0, other pass@k=0, non-pass@k or related=1, pass@1 share=50.0%
- 2023: total=12, pass@1=1, pass@5=3, pass@10=2, other pass@k=4, non-pass@k or related=2, pass@1 share=8.3%
- 2024: total=16, pass@1=5, pass@5=1, pass@10=1, other pass@k=4, non-pass@k or related=5, pass@1 share=31.2%
- 2025: total=30, pass@1=13, pass@5=3, pass@10=6, other pass@k=3, non-pass@k or related=5, pass@1 share=43.3%
- 2026: total=6, pass@1=1, pass@5=0, pass@10=1, other pass@k=0, non-pass@k or related=4, pass@1 share=16.7%

## Protocol-aligned windows

### W1_SWE_BENCH_LITE_PASS1
- **Tier**: B_protocol_aligned_stack_snapshot
- **Criteria**: SWE-bench Lite, pass@1, repository-level issue repair.
- **N**: 8
- **Systems**: MAGIS (16.67%); SWE-Agent (18.00%); AutoCodeRover (19.00%); OpenHands (26%); SpecRover (31.00%); Agentless (32%); SWE-Search (39.00%); KGCompass (46%)
- **Result Range**: 16.67--46.00%
- **Controlled Factors**: Benchmark variant and metric.
- **Remaining Confounders**: Base model, cost budget, search depth, validation strategy, and publication snapshot.
- **Supported Interpretation**: Whole-system stacks vary from 16.67% to 46.00%; repository context selection and search/validation design materially affect results.

### W1a_SWE_BENCH_LITE_CLAUDE35_PASS1
- **Tier**: B_protocol_aligned_stack_snapshot
- **Criteria**: SWE-bench Lite, pass@1, Claude 3.5 Sonnet family.
- **N**: 4
- **Systems**: OpenHands (26%); SpecRover (31.00%); SWE-Search (39.00%); KGCompass (46%)
- **Result Range**: 26.00--46.00%
- **Controlled Factors**: Benchmark variant, metric, and base-model family.
- **Remaining Confounders**: Tool interface, retrieval/search policy, validation depth, and exact model snapshot.
- **Supported Interpretation**: Even under the same base-model family, reported pass@1 spans 26.00%--46.00%, supporting analysis of orchestration/context design.

### W2_HUMANEVAL_JAVA_DEEPSEEK7B_PASS10_PERFECT_FL
- **Tier**: A_model_controlled_comparison
- **Criteria**: HumanEval-Java, pass@10, DeepSeek-Coder 7B, Perfect FL.
- **N**: 2
- **Systems**: Li et al. (68.10%); Ruiz et al. (78.53%)
- **Result Range**: 68.10--78.53%
- **Controlled Factors**: Benchmark, metric, base model, and FL assumption.
- **Remaining Confounders**: Training data, adaptation objective, and iterative repair details.
- **Supported Interpretation**: Ruiz et al. reports 78.53% versus Li et al. 68.10%, showing that training/evaluation design matters even with the same base model and FL assumption.

### W3_HUMANEVAL_JAVA_CODELLAMA13B_PASS10
- **Tier**: A_model_controlled_comparison
- **Criteria**: HumanEval-Java, pass@10, CodeLlama 13B.
- **N**: 2
- **Systems**: Luo et al. (76.88%); MORepair (77.90%)
- **Result Range**: 76.88--77.90%
- **Controlled Factors**: Benchmark, metric, and base-model family.
- **Remaining Confounders**: FL/oracle assumptions are underreported; training objective differs.
- **Supported Interpretation**: Luo et al. (76.88%) and MORepair (77.90%) are close, so this window supports only a narrow comparison of PEFT variants.

### W4_HUMANEVAL_JAVA_PASS10_PEFT
- **Tier**: C_limited_within_benchmark_comparison
- **Criteria**: HumanEval-Java, pass@10, PEFT-oriented systems.
- **N**: 5
- **Systems**: RepairLLaMA (67.28%); Li et al. (68.10%); Luo et al. (76.88%); MORepair (77.90%); Ruiz et al. (78.53%)
- **Result Range**: 67.28--78.53%
- **Controlled Factors**: Benchmark and metric.
- **Remaining Confounders**: Base model, training data, adaptation objective, and FL/oracle assumptions.
- **Supported Interpretation**: The five pass@10 rows range from 67.28% to 78.53%; useful for a bounded discussion, not for broad paradigm ranking.

## Same-benchmark/family protocol coverage groups

### G10_security_api_crash_fragmented: Vulnerability, API-misuse, and crash-repair datasets
- **N**: 11
- **Systems**: VulMaster (full match 20%); Vul-R2 (pass@10 24.83); Appatch (F1 36.46); SAN2PATCH (pass@5 79.49%); PredicateFix (pass@1 81/117); LLM4CVE (CodeBLEU +20%); VulDebugger (pass@1 60%); PailGen (EM 23.23%); ACFix (success rate 94.92%); Dr.Fix (EM 96.00%); IntDiagSolver (repair accuracy 86.7%)
- **Normalized Result Range**: 20.00--96.00%
- **Shared Basis**: Security or robustness-oriented repair tasks.
- **Noncomparable Dimensions**: Datasets and metrics are disjoint: EM, F1, CodeBLEU, success rate, repair accuracy, and pass@k.
- **Safe Interpretation**: Supports the conclusion that security/API/crash repair lacks a consolidated benchmark.

### G11_other_task_specific_or_singleton_benchmarks: Other task-specific or singleton benchmarks
- **N**: 24
- **Systems**: RepairCAT (pass@1000 14%); DistiLRR (pass@1 42.10%); RePair (pass@5 65.66%); SecRepair (F1 82); AdaPatcher (pass@1 67.57%); TraceFixer (pass@10 87%); InferFix (pass@1 76.80%); PyTy (full match 54.40%); Prenner et al. (pass@1 37/80); Fan et al. (pass@5 46/113); Tian et al. (pass@5 105/120); Gao et al. (full match 32.25%); Ahmed et al. (pass@30 31.80%); CEDAR (full match 76.55%); Ehsani et al. (pass@5 79.62%); RLCE (pass@1 81.45%); DsRepair (pass@1 29.18%); REx (pass@300 73.70%); CREF (avg@5 76.60%); HULA (merged PRs 56); DRCodePilot (full match 15.27%); PATCH (pass@5 39.81%); LANTERN (pass@10 87.67%); Abstain and Validate (accept@1 62%)
- **Normalized Result Range**: 14.00--87.67%
- **Shared Basis**: Each row is retained in the corpus-level audit.
- **Noncomparable Dimensions**: The 24 rows span non-overlapping or singleton benchmarks, including APR Competition, QuixBugs, BugsInPy, RepoBugs, DS-1000, TutorCode, Flink, and Google accept@1.
- **Safe Interpretation**: Used for coverage and protocol-diversity analysis, not cross-paper ranking.

### G1_Defects4J_PerfectFL_or_function_level: Defects4J with Perfect-FL/function-level assumptions
- **N**: 6
- **Systems**: Huang et al. (pass@5 82/107); Jiang et al. (pass@10 31/138); KNOD (pass@1000 122/837); NARRepair (pass@1 110/127); AlphaRepair (top@k (5h) 74/109); Xia et al. (pass@200 99/255)
- **Normalized Result Range**: 14.58--86.61%
- **Shared Basis**: Same benchmark family; all six rows use localized Java APR settings with Perfect-FL or comparable localized inputs.
- **Noncomparable Dimensions**: pass@1/top@k/pass@5/pass@10/pass@200/pass@1000 budgets, denominators, benchmark versions, and base models differ.
- **Safe Interpretation**: Useful for showing how headline Defects4J scores depend on FL hints and sampling budget; not a direct ranking.

### G2_Defects4J_single_function: Defects4J single-function variants
- **N**: 3
- **Systems**: D4C (pass@10 180/437); ChatRepair (pass@500 162/337); ThinkRepair (pass@25 98/255)
- **Normalized Result Range**: 38.43--48.07%
- **Shared Basis**: Same benchmark family and single-function scope.
- **Noncomparable Dimensions**: pass@10/pass@25/pass@500 budgets and denominators differ.
- **Safe Interpretation**: Useful for comparing how much extra generation/test feedback is reported under a narrowed scope.

### G3_Defects4J_tool_or_search_no_explicit_FL: Defects4J tool/search systems without explicit Perfect-FL control
- **N**: 2
- **Systems**: RepairAgent (pass@1 164/835); TSAPR (pass@16 24.07%)
- **Normalized Result Range**: 19.64--24.07%
- **Shared Basis**: Same broad benchmark family and GPT-3.5-class repair systems.
- **Noncomparable Dimensions**: pass@1 versus pass@16, tool autonomy, search policy, and FL assumptions differ.
- **Safe Interpretation**: Useful as end-to-end or search-heavy protocol evidence, not a direct score ranking.

### G4_Defects4J_single_hunk: Defects4J single-hunk snapshot
- **N**: 1
- **Systems**: Repilot (pass@5000 116/273)
- **Normalized Result Range**: 42.49--42.49%
- **Shared Basis**: Same benchmark family but singleton scope.
- **Noncomparable Dimensions**: No peer with the same single-hunk protocol in the retained set.
- **Safe Interpretation**: Used as evidence of subset specialization.

### G6_HumanEvalJava_pass10: HumanEval-Java pass@10
- **N**: 5
- **Systems**: RepairLLaMA (pass@10 67.28%); MORepair (pass@10 77.90%); Luo et al. (pass@10 76.88%); Li et al. (pass@10 68.10%); Ruiz et al. (pass@10 78.53%)
- **Normalized Result Range**: 67.28--78.53%
- **Shared Basis**: Same benchmark and pass@10 metric.
- **Noncomparable Dimensions**: Base model, training data, PEFT objective, and FL reporting differ.
- **Safe Interpretation**: Supports bounded comparison of PEFT-oriented repair systems; two smaller subwindows control base model more tightly.

### G7_HumanEvalJava_other_metrics: HumanEval-Java non-pass@10 rows
- **N**: 3
- **Systems**: NTR (pass@100 83.44%); TracePrompt (accuracy 71.30%); ContrastRepair (pass@40 84.05%)
- **Normalized Result Range**: 71.30--84.05%
- **Shared Basis**: Same benchmark.
- **Noncomparable Dimensions**: pass@100, pass@40, and accuracy are different metrics.
- **Safe Interpretation**: Used to show metric heterogeneity rather than ranked against pass@10.

### G8_SWEBench_Lite_pass1: SWE-bench Lite pass@1
- **N**: 8
- **Systems**: Agentless (pass@1 32%); KGCompass (pass@1 46%); SWE-Agent (pass@1 18.00%); OpenHands (pass@1 26%); AutoCodeRover (pass@1 19.00%); SpecRover (pass@1 31.00%); MAGIS (pass@1 16.67%); SWE-Search (pass@1 39.00%)
- **Normalized Result Range**: 16.67--46.00%
- **Shared Basis**: Same benchmark variant and pass@1 metric.
- **Noncomparable Dimensions**: Base model, exact snapshot, cost budget, search depth, retrieval policy, and validation depth differ.
- **Safe Interpretation**: Largest protocol-aligned whole-stack comparison window in the corpus.

### G9_SWEBench_other_variants: SWE-bench Verified, Multimodal, and full/conditioned variants
- **N**: 3
- **Systems**: SWE-RL (pass@1 41.00%); SWE-Agent M (pass@1 12.20%); Learn-by-Interact (pass@1 60.00%)
- **Normalized Result Range**: 12.20--60.00%
- **Shared Basis**: Same repository-level benchmark family.
- **Noncomparable Dimensions**: Different benchmark variants and additional environment, multimodal, or trajectory conditions.
- **Safe Interpretation**: Kept separate from Lite pass@1 while still contributing to repository-level protocol analysis.

## Non-comparable families and why
- **Defects4J**: 12 rows can all be used in same-family protocol analysis. They split into Perfect-FL/function-level, single-function, tool/search, and single-hunk groups, but the rows still mix benchmark versions/subsets, denominators, pass@k budgets from 1 to 5000, and FL assumptions. A global ranking remains unsupported by the reported protocols.
- **HumanEval-Java non-pass@10 rows**: NTR uses pass@100, ContrastRepair uses pass@40, and TracePrompt reports accuracy; these should remain protocol snapshots rather than being ranked against pass@10 PEFT rows.
- **SWE-bench Verified/Other**: SWE-RL is a singleton Verified row, while SWE-Agent M and Learn-by-Interact use different SWE-bench variants or extra environment/trajectory conditions.
- **Vulnerability/API/crash repair**: rows use disjoint datasets and metric families, including exact match, F1, CodeBLEU, EM, success rate, repair accuracy, and pass@k.
- **Other benchmark family**: rows use smaller or domain-specific datasets; apparent metric matches can occur across different datasets and should not be ranked.

## Manuscript consistency checks
- The current SWE-bench table uses `MAGIS` for the SWE-bench Lite `pass@1: 16.67%` row and keeps `TSAPR` only in the Defects4J table, matching `taxonomy_assignment_audit.csv` and the detailed system table.
- The current Defects4J table records `KNOD` with base model `Not specified`, matching the audit value `/`.
- The current Defects4J table does not mark `TSAPR` as a Perfect-FL row, matching the final audit.
- The current fragmented security/API table uses `EM` for `PailGen` and `Dr.Fix`, and records `Dr.Fix` with base model `GPT-4o`, matching the final audit.
