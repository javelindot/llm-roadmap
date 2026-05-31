#!/usr/bin/env python3
"""
面试题解析脚本
用法:
  python parse_questions.py              # 解析 _src/ 下所有 .md 文件
  python parse_questions.py demo.md      # 只解析指定文件
  python parse_questions.py demo.md demo2.md  # 解析多个文件

扫描面试题 Markdown，提取公司、题目、答案，
自动分类、打标签，输出 quiz-data.json。
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter

SRC_DIR = Path(__file__).parent / "_src"
OUTPUT = Path(__file__).parent / "quiz-data.json"


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
        ("编程基础", ["python", "list", "dict", "set", "tuple", "线程", "进程", "协程", "深浅拷贝", "装饰器", "算法", "leetcode", "排序", "数组"]),
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
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    questions = []
    current_company = None
    current_category = None
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

        # 检测公司名（排除编号列表项、说明性正文）
        company_match = None
        is_list_item = bool(re.match(r'^\s*\d+[\.、]\s*\S', line))
        if line.startswith("##") and not line.startswith("###"):
            m = re.search(r'^##\s*(.+)', line)
            if m:
                company_match = clean_html(m.group(1))
        elif not is_list_item and "**" in line and any(k in line for k in ["公司", "科技", "集团", "互联", "动力", "医疗", "车联网", "财经", "数字人", "机器人"]):
            c = clean_html(line.replace("**", ""))
            # 必须以公司类关键字结尾或临近结尾，避免句子被误判
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

            # 保留条件：有答案 或 来源为图片/截图/未知（纯问题录入）
            is_unknown_source = current_company and any(k in current_company for k in ["来源未知", "图片", "截图"])
            if answer or is_unknown_source:
                questions.append({
                    "company": current_company or "未知",
                    "category": current_category or "综合",
                    "question": q_text,
                    "answer": answer,
                })
            i = j
            continue

        i += 1

    return questions


def is_question_dump(path: Path) -> bool:
    """题库 dump 以 `## 公司名` 开头；指南类文档以 `---` frontmatter 开头。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            first = f.readline().strip()
        return first.startswith("##")
    except OSError:
        return False


def main():
    # 命令行参数指定文件；否则只扫 _src/ 下属于题库 dump 的 .md
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
    merged = {}  # key -> dict
    order = []   # 保留首次出现顺序
    for q in all_raw:
        key = q["question"][:60]
        company = q["company"].replace("（", "(").replace("）", ")")
        if key not in merged:
            merged[key] = {
                "question": q["question"],
                "answer": q["answer"],
                "companies": [],
            }
            order.append(key)
        rec = merged[key]
        if company and company not in rec["companies"]:
            rec["companies"].append(company)
        # 取最长答案作为参考答案
        if len(q["answer"].strip()) > len(rec["answer"].strip()):
            rec["answer"] = q["answer"]

    # 分类、打标签、计算频次、生成 ID
    results = []
    for idx, key in enumerate(order, 1):
        rec = merged[key]
        cat = classify(rec["question"], rec["answer"])
        tags = extract_tags(rec["question"], rec["answer"])
        has_answer = len(rec["answer"].strip()) > 10
        freq = len(rec["companies"])
        # 热度：freq>=4 双火 / freq>=2 单火 / 否则无
        if freq >= 4:
            hot = 2
        elif freq >= 2:
            hot = 1
        else:
            hot = 0
        results.append({
            "id": f"q-{idx}",
            "company": rec["companies"][0] if rec["companies"] else "未知",
            "companies": rec["companies"] or ["未知"],
            "frequency": freq if freq > 0 else 1,
            "hot": hot,
            "category": cat,
            "title": rec["question"],
            "answer": rec["answer"] if has_answer else "",
            "hasAnswer": has_answer,
            "tags": tags,
        })

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 共解析 {len(results)} 道题目，输出到 {OUTPUT}")

    # 统计
    cat_counter = Counter(q["category"] for q in results)
    co_counter = Counter(q["company"] for q in results)
    print("\n📊 分类分布:")
    for c, n in cat_counter.most_common():
        print(f"   {c}: {n}")
    print("\n🏢 公司分布:")
    for c, n in co_counter.most_common():
        print(f"   {c}: {n}")


if __name__ == "__main__":
    main()
