# Search Keywords and Automatic Filters

This file maps the paper-level search description to the executable implementation in `remote_results/pipeline.py`.

Canonical source:

- `remote_results/pipeline.py`

Key lists defined there:

- `APR_TERMS`: core software-repair phrases such as `program repair`, `automatic program repair`, `bug fixing`, `patch generation`, `code repair`, and `vulnerability repair`.
- `LLM_TERMS`: model-family cues such as `large language model`, `GPT`, `CodeT5`, `StarCoder`, `LLaMA`, `DeepSeek`, `Claude`, `InCoder`, `CodeGen`, and `BERT`.
- `BENCH_TERMS`: benchmark or dataset cues such as `Defects4J`, `SWE-bench`, `SWE-bench Lite`, `SWE-bench Verified`, `QuixBugs`, `HumanEval-Java`, `BugsInPy`, `CVEFixes`, `DS-1000`, `xCodeEval`, and others.
- `TOOL_TERMS`: explicit tool or system names such as `RepairAgent`, `AutoCodeRover`, `SWE-Agent`, `OpenHands`, `LANTERN`, `ChatRepair`, `ThinkRepair`, `Agentless`, `D4C`, `SpecRover`, and `Abstain and Validate`.

Automatic filtering cues defined there:

- `ABSTRACT_POSITIVE_HINTS`: broad APR-positive expressions, including repair, fix, vulnerability-patching, issue-resolution, and agent-oriented wording.
- `EVAL_HINTS`: evaluation-oriented words such as `benchmark`, `dataset`, `experiment`, `results`, and `performance`.
- stage-3 screening functions such as `has_positive_abstract`, `has_quantitative_success_signals`, `mentions_llm`, and `mentions_known_benchmark`.

How this relates to the paper:

- Table 1 in the paper summarizes the representative keyword families for readability.
- `remote_results/pipeline.py` is the canonical executable definition of the actual keyword pools and screening functions.
- The revised paper adds explicit tool-name examples such as `SpecRover` and `Abstain and Validate` precisely because repository-level and agent-oriented papers sometimes foreground system names more strongly than the phrase `program repair`.
