#!/usr/bin/env python3
"""
面试题解析脚本 —— MD 内容源 + JSON 索引层 分离架构

Windows 编码兼容：若 stdout 不是 utf-8，自动重配置

用法:
  python parse_questions.py                  # 解析 _src/ 下所有 quiz-*.md
  python parse_questions.py quiz-main.md     # 只解析指定文件
  python parse_questions.py quiz-main.md quiz-agent-pending.md

输出:
  1. questions/q-{id}.md    — 每题独立 Markdown（内容源，可独立拆分）
  2. quiz-index.json        — 轻量索引（列表/筛选/搜索）
  3. quiz-data.json         — 完整数据（兼容现有 quiz.html）

题库文件命名规范：
  quiz-[scope]-[status].md
    scope: 主题范围，如 main / agent / rag / deploy / algo
    status（可选）: pending 表示待补充答案
"""

import sys
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import json
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

SRC_DIR = Path(__file__).parent / "_src"
OUT_DIR = Path(__file__).parent
OUTPUT_FULL = OUT_DIR / "quiz-data.json"
OUTPUT_INDEX = OUT_DIR / "quiz-index.json"
QUESTIONS_DIR = OUT_DIR / "questions"

# 分类映射：中文名称 → 英文 key（支持完整名称及子分类）
category_key_map = {
    "RAG/检索": "rag",
    "RAG": "rag",
    "检索": "rag",
    "Agent/多智能体": "agent",
    "Agent": "agent",
    "多智能体": "agent",
    "大模型原理": "llm-theory",
    "推理优化/部署": "deploy",
    "推理优化": "deploy",
    "部署": "deploy",
    "NL2SQL/数据": "nl2sql",
    "NL2SQL": "nl2sql",
    "数据": "nl2sql",
    "知识图谱": "kg",
    "编程基础": "coding",
    "系统设计": "system-design",
    "综合": "mixed",
}

# key → 显示名称（聚合索引用）
category_display_map = {
    "rag": "RAG/检索",
    "agent": "Agent/多智能体",
    "llm-theory": "大模型原理",
    "deploy": "推理优化/部署",
    "nl2sql": "NL2SQL/数据",
    "kg": "知识图谱",
    "coding": "编程基础",
    "system-design": "系统设计",
    "mixed": "综合",
}


def clean_html(s: str) -> str:
    s = re.sub(r'<font[^>]*>', '', s)
    s = re.sub(r'</font>', '', s)
    s = re.sub(r'<[^>]+>', '', s)
    return s.strip()


def classify(question: str, answer: str) -> str:
    text = (question + " " + answer).lower()
    rules = [
        ("RAG/检索", ["rag", "检索", "向量", "召回", "embedding", "chunk", "分块", "索引", "es", "elasticsearch", "milvus", "chroma", "qdrant", "rerank", "嵌入", "相似度"]),
        ("Agent/多智能体", ["agent", "智能体", "langgraph", "langchain", "workflow", "state", "工具", "tool", "mcp", "skills", "function call", "调度", "对话栈", "tracker", "节点", "flow"]),
        ("大模型原理", ["transformer", "attention", "qkv", "位置编码", "梯度消失", "梯度爆炸", "bert", "gpt", "预训练", "微调", "sft", "rlhf", "ppo", "dpo", "grpo", "对齐", "量化", "损失函数", "交叉熵", "kl散度"]),
        ("推理优化/部署", ["vllm", "推理", "部署", "tensorrt", "加速", "显存", "gpu", "并行", "flashattention", "kv cache", "docker", "k8s", "fastapi", "flask", "websocket", "sse", "流式", "延迟", "qps", "tps", "压测"]),
        ("NL2SQL/数据", ["sql", "nl2sql", "数据库", "hive", "mysql", "binlog", "表", "字段", "元数据", "指标", "维度"]),
        ("知识图谱", ["图谱", "graphrag", "neo4j", "节点", "边", "关系", "实体", "属性", "多跳"]),
        ("编程基础", ["python", "list", "dict", "set", "tuple", "线程", "进程", "协程", "深浅拷贝", "装饰器", "leetcode", "排序算法", "手撕", "代码:", "code:", "秒撕", "二叉树", "链表", "数组与"]),
        ("系统设计", ["设计模式", "架构", "微服务", "并发", "锁", "连接池", "限流", "熔断", "消息队列", "kafka", "redis", "缓存"]),
    ]
    for cat, keywords in rules:
        if any(k in text for k in keywords):
            return cat
    return "综合"


