# Version Status Audit

This note tracks venue drift for retained studies that appeared as arXiv preprints in the released stage files.

The released stage files preserve the labels used during search and screening. The current bibliography cites an archival venue only when that venue version is reflected in the manuscript BibTeX. Otherwise, the paper remains cited as the retained preprint or stage-file record, and the possible venue drift is recorded below rather than silently overwritten.

## Verified archival updates reflected in the current bibliography

- `Less is More: Adaptive Program Repair with Bug Localization and Preference Learning` (`AdaPatcher`)
  - Released-stage status: arXiv `2503.06510`
  - Current archival version: AAAI 2025, DOI `10.1609/aaai.v39i1.31988`
  - Current bibliography action: cites the AAAI version.

- `Towards Effectively Leveraging Execution Traces for Program Repair with Code LLMs` (`TracePrompt`)
  - Released-stage status: arXiv `2505.04441`
  - Current archival version: 4th International Workshop on Knowledge-Augmented Methods for Natural Language Processing (ACL Anthology 2025)
  - Current bibliography action: cites the workshop proceedings version.

- `Enhancing LLM-Based Automated Program Repair with Design Rationales` (`DRCodePilot`)
  - Released-stage status: arXiv `2408.03873`
  - Current archival version: `Enhancing Automated Program Repair with Solution Design`, `ASE 2024`
  - Current bibliography action: cites the ASE 2024 conference version while the survey text keeps `DRCodePilot` as the system name.

- `Majority Rule: Better Patching via Self-Consistency`
  - Released-stage status: arXiv `2306.00108`
  - Current archival version: `Better Patching Using LLM Prompting, via Self-Consistency`, `ASE 2023`
  - Current bibliography action: cites the ASE 2023 conference version.

- `PredicateFix: Repairing Static Analysis Alerts with Bridging Predicates`
  - Released-stage status: arXiv `2503.12205`
  - Current archival version: ICSE 2026, DOI `10.1145/3744916.3773159`
  - Current bibliography action: cites the ICSE 2026 conference version while retaining the arXiv identifier for traceability.

- `Unlocking LLM Repair Capabilities Through Cross-Language Translation and Multi-Agent Refinement` (`LANTERN`)
  - Released-stage status: arXiv `2503.22512`
  - Current archival version: ICSE 2026 research-track record
  - Current bibliography action: cites the ICSE 2026 conference version while retaining the system name `LANTERN` in the survey text.

- `Abstain and Validate: A Dual-LLM Policy for Reducing Noise in Agentic Program Repair`
  - Released-stage status: arXiv `2510.03217`
  - Current archival version: ICSE-SEIP 2026 program record
  - Current bibliography action: cites the ICSE-SEIP 2026 accepted version while retaining the arXiv URL for traceability.

- `Hierarchical Knowledge Injection for Improving LLM-based Program Repair`
  - Released-stage status: arXiv `2506.24015`
  - Current archival version: ASE 2025, DOI `10.1109/ASE63991.2025.00122`
  - Current bibliography action: cites the ASE 2025 conference version.

- `Vul-R2: A Reasoning LLM for Automated Vulnerability Repair`
  - Released-stage status: arXiv `2510.05480`
  - Current archival version: ASE 2025, DOI `10.1109/ASE63991.2025.00011`
  - Current bibliography action: cites the ASE 2025 conference version.

- `DistiLRR: Transferring Code Repair for Low-Resource Programming Languages`
  - Released-stage status: arXiv `2406.14867`
  - Current archival version: `Investigating the Transferability of Code Repair for Low-Resource Programming Languages`, Findings of NAACL 2025, DOI `10.18653/v1/2025.findings-naacl.190`
  - Current bibliography action: cites the ACL Anthology version while the survey text keeps `DistiLRR` as the system name.

- `SWE-RL: Advancing LLM Reasoning via Reinforcement Learning on Open Software Evolution`
  - Released-stage status: arXiv/preprint record
  - Current archival version: NeurIPS 2025
  - Current bibliography action: cites the NeurIPS 2025 conference version.

## Additional cited-year normalizations checked in this audit

These records do not change the 66-system corpus, but they affect the year labels used in the taxonomy table, annual-count table, benchmark snapshots, or BibTeX.

- `Aligning the Objective of LLM-based Program Repair` (`D4C`)
  - Released-stage status: arXiv `2404.08877`
  - Current archival version: ICSE 2025, DOI `10.1109/ICSE55347.2025.00169`
  - Current action: keep the system in the Prompting/AAG row and normalize table year labels to 2025.

- `Template-Guided Program Repair in the Era of Large Language Models` (`NTR`)
  - Released-stage status: research-track/program-record entry
  - Current archival version: ICSE 2025, DOI `10.1109/ICSE55347.2025.00030`
  - Current action: keep the system in the Fine-Tuning/Full FT row and normalize the bibliography and table year labels to 2025.

- `ContrastRepair: Enhancing Conversation-Based Automated Program Repair via Contrastive Test Case Pairs`
  - Released-stage status: arXiv `2403.01971`
  - Current archival version: TOSEM 2025, DOI `10.1145/3719345`
  - Current action: keep the system in the Procedural/Test-in-the-Loop row and normalize benchmark year labels to 2025.

- `Demystifying LLM-based Software Engineering Agents` (`Agentless`)
  - Released-stage status: arXiv `2407.01489`
  - Current archival version: FSE 2025
  - Current action: keep the system in the Procedural/Scripted Tool Loop row and normalize benchmark year labels to 2025.

