# R223M-P2 Before / After Compare With R223M-P1

```text
stage_id=1013R_R223M_P2_CLASSROOM_EVENT_EXPANSION_AND_STUDENT_RESPONSE_PREDICTION
compare_target=R223M-P1_SOURCE_ANCHORED_TEACHER_DRAFT_HARDENING
```

## What P1 Solved

```text
教师稿形态成立。
源文档锚定完成。
gold sample 活动语言恢复。
评价表证据对齐。
主稿不是卡片墙。
```

## What P2 Adds

| Layer | P1 | P2 |
| --- | --- | --- |
| 环节描述 | 写出活动名称、教师行为、学生行为 | 展开课堂事件、学生反应、教师应对 |
| 学情使用 | 总体说明一年级特点 | 每个环节预判一年级常见偏差 |
| 教师话术 | 有关键提问 | 增加追问、补救、收束和过渡 |
| 证据采集 | 写出证据类型 | 指出证据采集时机和课堂来源 |
| 素材/大屏 | 准备项和环节落点 | 明确何时投屏、何时比较、何时示范 |
| 主稿形态 | 连续教师稿 | 继续保持连续教师稿，不做卡片墙 |

## Key Improvement

R223M-P2 makes the missing layer explicit:

```text
环节责任
→ 课堂事件
→ 学生可能反应
→ 学生可能偏差
→ 教师追问和补救
→ 投屏 / 示范 / 比较时机
→ 证据采集
→ 收束过渡
```

## Boundary

This is still a static teacher-draft hardening stage. It does not authorize UI,
R97B changes, runtime generation, provider/model calls, prompt changes,
database writes, lesson body writeback, R224, or formal apply.

