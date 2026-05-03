# Version Status Audit

This note tracks venue drift for retained studies that appeared as arXiv preprints in the released stage files.

The released stage files preserve the labels used during search and screening. The current bibliography, however, cites the latest verified archival venue when a publication can be identified unambiguously.

## Verified archival updates applied in the current bibliography

- `Less is More: Adaptive Program Repair with Bug Localization and Preference Learning` (`AdaPatcher`)
  - Released-stage status: arXiv `2503.06510`
  - Current archival version: AAAI 2025, DOI `10.1609/aaai.v39i1.31988`
  - Current bibliography action: cites the AAAI version.

- `Towards Effectively Leveraging Execution Traces for Program Repair with Code LLMs` (`TracePrompt`)
  - Released-stage status: arXiv `2505.04441`
  - Current archival version: 4th International Workshop on Knowledge-Augmented Methods for Natural Language Processing (ACL Anthology 2025)
  - Current bibliography action: cites the workshop proceedings version.

- `DistiLRR: Transferring Code Repair for Low-Resource Programming Languages`
  - Released-stage status: arXiv `2406.14867`
  - Current archival version: `Investigating the Transferability of Code Repair for Low-Resource Programming Languages`, Findings of the Association for Computational Linguistics: NAACL 2025, DOI `10.18653/v1/2025.findings-naacl.190`
  - Current bibliography action: cites the NAACL Findings paper, while the survey text keeps `DistiLRR` as the system name.

- `Vul-R2: A Reasoning LLM for Automated Vulnerability Repair`
  - Released-stage status in the public candidate logs: conference record `ASE 2025` with linked arXiv id `2510.05480`
  - Current bibliography action: cites the ASE 2025 conference version instead of a stale arXiv-only placeholder.

- `Hierarchical Knowledge Injection for Improving LLM-based Program Repair`
  - Released-stage status: arXiv `2506.24015`
  - Current archival version: `ASE 2025`
  - Current bibliography action: cites the ASE 2025 conference version.

- `LLM4CVE: Enabling Iterative Automated Vulnerability Repair with Large Language Models`
  - Released-stage status: arXiv `2501.03446`
  - Current archival version: `DSD 2025`
  - Current bibliography action: cites the DSD 2025 conference version.

- `PredicateFix: Repairing Static Analysis Alerts with Bridging Predicates`
  - Released-stage status: arXiv `2503.12205`
  - Current archival version: `ICSE 2026`
  - Current bibliography action: cites the ICSE 2026 research-track version.

- `Enhancing LLM-Based Automated Program Repair with Design Rationales` (`DRCodePilot`)
  - Released-stage status: arXiv `2408.03873`
  - Current archival version: `Enhancing Automated Program Repair with Solution Design`, `ASE 2024`
  - Current bibliography action: cites the ASE 2024 conference version while the survey text keeps `DRCodePilot` as the system name.

- `The Art of Repair: Optimizing Iterative Program Repair with Instruction-Tuned Models`
  - Released-stage status: arXiv `2505.02931`
  - Current archival version: `EASE 2025`
  - Current bibliography action: cites the EASE 2025 conference version.

- `Majority Rule: Better Patching via Self-Consistency`
  - Released-stage status: arXiv `2306.00108`
  - Current archival version: `Better Patching Using LLM Prompting, via Self-Consistency`, `ASE 2023`
  - Current bibliography action: cites the ASE 2023 conference version.

## Related-work update outside the retained system corpus

- `A systematic literature review on large language models for automated program repair`
  - Earlier status: arXiv `2405.01466`
  - Current archival version: `ACM Transactions on Software Engineering and Methodology` (2026), DOI `10.1145/3799693`
  - Current bibliography action: cites the TOSEM version instead of the preprint.

## Retained as arXiv in the current bibliography

During the current audit, the following retained studies were not upgraded because no archival publication was verified unambiguously from the checked sources:

- `Abstain and Validate: A Dual-LLM Policy for Reducing Noise in Agentic Program Repair`
- `Agent That Debugs: Dynamic State-Guided Vulnerability Repair`
- `Enhancing repository-level software repair via repository-aware knowledge graphs`
- `LLM-Powered Code Vulnerability Repair with Reinforcement Learning and Semantic Reward`
- `NARRepair: Non-Autoregressive Code Generation Model for Automatic Program Repair`
- `SWE-RL: Advancing LLM Reasoning via Reinforcement Learning on Open Software Evolution`
- `TraceFixer: Execution Trace-Driven Program Repair`
- `TSAPR: A Tree Search Framework For Automated Program Repair`
- `Unlocking LLM Repair Capabilities in Low-Resource Programming Languages Through Cross-Language Translation and Multi-Agent Refinement`

## Stage-6 retained-list correction

The current artifact also corrects one stale retained-list mismatch in `remote_results/stage6.jsonl`: a vulnerability-detection paper (`Smart-LLaMA-DPO`) was occupying one retained slot even though it is not part of the repair corpus used in the manuscript tables. It has been replaced with the retained repair paper `Vul-R2`, which already appeared in the public candidate logs and in the manuscript itself.