def extract_tags(question: str, answer: str) -> list:
    text = (question + " " + answer).lower()
    tag_map = {
        "RAG": ["rag", "检索"],
        "向量检索": ["向量", "embedding"],
        "Agent": ["agent", "智能体"],
        "LangGraph": ["langgraph"],
        "LangChain": ["langchain"],
        "vLLM": ["vllm"],
        "Transformer": ["transformer", "attention"],
        "微调": ["微调", "sft", "lora"],
        "对齐": ["rlhf", "ppo", "dpo", "grpo"],
        "知识图谱": ["图谱", "graphrag", "neo4j"],
        "NL2SQL": ["nl2sql", "sql"],
        "推理优化": ["推理", "加速", "量化"],
        "Python": ["python"],
        "部署": ["docker", "k8s", "gpu"],
        "幻觉": ["幻觉"],
        "安全": ["安全", "脱敏", "权限"],
        "记忆": ["记忆", "上下文"],
        "分块": ["chunk", "分块"],
        "评估": ["评估", "benchmark", "ab测试"],
    }
    tags = []
    for tag, keywords in tag_map.items():
        if any(k in text for k in keywords):
            if tag not in tags:
                tags.append(tag)
    return tags[:3]


def parse_markdown(filepath: Path) -> list:
    """解析题库 dump，返回原始题目列表。"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    questions = []
    current_company = None
    current_category = None
    source_name = filepath.stem
    i = 0

    def is_question_line(line: str) -> bool:
        return bool(re.match(r'^\s*\d+[\.、]\s*\S', line))

    def extract_qtext(line: str) -> str:
        t = re.sub(r'^\s*\d+[\.、]\s*', '', line)
        t = clean_html(t)
        t = re.sub(r'\*\*', '', t)
        return t.strip()

    while i < len(lines):
        line = lines[i].strip()

        # 检测公司名
        company_match = None
        is_list_item = bool(re.match(r'^\s*\d+[\.、]\s*\S', line))
        if line.startswith("##") and not line.startswith("###"):
            m = re.search(r'^##\s*(.+)', line)
            if m:
                company_match = clean_html(m.group(1))
        elif not is_list_item and "**" in line and any(k in line for k in ["公司", "科技", "集团", "互联", "动力", "医疗", "车联网", "财经", "数字人", "机器人"]):
            c = clean_html(line.replace("**", ""))
            if len(c) < 40 and re.search(r'(公司|科技|集团|互联|动力|医疗|车联网|财经|数字人|机器人)[\s\)\）]*$', c):
                company_match = c
        elif not is_list_item and re.match(r'^[^\d\*#\-].+(公司|科技|集团|互联|动力|医疗|财经|数字人|机器人)$', line) and len(line) < 30:
            company_match = line

        if company_match and len(company_match) < 40:
            current_company = company_match
            current_category = None
            i += 1
            continue

        # 检测分类
        if re.match(r'^[一二三四五六七八九十]+[、\.\s]', line) or line.startswith("### "):
            cat = re.sub(r'^[一二三四五六七八九十]+[、\.\s]*', '', line)
            cat = re.sub(r'^#+\s*', '', cat)
            current_category = clean_html(cat)
            i += 1
            continue

        # 检测题目
        if is_question_line(line):
            q_text = extract_qtext(line)
            if len(q_text) < 5:
                i += 1
                continue

            answer_lines = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if not next_line:
                    j += 1
                    continue
                if is_question_line(next_line):
                    break
                if next_line.startswith("##") or (next_line.startswith("**") and "**" in next_line and len(clean_html(next_line)) < 40 and any(k in next_line for k in ["公司", "科技", "集团"])):
                    break
                if re.match(r'^[一二三四五六七八九十]+[、\.\s]', next_line) or next_line.startswith("### "):
                    break
                answer_lines.append(clean_html(next_line))
                j += 1

            answer = "\n".join(answer_lines)
            answer = re.sub(r'\*\*', '', answer)

            if True:  # 保留所有题目，无论是否有答案
                questions.append({
                    "company": current_company or "未知",
                    "category": current_category or "综合",
                    "question": q_text,
                    "answer": answer,
                    "source": source_name,
                })
            i = j
            continue

        i += 1

    return questions


def slugify_category(name: str) -> str:
    """分类中文名 → 英文 key。"""
    return category_key_map.get(name, "mixed")


def write_question_md(qid: str, rec: dict, out_path: Path):
    """生成单题独立 Markdown 文件。"""
    cat = rec["category"]
    cat_arr = [p.strip() for p in cat.split("/")]
    cat_key = slugify_category(cat_arr[0])
    cat_yaml = ", ".join(f'"{c}"' for c in cat_arr)
    tags = ", ".join(f'"{t}"' for t in rec["tags"])
    companies = ", ".join(f'"{c}"' for c in rec["companies"])
    has_answer = "true" if rec["hasAnswer"] else "false"
    created = rec.get("created", datetime.now().strftime("%Y-%m-%d"))

    fm = f"""---
