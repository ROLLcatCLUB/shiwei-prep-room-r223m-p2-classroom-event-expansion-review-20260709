# R223M-P2 GPT Review Guide

```text
stage_id=1013R_R223M_P2_CLASSROOM_EVENT_EXPANSION_AND_STUDENT_RESPONSE_PREDICTION
status=classroom_event_expansion_review_package
formal_ui=blocked
R97B / UI / runtime / prompt / model / db = untouched
```

## What To Review First

Open this file first:

```text
R223M_P2_teacher_readable_process_v3.html
```

Judge it as a teacher-facing classroom process draft, not as a UI mock.

Core question:

```text
Does the classroom actually unfold now?
```

## Review Order

1. Read `R223M_P2_teacher_readable_process_v3.html`.
2. Check whether the seven classroom events are readable as a continuous teaching process.
3. Read `R223M_P2_classroom_event_expansion_matrix.json` only after reading the main draft.
4. Use `R223M_P2_student_response_prediction_matrix.md` to audit student response realism.
5. Use `R223M_P2_classroom_depth_check.md` and `validate_1013R_R223M_P2_classroom_event_expansion_result.json` for verification.

## Hard Review Points

```text
1. 课堂过程是否真正展开；
2. 学生可能反应是否真实；
3. 教师追问和补救是否具体；
4. 是否能看出一年级学情；
5. 素材、大屏、学习单、评价证据是否自然嵌入；
6. 最终主稿是否仍然是连续教师稿，而不是卡片墙。
```

## Boundary

This package does not authorize formal UI.

```text
No R97B modification.
No formal route.
No frontend/backend implementation.
No runtime/provider/model/prompt/database.
No lesson body writeback.
No R224.
No formal apply.
```

## Possible Decisions

```text
R223M-P2 = PASS_CLASSROOM_EVENT_EXPANSION_REVIEW
R223M-P2 = HOLD_FOR_CLASSROOM_EVENT_REWRITE
R223M-P2 = HOLD_FOR_TEACHER_READABILITY_COMPRESSION
FORMAL_UI = BLOCKED
```
