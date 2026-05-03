# 474 篇筛选复核标注说明

这套表用于做 independent re-screening audit，目标是复核当前稿件 screening flow 中 474 条 full-text screening 候选记录中哪些应纳入最终 LLM-based software repair survey。

## 文件

- `screening_annotation_template_474.csv`: 空白双人标注表，给两位标注者填写。
- `screening_reference_labels_474.csv`: 当前论文最终筛选结果对应的 reference 表。该表只表示当前稿件的最终 include/exclude 状态，不是原始 screening ledger。
- `remote_results/stage5.jsonl`: 冻结基线中的 462 条候选记录来源。
- `artifact/version_status_audit.md`: 正式出版更新和版本状态说明。
- `artifact/taxonomy_assignment_audit.csv`: 当前论文最终保留的 66 条记录来源。

## 标注任务

每位标注者独立阅读每条记录的 title、abstract、venue、url，必要时打开全文，填写自己的字段：

- `coder_1_decision` / `coder_2_decision`: 填 `include` 或 `exclude`。
- `coder_1_exclusion_reason` / `coder_2_exclusion_reason`: 如果 exclude，填写下面的排除原因之一。
- `coder_1_evidence_location` / `coder_2_evidence_location`: 证据位置，例如 `title/abstract`、`method section`、`evaluation section`、`full text unavailable`。
- `coder_1_notes` / `coder_2_notes`: 简短说明边界情况。

## Include 标准

标为 `include` 需要同时满足：

1. 研究对象是软件缺陷修复、程序修复、漏洞修复、repository issue resolution、patch generation 或紧密相关的自动修复任务。
2. LLM 或大型代码模型在推理时是修复流程的核心组成部分。
3. 论文报告了可提取的实证评估，例如 benchmark、dataset、issue suite、real-world bugs、pass@k、fix rate、F1、CodeBLEU、merged PRs 等。
4. 论文在 2022 年至 2026 年 4 月的检索窗口内，或是当前更新候选文件中已保留的相关记录。
5. 不是 survey、position paper、纯 benchmark paper、纯 bug detection/localization paper、纯代码生成 paper，除非它明确提出并评估 LLM-based repair system。

## Exclusion reason 可选值

- `survey_or_review`
- `not_software_repair`
- `detection_or_localization_only`
- `benchmark_or_evaluation_only`
- `llm_not_central_to_repair`
- `no_patch_generation_or_repair_pipeline`
- `no_reproducible_quantitative_repair_evaluation`
- `duplicate_or_less_complete_version`
- `out_of_scope_year_or_venue`
- `full_text_unavailable_or_insufficient_detail`
- `other_unclear`

## 裁决

两位标注者完成后，再比较分歧。分歧项由第三人或讨论后填写：

- `adjudicated_decision`
- `adjudicated_exclusion_reason`
- `adjudicator`
- `adjudication_basis`

## 报告口径

这是一轮新增的可核查筛选复核，建议称为 `independent re-screening audit`。不要把它写成原始提交时的 human screening kappa。
