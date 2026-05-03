# 人工双标注说明

这套材料是给两位人工标注者做独立复核用的，目标是对当前 survey 里的 taxonomy 和 scenario 进行真正的双人标注，并留下后续可计算一致性统计的位置。

## 需要用到的文件

- `taxonomy_coding_guide.md`
  作用：定义 `primary_paradigm`、`control_subparadigm`、`retrieval_tag`、`analysis_tag` 的判定规则
- `scenario_assignment_audit.csv`
  作用：说明论文里采用的 deployment scenario 体系
- `human_taxonomy_annotation_template.csv`
  作用：正式标注表，已经留好了 coder 1、coder 2 和 adjudication 的空位
- `compute_annotation_agreement.py`
  作用：在两位标注者填完后，直接计算 kappa、原始一致率和分歧条目

## 两位标注者各自要填什么

每个 system 都需要独立填写以下字段：

- `primary_paradigm`
  可选值：`Fine-Tuning`、`Prompting`、`Procedural`、`Agentic`
- `control_subparadigm`
  尽量使用当前论文里的控制方式标签
- `retrieval_tag`
  填 `yes` 或 `no`
- `analysis_tag`
  填 `yes` 或 `no`
- `primary_scenario`
  可选值：
  - `Localized benchmark repair`
  - `Repository-level issue resolution`
  - `Vulnerability repair`
  - `Educational tutoring`
  - `Industrial / practitioner workflow`
- `evidence_location`
  写证据位置，比如 “method section”, “evaluation setup”, “Figure 2”, “Appendix A”
- `rationale`
  用一句短话写明为什么这样判

## 标注纪律

1. 两位标注者必须独立完成，不要互相看对方结果。
2. `adjudicated_*`、`adjudicator`、`adjudication_basis` 这些列在双标注结束前不要动。
3. 遇到边界案例不要跳过，先给出自己的最终判断，再在 `rationale` 里写不确定点。
4. 真正需要讨论和第三方裁决的，只放到双标注完成之后。

## 推荐流程

1. 先读 `taxonomy_coding_guide.md`
2. 各自独立填写 `human_taxonomy_annotation_template.csv`
3. 填完后运行：

```bash
python3 artifact/compute_annotation_agreement.py artifact/human_taxonomy_annotation_template.csv
```

4. 看脚本输出的分歧项
5. 对分歧项讨论，或者交给第三人裁决
6. 把裁决结果写入 `adjudicated_*`、`adjudicator`、`adjudication_basis`

## 你回传给我什么

你只需要把填好的 `human_taxonomy_annotation_template.csv` 给我。我收到后可以直接：

- 计算 `primary_paradigm` 的 Cohen's kappa
- 统计 `retrieval_tag` / `analysis_tag` 的一致性
- 统计 `primary_scenario` 的原始一致率
- 列出具体分歧系统
- 帮你把这些数字写进论文正文或 artifact 说明

## 说明

- 这是一轮当前 taxonomy 的人类复核包，不是对最初 screening 过程的事后伪造。
- 因为原始 screening ledger 不在当前公开仓库里，这一轮能提供的是新的、可核查的人工双标注证据。
