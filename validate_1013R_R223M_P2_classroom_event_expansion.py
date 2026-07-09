#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


STAGE_ID = "1013R_R223M_P2_CLASSROOM_EVENT_EXPANSION_AND_STUDENT_RESPONSE_PREDICTION"

REQUIRED_FILES = [
    "R223M_P2_classroom_event_expansion_matrix.json",
    "R223M_P2_student_response_prediction_matrix.md",
    "R223M_P2_teacher_readable_process_v3.md",
    "R223M_P2_teacher_readable_process_v3.html",
    "R223M_P2_teacher_readable_process_v3_screenshot.png",
    "R223M_P2_screenshot_smoke_result.json",
    "R223M_P2_before_after_compare_with_R223M.md",
    "R223M_P2_classroom_depth_check.md",
    "R223M_P2_report.md",
    "README_FOR_GPT_REVIEW.md",
    "README.md",
]

EVENT_NAMES = [
    "忆一忆：毛笔的诞生",
    "探一探：关键的结构 / 十万个为什么",
    "设计会：像设计师一样思考",
    "试一试：1+1 合作小设计",
    "创一创：1+n 文具大变身",
    "笔友汇",
    "赠笔礼",
]

EVENT_KEYS = [
    "event_id",
    "event_name",
    "teaching_responsibility",
    "task_release_talk",
    "expected_student_responses",
    "likely_deviations",
    "teacher_follow_up_strategy",
    "remediation_strategy",
    "demo_projection_timing",
    "evidence_capture",
    "closing_talk",
    "transition_to_next",
]

MAIN_TEXT_REQUIRED = [
    "学生可能",
    "追问",
    "如果学生",
    "投屏",
    "证据",
    "收束",
    "过渡",
    "一年级",
    "学习单",
    "评价表",
]

FORBIDDEN_TEXT = [
    "正式 UI 已放行",
    "formal UI approved",
    "R97B route implemented",
    "provider call enabled",
    "database write enabled",
    "R224 started",
    "问我任何问题",
    "组件货架",
]


def read_text(root: Path, name: str) -> str:
    return (root / name).read_text(encoding="utf-8")


def add_check(checks: list[dict], name: str, passed: bool, detail: str = "") -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def validate(root: Path) -> dict:
    checks: list[dict] = []

    for name in REQUIRED_FILES:
        path = root / name
        add_check(checks, f"required_file::{name}", path.exists(), "exists" if path.exists() else "missing")

    matrix_path = root / "R223M_P2_classroom_event_expansion_matrix.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    add_check(checks, "stage_id_matches", matrix.get("stage_id") == STAGE_ID)
    add_check(checks, "formal_ui_false", matrix.get("formal_ui") is False)
    boundary = matrix.get("boundary", {})
    add_check(checks, "r97b_unmodified", boundary.get("r97b_modified") is False)
    add_check(checks, "runtime_prompt_db_blocked", boundary.get("runtime_model_prompt_db") is False)
    add_check(checks, "teacher_main_draft_continuous", boundary.get("teacher_main_draft_should_be_continuous") is True)
    add_check(checks, "card_wall_not_allowed", boundary.get("card_wall_allowed") is False)

    events = matrix.get("event_model", [])
    add_check(checks, "event_count_is_7", len(events) == 7, f"count={len(events)}")
    seen_names = [event.get("event_name") for event in events]
    for event_name in EVENT_NAMES:
        add_check(checks, f"event_present::{event_name}", event_name in seen_names)

    for index, event in enumerate(events, start=1):
        for key in EVENT_KEYS:
            value = event.get(key)
            ok = bool(value) and (not isinstance(value, list) or len(value) >= 1)
            add_check(checks, f"event_{index:02d}_has::{key}", ok)
        for list_key in ["expected_student_responses", "likely_deviations", "teacher_follow_up_strategy", "remediation_strategy"]:
            value = event.get(list_key)
            add_check(checks, f"event_{index:02d}_{list_key}_multiple", isinstance(value, list) and len(value) >= 2)

    main_md = read_text(root, "R223M_P2_teacher_readable_process_v3.md")
    main_html = read_text(root, "R223M_P2_teacher_readable_process_v3.html")
    student_matrix = read_text(root, "R223M_P2_student_response_prediction_matrix.md")
    depth_check = read_text(root, "R223M_P2_classroom_depth_check.md")
    report = read_text(root, "R223M_P2_report.md")

    for phrase in EVENT_NAMES:
        short_phrase = phrase.split(" / ")[0]
        add_check(checks, f"main_md_has_event::{short_phrase}", short_phrase in main_md)

    for phrase in MAIN_TEXT_REQUIRED:
        add_check(checks, f"main_md_has_classroom_depth::{phrase}", phrase in main_md)

    for phrase in ["学生常见反应", "学生可能偏差", "教师应对", "证据采集"]:
        add_check(checks, f"student_matrix_has::{phrase}", phrase in student_matrix)

    for phrase in ["PASS", "课堂过程是否真正展开", "学生可能反应是否真实", "教师追问和补救是否具体"]:
        add_check(checks, f"depth_check_has::{phrase}", phrase in depth_check)

    for phrase in ["R223M_CLASSROOM_EVENT_EXPANSION", "NOT_PASS -> addressed", "formal_ui=blocked"]:
        add_check(checks, f"report_has::{phrase}", phrase in report)

    add_check(checks, "html_stage_attr", f'data-stage-id="{STAGE_ID}"' in main_html)
    add_check(checks, "html_formal_ui_false", 'data-formal-ui="false"' in main_html)
    add_check(checks, "html_card_wall_false", 'data-card-wall="false"' in main_html)
    add_check(checks, "html_classroom_event_expansion_true", 'data-classroom-event-expansion="true"' in main_html)
    for forbidden_class in ["component-card", "chain-node", "decision-card"]:
        add_check(checks, f"html_no_card_wall_class::{forbidden_class}", forbidden_class not in main_html)
    add_check(checks, "html_no_card_wall_class_attr", 'class="card-wall"' not in main_html)

    smoke = json.loads((root / "R223M_P2_screenshot_smoke_result.json").read_text(encoding="utf-8"))
    add_check(checks, "smoke_stage_matches", smoke.get("stage") == STAGE_ID)
    add_check(checks, "smoke_no_horizontal_overflow", smoke.get("horizontalOverflow") is False)
    add_check(checks, "smoke_card_wall_false", smoke.get("cardWall") == "false")
    add_check(checks, "smoke_classroom_event_expansion_true", smoke.get("classroomEventExpansion") == "true")
    for key, value in smoke.get("hasText", {}).items():
        add_check(checks, f"smoke_has_text::{key}", value is True)
    for key, value in smoke.get("forbiddenSignals", {}).items():
        add_check(checks, f"smoke_forbidden_absent::{key}", value is False)

    all_text = "\n".join([main_md, main_html, student_matrix, depth_check, report])
    for phrase in FORBIDDEN_TEXT:
        add_check(checks, f"forbidden_absent::{phrase}", phrase not in all_text)

    failed = [check for check in checks if not check["passed"]]
    return {
        "stage_id": STAGE_ID,
        "passed": not failed,
        "check_count": len(checks),
        "failed": len(failed),
        "failed_checks": failed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Directory containing R223M-P2 review artifacts")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    result = validate(root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
