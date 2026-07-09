from pathlib import Path
import html

root = Path(__file__).resolve().parent
md_path = root / "R223M_P2_teacher_readable_process_v3.md"
out = root / "R223M_P2_teacher_readable_process_v3.html"

text = md_path.read_text(encoding="utf-8")
lines = text.splitlines()
heading = next((line[2:].strip() for line in lines if line.startswith("# ")), "R223M-P2 teacher readable process v3")
first_para = next(
    (
        line.strip()
        for line in lines
        if line.strip()
        and not line.startswith("#")
        and not line.startswith("```")
        and not line.startswith("stage_id")
        and not line.startswith("status=")
        and not line.startswith("source=")
        and not line.startswith("formal_ui")
        and not line.startswith("R97B")
    ),
    "",
)

body = []
in_fence = False
pre_lines = []
for line in lines:
    if line.strip().startswith("```"):
        if not in_fence:
            in_fence = True
            pre_lines = []
        else:
            body.append('<pre class="meta-block">' + html.escape("\n".join(pre_lines)) + "</pre>")
            in_fence = False
        continue
    if in_fence:
        pre_lines.append(line)
        continue
    if not line.strip():
        continue
    if line.startswith("# "):
        body.append(f"<h1>{html.escape(line[2:].strip())}</h1>")
    elif line.startswith("## "):
        body.append(f"<section><h2>{html.escape(line[3:].strip())}</h2>")
    elif line.startswith("### "):
        body.append(f"<h3>{html.escape(line[4:].strip())}</h3>")
    else:
        raw = line.strip()
        klass = "section-purpose" if raw.startswith("【环节说明】") else ("intention" if raw.startswith("【") else "")
        body.append(f'<p class="{klass}">{html.escape(raw)}</p>')

html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(heading)}</title>
<style>
:root{{--ink:#1e2f2a;--muted:#64766f;--line:#d9e5df;--paper:#fffef9;--bg:#f5f8f5;--accent:#227866;--soft:#edf7f3;--warn:#f6ead3;}}
*{{box-sizing:border-box;overflow-wrap:anywhere;}}
body{{margin:0;background:linear-gradient(90deg,rgba(34,120,102,.045) 1px,transparent 1px),linear-gradient(rgba(34,120,102,.045) 1px,transparent 1px),var(--bg);background-size:24px 24px;color:var(--ink);font-family:"Microsoft YaHei","PingFang SC",Arial,sans-serif;letter-spacing:0;}}
.shell{{max-width:1120px;margin:0 auto;padding:36px 28px 58px;}}
.paper{{background:var(--paper);border:1px solid var(--line);border-radius:8px;box-shadow:0 22px 62px rgba(31,63,55,.13);padding:46px 68px 56px;}}
.kicker{{color:var(--accent);font-weight:800;font-size:14px;margin-bottom:12px;}}
h1{{font-size:34px;line-height:1.3;margin:0 0 18px;color:#162922;}}
.summary{{font-size:16px;line-height:1.9;color:var(--muted);border-bottom:2px solid #b9d7cd;padding-bottom:20px;margin-bottom:28px;}}
.chips{{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 26px;}}
.chips span{{border:1px solid #c8dfd7;background:var(--soft);color:#155b4d;border-radius:999px;padding:5px 12px;font-size:12px;font-weight:700;}}
article{{max-width:890px;margin:0 auto;}}
section{{display:block;margin:30px 0;}}
h2{{margin:0 0 14px;font-size:23px;line-height:1.45;color:#162821;padding-left:13px;border-left:5px solid var(--accent);}}
h3{{margin:30px 0 10px;font-size:20px;line-height:1.5;color:#145e50;}}
p{{margin:0 0 15px;font-size:16px;line-height:2.08;text-align:justify;}}
.section-purpose{{margin:0 0 16px;padding:10px 14px;background:#eef7f3;border-left:4px solid #70a999;color:#2f5148;font-size:15px;line-height:1.85;text-align:left;}}
.intention{{margin:14px 0 20px;padding:13px 16px;background:#f2faf6;border-left:4px solid #86bbab;color:#36534b;font-size:15px;line-height:1.9;}}
.meta-block{{background:#102a24;color:#e7f5ef;border-radius:8px;padding:16px 20px;font-size:13px;line-height:1.7;white-space:pre-wrap;margin:14px 0 24px;word-break:break-word;}}
.note{{margin-top:30px;background:var(--warn);border:1px solid #ead59b;border-radius:8px;padding:14px 18px;color:#6b5418;font-size:14px;line-height:1.8;}}
.footer{{margin-top:30px;text-align:center;color:var(--muted);font-size:12px;}}
@media (max-width: 760px){{.shell{{padding:18px 12px 32px;}}.paper{{padding:28px 20px 36px;}}h1{{font-size:27px;}}h2{{font-size:20px;}}p{{font-size:15px;line-height:1.95;}}}}
</style>
</head>
<body data-stage-id="1013R_R223M_P2_CLASSROOM_EVENT_EXPANSION_AND_STUDENT_RESPONSE_PREDICTION" data-formal-ui="false" data-card-wall="false" data-classroom-event-expansion="true" data-r97b-modified="false">
<main class="shell"><div class="paper"><div class="kicker">师维智教 · 教师可读课堂过程稿 · 静态审核</div><div class="summary">{html.escape(first_para or '本页只展示 R223M-P2 的课堂事件展开稿，不是正式 UI。')}</div><div class="chips"><span>课堂事件展开</span><span>学生反应预判</span><span>教师追问与补救</span><span>连续教师稿</span><span>formal UI blocked</span></div><article>
{''.join(body)}
</article><div class="note">边界：R223M-P2 只做静态内容产物和审核包；不改 R97B，不新增正式 route，不改 frontend/backend，不接 runtime/model/prompt/db，不写回 lesson body，不启动 R224，不 formal apply。</div></div><div class="footer">R223M-P2 classroom event expansion and student response prediction · fixture/static only</div></main>
</body></html>
"""

out.write_text(html_doc, encoding="utf-8")
print(out)
