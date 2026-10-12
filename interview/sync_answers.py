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
import json
import sys
from question_bank import load_question_bank, read_question

ROOT = Path(__file__).parent
QUESTIONS_DIR = ROOT / "questions"
DATA_JSON = ROOT / "quiz-data.json"
INDEX_JSON = ROOT / "quiz-index.json"


def parse_md(path: Path):
    """兼容原入口，返回题号、完成状态和不截断的完整答案。"""
    meta, answer = read_question(path)
    return meta["id"], meta["hasAnswer"], answer


def main():
    """校验所有单题后同步答案与统计，保留题号、分类和浏览器学习记录。"""
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

    bank = load_question_bank(QUESTIONS_DIR)
    if len(by_id_data) != len(data):
        raise ValueError("quiz-data.json 存在重复题号，请先运行 parse_questions.py")
    if set(bank) != set(by_id_data):
        raise ValueError("Markdown 与 JSON 题号不一致，请先运行 parse_questions.py")
    if by_id_index is not None and set(by_id_index) != set(by_id_data):
        raise ValueError("两个 JSON 题号不一致，请先运行 parse_questions.py")
    print(f"📄 扫描 {len(bank)} 个 markdown 文件…")

    updated_data = 0
    updated_index = 0
    answered_total = 0

    for qid, (meta, answer) in bank.items():
        has_answer = meta["hasAnswer"]
        if has_answer:
            answered_total += 1

        # 更新 quiz-data.json
        if qid in by_id_data:
            q = by_id_data[qid]
            if q.get("hasAnswer") != has_answer or q.get("answer") != answer:
                q["hasAnswer"] = has_answer
                q["answer"] = answer
                updated_data += 1

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


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
