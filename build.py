#!/usr/bin/env python3
"""
build.py — 零依赖 Markdown → HTML 构建脚本

用法：
    python build.py            # 构建全部模块
    python build.py app-dev    # 只构建 app-dev
    python build.py interview  # 只构建 interview

输入：<module>/_src/*.md  （带 YAML 风格 frontmatter）
模板：_templates/reader.html
输出：<module>/docs.html

Markdown frontmatter 示例：
    ---
    group: 1. Prompt 工程
    id:    prompt-basics
    title: Prompt 工程 · 基础原则
    toc:   Prompt · 基础原则
    ---

    正文（markdown）...

支持的 Markdown 语法（迷你子集）：
    # H1   ## H2   ### H3
    **bold**   *italic*   `inline code`
    [link text](url)
    - 无序列表
    1. 有序列表
    > 引用块
    | a | b |     表格
    |---|---|
    ```python    代码块（自动 Python 关键字高亮）
    code
    ```
    :::callout 💡    自定义 callout
    内容（markdown）
    :::
"""
import re
import html as htmllib
import sys
import string
from pathlib import Path

ROOT = Path(__file__).parent
TPL = ROOT / "_templates" / "reader.html"

# ─────────────────────────────────────────────────────────────
# 模块配置（颜色 + 文案）
# ─────────────────────────────────────────────────────────────
MODULES = {
    "app-dev": {
        "title": "大模型应用开发 · 文档 · App Dev Guide",
        "brand": "app-dev-guide",
        "cover_url": "index.html",
        "main_url": "../index.html",
        "cover_label": "封面",
        "h1": "大模型应用开发",
        "lead": "从 Prompt 工程到 AI Agent，一站式覆盖大模型应用开发全链路 —— 让你能在 1 周内跑出生产级 MVP。",
        "eyebrow": "Docs · App Dev Guide",
        "back_label": "应用开发封面",
    },
    "interview": {
        "title": "全栈面试 · 文档 · Interview Guide",
        "brand": "interview-guide",
        "cover_url": "index.html",
        "main_url": "../index.html",
        "cover_label": "封面",
        "h1": "全栈面试",
        "lead": "LLM 工程师全栈面试指南 —— 从简历到 Offer 的系统性准备，覆盖算法、八股、系统设计、行为面与谈薪。",
        "eyebrow": "Docs · Interview Guide",
        "back_label": "面试封面",
    },
}

# ─────────────────────────────────────────────────────────────
# 代码高亮（迷你版，支持 Python 关键字）
# ─────────────────────────────────────────────────────────────
KEYWORDS = {
    "python": set("def class if else elif return import from as for while in not and or is async await try except finally raise pass break continue lambda with yield global nonlocal None True False self".split()),
}


def highlight(code, lang="generic"):
    """对已 HTML 转义的代码做朴素高亮。"""
    stash = []

    def keep(s):
        i = len(stash)
        stash.append(s)
        return f"\x00{i}\x00"

    # 1. 注释（# 或 //）
    code = re.sub(r"(#[^\n]*)", lambda m: keep(f'<span class="c">{m.group(1)}</span>'), code)
    code = re.sub(r"(//[^\n]*)", lambda m: keep(f'<span class="c">{m.group(1)}</span>'), code)

    # 2. 字符串（HTML 转义后是 &quot; / &#x27;）
    code = re.sub(r"(&quot;[^&\n]*?&quot;)", lambda m: keep(f'<span class="s">{m.group(1)}</span>'), code)
    code = re.sub(r"(&#x27;[^&\n]*?&#x27;)", lambda m: keep(f'<span class="s">{m.group(1)}</span>'), code)

    # 3. 关键字
    if lang in KEYWORDS:
        kws = KEYWORDS[lang]
        code = re.sub(r"\b([A-Za-z_]\w*)\b",
                      lambda m: f'<span class="k">{m.group(1)}</span>' if m.group(1) in kws else m.group(1),
                      code)

    # 4. 数字
    code = re.sub(r"(?<!\w)(\d+\.?\d*)(?!\w)", r'<span class="n">\1</span>', code)

    for i, s in enumerate(stash):
        code = code.replace(f"\x00{i}\x00", s)
    return code


# ─────────────────────────────────────────────────────────────
# Inline Markdown → HTML
# ─────────────────────────────────────────────────────────────
def render_inline(text):
    """处理 inline 语法：**bold** *italic* `code` [link](url)"""
    stash = []

    def keep(s):
        i = len(stash)
        stash.append(s)
        return f"\x00{i}\x00"

    # 行内代码先抽出，避免内部被其他规则匹配
    text = re.sub(r"`([^`\n]+)`", lambda m: keep(f"<code>{htmllib.escape(m.group(1))}</code>"), text)

    # 转义 HTML
    text = htmllib.escape(text, quote=False)

    # 加粗
    text = re.sub(r"\*\*([^*\n]+)\*\*", r"<strong>\1</strong>", text)
    # 斜体（避开加粗的残余）
    text = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])", r"<em>\1</em>", text)
    # 链接
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)

    for i, s in enumerate(stash):
        text = text.replace(f"\x00{i}\x00", s)
    return text