- `OpenHands: An Open Platform for AI Software Developers as Generalist Agents`
  - Released-stage status: preprint/program-record entry
  - Current archival version: ICLR 2025
  - Current action: keep the system in the Agentic/Tool-Augmented Agents row and normalize the BibTeX year and benchmark year labels to 2025.

- `SWE-bench Multimodal: Do AI Systems Generalize to Visual Software Domains?` (`SWE-Agent M`)
  - Released-stage status: arXiv `2410.03859`
  - Current archival version: ICLR 2025
  - Current action: keep the system in the Agentic/Tool-Augmented Agents row and normalize the BibTeX year to 2025.

- `SWE-Search: Enhancing Software Agents with Monte Carlo Tree Search and Iterative Refinement`
  - Released-stage status: preprint/program-record entry
  - Current archival version: ICLR 2025
  - Current action: keep the system in the Agentic/Self-Controlled System row and normalize the BibTeX year and benchmark year labels to 2025.

## Related-work update outside the retained system corpus

- `A systematic literature review on large language models for automated program repair`
  - Earlier status: arXiv `2405.01466`
  - Current archival version: `ACM Transactions on Software Engineering and Methodology` (2026), DOI `10.1145/3799693`
  - Current bibliography action: cites the TOSEM version instead of the preprint.

## Retained as arXiv in the current bibliography

During the current audit, the following retained studies remain cited as arXiv/preprint or stage-file records in the current bibliography. Some have candidate venue hints outside the manuscript's configured venue families, but no in-scope archival citation was inserted into the current BibTeX for this manuscript version.

- `Agent That Debugs: Dynamic State-Guided Vulnerability Repair`
- `Enhancing repository-level software repair via repository-aware knowledge graphs`
- `LLM4CVE: Enabling Iterative Automated Vulnerability Repair with Large Language Models`
- `LLM-Powered Code Vulnerability Repair with Reinforcement Learning and Semantic Reward`
- `NARRepair: Non-Autoregressive Code Generation Model for Automatic Program Repair`
- `The Art of Repair: Optimizing Iterative Program Repair with Instruction-Tuned Models`
- `TraceFixer: Execution Trace-Driven Program Repair`
- `TSAPR: A Tree Search Framework For Automated Program Repair`
- `Is ChatGPT the ultimate programming assistant--how far is it?`

Two retained systems have archival venue hints outside the configured venue families and are therefore intentionally left as arXiv records for the venue-count figure: `LLM4CVE` has a DSD 2025 DOI, and `The Art of Repair` has an EASE 2025 DOI.

Current conversion and retention audit for these retained arXiv records:

| Retained arXiv record | Current status | Retention rationale |
|---|---|---|
| `Agent That Debugs: Dynamic State-Guided Vulnerability Repair` | DBLP and arXiv list only the CoRR/arXiv version. | Retained as a vulnerability-repair system with a concrete dynamic-state-guided LLM repair pipeline and benchmark evidence. |
| `Enhancing repository-level software repair via repository-aware knowledge graphs` | DBLP and arXiv list only the CoRR/arXiv version. | Retained as a repository-level repair system because it reports SWE-bench Lite evidence and is central to the RAG/procedural benchmark analysis. |
| `LLM-Powered Code Vulnerability Repair with Reinforcement Learning and Semantic Reward` | DBLP and arXiv list only the CoRR/arXiv version. | Retained as an RLFT-style vulnerability-repair system with semantic reward design and reported repair results. |
| `LLM4CVE: Enabling Iterative Automated Vulnerability Repair with Large Language Models` | Has a DSD 2025 DOI, but DSD is outside the configured venue families for the manuscript figure. | Retained as an iterative LLM-based vulnerability-repair system; cited as arXiv in the manuscript because the archival hint is outside the configured CCF-A venue families. |
| `NARRepair: Non-Autoregressive Code Generation Model for Automatic Program Repair` | DBLP and arXiv list only the CoRR/arXiv version. | Retained because it represents non-autoregressive/distillation-style LLM repair and reports Defects4J repair results. |
| `The Art of Repair: Optimizing Iterative Program Repair with Instruction-Tuned Models` | Has an EASE 2025 DOI, but EASE is outside the configured venue families for the manuscript figure. | Retained because it reports iterative instruction-tuned repair on HumanEval-Java; cited as arXiv because EASE is outside the configured CCF-A venue families. |
| `TraceFixer: Execution Trace-Driven Program Repair` | DBLP and arXiv list only the CoRR/arXiv version. | Retained as an execution-trace-driven repair system that supports the analysis-augmented repair dimension. |
| `TSAPR: A Tree Search Framework For Automated Program Repair` | Indexed as an arXiv preprint; no in-scope archival version was found. | Retained because it contributes tree-search and LLM-as-judge repair evidence on Defects4J. |
| `Is ChatGPT the ultimate programming assistant--how far is it?` | DBLP and arXiv list only the CoRR/arXiv version. | Retained as an early benchmarked ChatGPT repair study that anchors the prompting baseline in the 2023 corpus. |

## Legacy stage-6 retained-list repair-scope check

The released `remote_results/stage6.jsonl` file is the legacy 62-record retained-list snapshot described in `screening_transparency.md`; the current 66-system corpus is defined by `selection_reference_474_final_adjudicated.csv`, `taxonomy_assignment_audit.csv`, and `scenario_assignment_audit.csv`. Within the legacy stage-6 snapshot, the retained-list slot previously occupied by the vulnerability-detection record `Smart-LLaMA-DPO` now points to the retained repair paper `Vul-R2`, which already appeared in the public candidate logs and in the manuscript itself. This keeps the legacy snapshot repair-focused while avoiding the incorrect implication that `stage6.jsonl` alone contains all 66 current manuscript systems.