id: {qid}
title: {rec["question"]}
category: [{cat_yaml}]
categoryKey: {cat_key}
tags: [{tags}]
companies: [{companies}]
frequency: {rec["frequency"]}
hot: {rec["hot"]}
hasAnswer: {has_answer}
source: {rec["source"]}
created: "{created}"
---

# {rec["question"]}

## 答案

{rec["answer"] if rec["answer"] else "（待补充）"}
"""
    out_path.write_text(fm, encoding="utf-8")


def is_question_dump(path: Path) -> bool:
    """题库 dump 以 `## 公司名` 开头；指南类文档以 `---` frontmatter 开头。"""
    if path.name.startswith("__"):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            first = f.readline().strip()
        return first.startswith("##")
    except OSError:
        return False


def main():
    if len(sys.argv) > 1:
        md_files = [SRC_DIR / f for f in sys.argv[1:]]
    else:
        md_files = [f for f in sorted(SRC_DIR.glob("*.md")) if is_question_dump(f)]

    md_files = [f for f in md_files if f.exists()]
    if not md_files:
        print(f"❌ 未找到 .md 文件")
        sys.exit(1)

    all_raw = []
    for f in md_files:
        print(f"📄 解析: {f.name}")
        all_raw.extend(parse_markdown(f))

    # 跨公司合并：相同题目（前 60 字符为 key）聚合 companies + 取最长答案
    merged = {}
    order = []
    for q in all_raw:
        key = q["question"][:60]
        company = q["company"].replace("（", "(").replace("）", ")")
        if company == "通用题库":
            company = "其他"
        if key not in merged:
            merged[key] = {
                "question": q["question"],
                "answer": q["answer"],
                "companies": [],
                "source": q["source"],
            }
            order.append(key)
        rec = merged[key]
        if company and company not in rec["companies"]:
            rec["companies"].append(company)
        if len(q["answer"].strip()) > len(rec["answer"].strip()):
            rec["answer"] = q["answer"]

    # 准备输出目录
    QUESTIONS_DIR.mkdir(parents=True, exist_ok=True)

    # 生成完整数据 + 索引
    full_results = []
    index_questions = []
    created_date = datetime.now().strftime("%Y-%m-%d")

    for idx, key in enumerate(order, 1):
        rec = merged[key]
        qid = f"q-{idx}"
        cat = classify(rec["question"], rec["answer"])
        cat_arr = [p.strip() for p in cat.split("/")]
        tags = extract_tags(rec["question"], rec["answer"])
        has_answer = len(rec["answer"].strip()) > 10
        freq = len(rec["companies"])
        hot = 2 if freq >= 4 else (1 if freq >= 2 else 0)
        cat_key = slugify_category(cat_arr[0])
        md_path = f"questions/{qid}.md"

        # 写入单题 MD
        write_question_md(qid, {
            "question": rec["question"],
            "category": cat,
            "tags": tags,
            "companies": rec["companies"],
            "frequency": freq if freq > 0 else 1,
            "hot": hot,
            "hasAnswer": has_answer,
            "source": rec["source"],
            "answer": rec["answer"] if has_answer else "",
            "created": created_date,
        }, QUESTIONS_DIR / f"{qid}.md")

        # 完整数据（兼容 quiz.html）
        full_results.append({
            "id": qid,
            "company": rec["companies"][0] if rec["companies"] else "未知",
            "companies": rec["companies"] or ["未知"],
            "frequency": freq if freq > 0 else 1,
            "hot": hot,
            "category": cat_arr,
            "title": rec["question"],
            "answer": rec["answer"] if has_answer else "",
            "hasAnswer": has_answer,
            "tags": tags,
        })

        # 索引数据（轻量）
        index_questions.append({
            "id": qid,
            "title": rec["question"],
            "mdPath": md_path,
            "categoryKey": cat_key,
            "categoryName": cat_arr,
            "companies": rec["companies"] or ["未知"],
            "frequency": freq if freq > 0 else 1,
            "hot": hot,
            "isHighFrequency": hot >= 1,
            "hasAnswer": has_answer,
            "tags": tags,
            "variants": [],
            "source": rec["source"],
        })

    # 聚合索引
    categories = defaultdict(lambda: {"name": "", "questionIds": []})
    companies_idx = defaultdict(lambda: {"name": "", "questionIds": []})
    tags_idx = defaultdict(lambda: {"name": "", "questionIds": []})

    for q in index_questions:
        seen_cat_keys = set()
        for c in q["categoryName"]:
            ck = slugify_category(c)
            if ck not in seen_cat_keys:
                seen_cat_keys.add(ck)
                categories[ck]["name"] = category_display_map.get(ck, c)
                categories[ck]["questionIds"].append(q["id"])

        for co in q["companies"]:
            companies_idx[co]["name"] = co
            companies_idx[co]["questionIds"].append(q["id"])

        for t in q["tags"]:
            tags_idx[t]["name"] = t
            tags_idx[t]["questionIds"].append(q["id"])

    categories_out = [
        {
            "key": k,
            "name": v["name"],
            "questionCount": len(v["questionIds"]),
            "highFrequencyCount": sum(1 for qid in v["questionIds"] if next((x for x in index_questions if x["id"] == qid), {}).get("isHighFrequency", False)),
            "questionIds": v["questionIds"],
        }
        for k, v in sorted(categories.items())
    ]

    companies_out = [
        {
            "name": v["name"],
            "questionCount": len(v["questionIds"]),
            "highFrequencyCount": sum(1 for qid in v["questionIds"] if next((x for x in index_questions if x["id"] == qid), {}).get("isHighFrequency", False)),
            "questionIds": v["questionIds"],
        }
        for v in sorted(companies_idx.values(), key=lambda x: -len(x["questionIds"]))
    ]

    tags_out = [
        {
            "name": v["name"],
            "questionCount": len(v["questionIds"]),
            "questionIds": v["questionIds"],
        }
        for v in sorted(tags_idx.values(), key=lambda x: -len(x["questionIds"]))
    ]

    stats = {
        "totalQuestions": len(index_questions),
        "totalCompanies": len(companies_idx),
        "totalCategories": len(categories),
        "totalTags": len(tags_idx),
        "highFrequencyQuestions": sum(1 for q in index_questions if q["isHighFrequency"]),
        "answeredQuestions": sum(1 for q in index_questions if q["hasAnswer"]),
        "pendingQuestions": sum(1 for q in index_questions if not q["hasAnswer"]),
        "lastUpdated": created_date,
    }

    index_data = {
        "meta": {
            "version": "1.0",
            "schema": "interview-quiz-index",
            "description": "LLM 工程师面试题库索引 —— JSON 负责列表/筛选/搜索，MD 负责内容承载",
            "lastUpdated": created_date,
        },
        "stats": stats,
        "categories": categories_out,
        "companies": companies_out,
        "tags": tags_out,
        "questions": index_questions,
    }

    # 写入文件
    with open(OUTPUT_FULL, "w", encoding="utf-8") as f:
        json.dump(full_results, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_INDEX, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ quiz-data.json    — 共 {len(full_results)} 道题目（兼容层）")
    print(f"✅ quiz-index.json   — 轻量索引（{len(categories_out)} 分类 / {len(companies_out)} 公司 / {len(tags_out)} 标签）")
    print(f"✅ questions/        — {len(full_results)} 个独立 Markdown 内容源")

    # 统计
    cat_counter = Counter("/".join(q["category"]) for q in full_results)
    print("\n📊 分类分布:")
    for c, n in cat_counter.most_common():
        print(f"   {c}: {n}")


if __name__ == "__main__":
    main()
