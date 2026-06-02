#!/usr/bin/env python3
"""
反向同步：questions/q-*.md → quiz-data.json + quiz-index.json

用途：
  当你直接编辑 questions/q-*.md 补充答案后，运行本脚本把答案回写到 JSON，
  这样前端 quiz.html / index.html 能立刻显示。

用法：
  python3 sync_answers.py
"""
from pathlib import Path
from datetime import datetime
import re
import json
import sys
import yaml

ROOT = Path(__file__).parent
QUESTIONS_DIR = ROOT / "questions"
DATA_JSON = ROOT / "quiz-data.json"
INDEX_JSON = ROOT / "quiz-index.json"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
ANSWER_HEADING_RE = re.compile(r"^##\s*答案\s*$", re.MULTILINE)


def parse_md(path: Path):
    """返回 (id, hasAnswer, answer_text) 或 None"""
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fm_str, body = m.group(1), m.group(2)
    try:
        fm = yaml.safe_load(fm_str) or {}
    except yaml.YAMLError as e:
        print(f"⚠️  {path.name}: frontmatter 解析失败: {e}", file=sys.stderr)
        return None

    qid = fm.get("id")
    has_answer = bool(fm.get("hasAnswer"))

    # 取 "## 答案" 之后到下一个 H1/H2（或文件结束）的所有内容
    ans_match = ANSWER_HEADING_RE.search(body)
    if not ans_match:
        return qid, has_answer, ""
    after = body[ans_match.end():].lstrip("\n")

    # 截断到下一个一级或二级标题（如果有）
    next_h = re.search(r"^(#|##)\s+\S", after, re.MULTILINE)
    if next_h:
        after = after[: next_h.start()]

    answer = after.strip()

    # frontmatter 标 true 但正文是"（待补充）"的情况，强制 false
    if answer in ("（待补充）", "(待补充)", ""):
        return qid, False, ""

    return qid, has_answer, answer


def main():
    if not DATA_JSON.exists():
        print(f"❌ 找不到 {DATA_JSON}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    index = json.loads(INDEX_JSON.read_text(encoding="utf-8")) if INDEX_JSON.exists() else None

    # 索引化方便回写
    by_id_data = {q["id"]: q for q in data}
    by_id_index = None
    if index is not None:
        # quiz-index.json 顶层可能是 dict 含 questions
        if isinstance(index, dict) and "questions" in index:
            by_id_index = {q["id"]: q for q in index["questions"]}
        elif isinstance(index, list):
            by_id_index = {q["id"]: q for q in index}

    md_files = sorted(QUESTIONS_DIR.glob("q-*.md"))
    print(f"📄 扫描 {len(md_files)} 个 markdown 文件…")

    updated_data = 0
    updated_index = 0
    added_data = 0
    missing_in_data = []
    answered_total = 0

    for md in md_files:
        parsed = parse_md(md)
        if not parsed:
            continue
        qid, has_answer, answer = parsed
        if not qid:
            continue
        if has_answer:
            answered_total += 1

        # 更新 quiz-data.json
        if qid in by_id_data:
            q = by_id_data[qid]
            if q.get("hasAnswer") != has_answer or q.get("answer") != answer:
                q["hasAnswer"] = has_answer
                q["answer"] = answer
                updated_data += 1
        else:
            missing_in_data.append(qid)

        # 更新 quiz-index.json（如果存在）
        if by_id_index is not None and qid in by_id_index:
            q = by_id_index[qid]
            if q.get("hasAnswer") != has_answer:
                q["hasAnswer"] = has_answer
                updated_index += 1

    # 写回
    DATA_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"✅ 写回 quiz-data.json：更新 {updated_data} 题")

    if index is not None:
        # 同步 stats / metadata 计数（兼容两种命名）
        today = datetime.now().strftime("%Y-%m-%d")
        if isinstance(index, dict) and by_id_index is not None:
            ans = sum(1 for q in by_id_index.values() if q.get("hasAnswer"))
            pend = len(by_id_index) - ans
            for key in ("stats", "metadata"):
                m = index.get(key)
                if isinstance(m, dict):
                    m["answeredQuestions"] = ans
                    m["pendingQuestions"] = pend
                    m["lastUpdated"] = today
            meta = index.get("meta")
            if isinstance(meta, dict):
                meta["lastUpdated"] = today
        INDEX_JSON.write_text(
            json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"✅ 写回 quiz-index.json：更新 {updated_index} 题")

    print(f"📊 已答题总数（按 frontmatter hasAnswer:true 算）：{answered_total}")
    if missing_in_data:
        print(f"⚠️  {len(missing_in_data)} 个 md 在 quiz-data.json 里找不到（前 5 个）：{missing_in_data[:5]}")


if __name__ == "__main__":
    main()