# ─────────────────────────────────────────────────────────────
# Block-level Markdown → HTML
# ─────────────────────────────────────────────────────────────
BLOCK_START_RE = re.compile(r"^(#{1,6}\s|```|[-*]\s|\d+\.\s|\||>|:::)")


def slugify(text):
    """从标题文本生成 URL slug。"""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.strip().lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text or 'heading'


def render_blocks(md_text, heading_prefix=None):
    """将 markdown 文本解析为 HTML（块级）。"""
    lines = md_text.split("\n")
    out = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # 空行
        if not stripped:
            i += 1
            continue

        # 标题（h2/h3 生成唯一 id，支持 TOC 锚点）
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            text = render_inline(m.group(2))
            if level >= 2 and heading_prefix:
                hid = f"{heading_prefix}--{slugify(text)}"
                out.append(f'<h{level} id="{hid}">{text}</h{level}>')
            else:
                out.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        # 围栏代码块
        m = re.match(r"^```(\w*)\s*$", line)
        if m:
            lang = m.group(1) or "generic"
            code_lines = []
            i += 1
            while i < n and not re.match(r"^```\s*$", lines[i]):
                code_lines.append(lines[i])
                i += 1
            i += 1  # 跳过结束的 ```
            code = "\n".join(code_lines)
            escaped = htmllib.escape(code, quote=True)
            out.append(f"<pre><code>{highlight(escaped, lang)}</code></pre>")
            continue

        # Callout 自定义块
        m = re.match(r"^:::callout\s+(.+?)\s*$", line)
        if m:
            icon = m.group(1)
            inner = []
            i += 1
            while i < n and lines[i].strip() != ":::":
                inner.append(lines[i])
                i += 1
            i += 1  # 跳过结束的 :::
            inner_html = render_blocks("\n".join(inner))
            out.append(f'<div class="callout"><div class="ic">{icon}</div><div>{inner_html}</div></div>')
            continue

        # 引用块
        if line.startswith(">"):
            qlines = []
            while i < n and lines[i].startswith(">"):
                qlines.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            out.append(f"<blockquote>{render_blocks(chr(10).join(qlines))}</blockquote>")
            continue

        # 表格（当前行以 | 开头 且下一行是 |---|---| 分隔符）
        if line.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|\s*$", lines[i + 1]):
            header_cells = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2  # 跳过表头和分隔符
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(cells)
                i += 1
            tbl = ["<table><thead><tr>"]
            for h in header_cells:
                tbl.append(f"<th>{render_inline(h)}</th>")
            tbl.append("</tr></thead><tbody>")
            for row in rows:
                tbl.append("<tr>")
                for cell in row:
                    tbl.append(f"<td>{render_inline(cell)}</td>")
                tbl.append("</tr>")
            tbl.append("</tbody></table>")
            out.append("".join(tbl))
            continue

        # 无序列表
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i]):
                items.append(f"<li>{render_inline(re.sub(r'^[-*]\s+', '', lines[i]))}</li>")
                i += 1
            out.append(f"<ul>{''.join(items)}</ul>")
            continue

        # 有序列表
        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i]):
                items.append(f"<li>{render_inline(re.sub(r'^\d+\.\s+', '', lines[i]))}</li>")
                i += 1
            out.append(f"<ol>{''.join(items)}</ol>")
            continue

        # 段落（直到遇到空行或下一个块级语法）
        para = []
        while i < n and lines[i].strip() and not BLOCK_START_RE.match(lines[i]):
            para.append(lines[i])
            i += 1
        out.append(f"<p>{render_inline(' '.join(para).strip())}</p>")

    return "\n".join(out)


# ─────────────────────────────────────────────────────────────
# Frontmatter 解析
# ─────────────────────────────────────────────────────────────
def parse_frontmatter(text):
    """提取文件开头的 --- ... --- 元数据。返回 (meta_dict, body)。"""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    fm = text[4:end]
    body = text[end + 5:]
    meta = {}
    for line in fm.split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


# ─────────────────────────────────────────────────────────────
# 单模块构建
# ─────────────────────────────────────────────────────────────
def build_module(name, cfg):
    src_dir = ROOT / name / "_src"
    if not src_dir.exists():
        print(f"  ⚠ {src_dir} 不存在，跳过")
        return

    files = sorted(src_dir.glob("*.md"))
    if not files:
        print(f"  ⚠ {src_dir} 无 .md 文件，跳过")
        return

    chapters = []  # list of {group, id, title, toc, html, headings}
    for f in files:
        text = f.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        if "id" not in meta:
            print(f"  ⚠ {f.name} 缺 frontmatter `id`，跳过")
            continue
        html = render_blocks(body, heading_prefix=meta["id"])
        # 提取本章节内的 h2/h3 作为 right-TOC 的子条目
        headings = []
        for m in re.finditer(r'<h([23])\s+id="([^"]+)"[^>]*>(.*?)</h\1>', html):
            level = int(m.group(1))
            hid = m.group(2)
            htext = re.sub(r'<[^>]+>', '', m.group(3))
            headings.append({"level": level, "id": hid, "text": htext})
        chapters.append({
            "file": f.name,
            "group": meta.get("group", "未分组"),
            "id": meta["id"],
            "title": meta.get("title", meta["id"]),
            "toc": meta.get("toc", meta.get("title", meta["id"])),
            "html": html,
            "headings": headings,
        })

    # 按文件名顺序保留；按 group 分组（保持首次出现顺序）
    groups = {}
    group_order = []
    for c in chapters:
        if c["group"] not in groups:
            groups[c["group"]] = []
            group_order.append(c["group"])
        groups[c["group"]].append(c)

    # 生成左侧栏
    sidebar_parts = []
    for g in group_order:
        sidebar_parts.append(f'    <div class="chap-head">{g}</div>')
        for c in groups[g]:
            sidebar_parts.append(f'    <a class="chap-item" href="#{c["id"]}">{c["title"]}</a>')
    sidebar_html = "\n".join(sidebar_parts)

    # 生成正文（按文件顺序，自动包 <section> + <h2> + 底部翻页卡片）
    content_parts = []
    total = len(chapters)
    for i, c in enumerate(chapters):
        content_parts.append(f'    <section id="{c["id"]}">')
        content_parts.append(f'      <h2>{c["title"]}</h2>')
        content_parts.append("      " + c["html"].replace("\n", "\n      "))

        # 底部上一篇 / 下一篇导航
        nav_html = ['      <div class="chap-nav">']
        if i > 0:
            prev = chapters[i - 1]
            nav_html.append(
                f'        <a href="#{prev["id"]}" class="prev">'
                f'<div class="lbl">← 上一篇</div>'
                f'<div class="ttl">{htmllib.escape(prev["title"])}</div></a>'
            )
        else:
            nav_html.append('        <span></span>')
        if i < total - 1:
            nxt = chapters[i + 1]
            nav_html.append(
                f'        <a href="#{nxt["id"]}" class="next">'
                f'<div class="lbl">下一篇 →</div>'
                f'<div class="ttl">{htmllib.escape(nxt["title"])}</div></a>'
            )
        else:
            nav_html.append('        <span></span>')
        nav_html.append('      </div>')
        content_parts.append("\n".join(nav_html))

        content_parts.append('    </section>')
    content_html = "\n".join(content_parts)

    # 生成右侧 TOC（按章节分组，每个项标记 data-section 供 JS 过滤）
    toc_parts = []
    for c in chapters:
        toc_parts.append(f'    <a class="toc-item toc-h1" href="#{c["id"]}" data-section="{c["id"]}">{c["toc"]}</a>')
        for h in c["headings"]:
            indent_class = "toc-h3" if h["level"] == 3 else "toc-h2"
            toc_parts.append(f'    <a class="toc-item {indent_class}" href="#{h["id"]}" data-section="{c["id"]}">{h["text"]}</a>')
    toc_html = "\n".join(toc_parts)

    # 模板替换
    tpl_text = TPL.read_text(encoding="utf-8")
    out_text = string.Template(tpl_text).safe_substitute(
        sidebar=sidebar_html,
        content=content_html,
        toc=toc_html,
        **cfg,
    )

    out_path = ROOT / name / "docs.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out_text, encoding="utf-8")
    print(f"  ✓ {out_path.relative_to(ROOT)}  ({len(chapters)} 章节, {sum(len(v) for v in groups.values())} 项, {len(group_order)} 组)")


# ─────────────────────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────────────────────
def main():
    targets = sys.argv[1:] or list(MODULES.keys())
    print(f"⚙ 构建中...")
    for name in targets:
        if name not in MODULES:
            print(f"  ✗ 未知模块: {name}（可选：{', '.join(MODULES)}）")
            continue
        build_module(name, MODULES[name])
    print("✓ Done.")


if __name__ == "__main__":
    main()
