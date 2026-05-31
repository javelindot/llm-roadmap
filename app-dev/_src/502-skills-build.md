---
group: 5. Skills
id: skills-build
title: Skills · 编写第一个 Skill
toc: Skills · 编写
---

实战章节。**从零写一个 Skill**，接入 Claude Agent SDK 跑起来。

## Skill 的标准目录结构

```
my_skill/
├── SKILL.md             ← 必需，Skill 的主定义
├── tools/               ← 可选，该 Skill 用到的工具
│   ├── tool_a.py
│   └── tool_b.py
├── templates/           ← 可选，输出模板
│   └── template.md
├── examples/            ← 可选，Few-shot 示例
│   └── example.md
└── resources/           ← 可选，静态资源（参考资料、配置等）
    └── style_guide.md
```

只有 `SKILL.md` 是必需的。其他按需添加。

## SKILL.md 的标准结构

```markdown
---
name: skill_name              # 唯一标识符（snake_case）
display_name: Skill Name       # 展示用
version: 1.0.0
description: 一句话描述这个 Skill 的能力
author: Your Name
tags: [data, analysis]
---

# Skill 名称

## When to use

什么场景下应该使用这个 Skill。
（这部分是 Claude 判断"要不要加载我"的关键依据，必须清晰）

## Capabilities

这个 Skill 能做什么：
- 能力 1
- 能力 2

## Tools available

列出该 Skill 使用的工具：
- `tool_a`: 描述
- `tool_b`: 描述

## Process

完成任务的标准步骤：
1. 步骤 1
2. 步骤 2

## Output format

输出的格式规范。

## Examples

简要的使用例子。
```

## 实战 1：编写「CSV 数据分析」Skill

需求：让 Claude 能分析任意 CSV 文件，输出关键统计 + 洞察。

### 目录结构

```
skills/csv_analyzer/
├── SKILL.md
├── tools/
│   ├── load_csv.py
│   ├── compute_stats.py
│   └── plot_chart.py
├── templates/
│   └── analysis_report.md
└── examples/
    └── sales_analysis.md
```

### SKILL.md

```markdown
---
name: csv_analyzer
display_name: CSV 数据分析师
version: 1.0.0
description: 加载 CSV 文件，计算统计指标，生成洞察报告
tags: [data, analysis, csv]
---

# CSV Data Analyzer

## When to use

当用户提供 CSV 文件或路径，并询问以下需求时使用：
- 数据基本统计（均值、中位数、分布）
- 相关性分析
- 趋势识别
- 异常值检测
- 数据可视化
- 生成分析报告

## Capabilities

- 加载和预览 CSV
- 数值列统计（mean / median / std / quartiles）
- 类别列分布
- 列间相关性矩阵
- 时间序列趋势
- 异常值检测（基于 z-score 或 IQR）
- 生成可视化图表（柱状/折线/散点/热力图）
- 输出结构化分析报告

## Tools available

- `load_csv(path, encoding)`: 加载 CSV 文件，返回 dataframe summary
- `compute_stats(df_id, columns)`: 计算指定列的统计指标
- `plot_chart(df_id, type, x, y, title)`: 生成图表，返回图片 URL
- `detect_outliers(df_id, column, method)`: 检测异常值

## Process

按以下步骤分析 CSV：

1. **加载**：用 `load_csv` 加载文件，获取列名、数据类型、行数
2. **数据画像**：
   - 数值列：用 `compute_stats` 获取统计指标
   - 类别列：统计分布
3. **核心分析**：根据用户具体问题，选择执行：
   - 趋势分析：plot_chart(type="line")
   - 分布分析：plot_chart(type="histogram")
   - 关系分析：plot_chart(type="scatter")
   - 异常值：detect_outliers
4. **生成洞察**：基于上述结果，总结 3-5 条关键发现
5. **输出报告**：按 `templates/analysis_report.md` 格式输出

## Output format

最终输出按 `templates/analysis_report.md` 的结构：

```
## 数据概览
- 行数 / 列数
- 数据类型分布

## 关键发现
1. ...
2. ...
3. ...

## 详细分析
（按用户问题展开）

## 可视化
（插入图表 URL）

## 建议
（基于分析的行动建议，2-3 条）
```

## Tips

- 如果数据 > 100K 行，先采样分析再说明
- 遇到缺失值要先汇报情况再继续
- 输出中所有数字保留 2 位小数
- 图表标题用中文
```

### tools/load_csv.py

```python
"""Skill 内部工具：加载 CSV"""
import pandas as pd
import uuid
from pathlib import Path

# 简单的内存 DataFrame 存储（生产可换 Redis）
_df_store: dict[str, pd.DataFrame] = {}

def load_csv(path: str, encoding: str = "utf-8") -> dict:
    """加载 CSV 文件
    
    Args:
        path: CSV 文件路径
        encoding: 编码（默认 utf-8）
    
    Returns:
        {
            "df_id": str,        # 后续工具用这个 ID 引用
            "rows": int,
            "columns": list[str],
            "dtypes": dict,
            "preview": str       # 前 5 行的 Markdown 表格
        }
    """
    df = pd.read_csv(path, encoding=encoding)
    df_id = str(uuid.uuid4())[:8]
    _df_store[df_id] = df
    
    return {
        "df_id": df_id,
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": {col: str(dt) for col, dt in df.dtypes.items()},
        "preview": df.head().to_markdown(index=False)
    }

def get_df(df_id: str) -> pd.DataFrame:
    """内部用，其他工具用 df_id 获取 DataFrame"""
    if df_id not in _df_store:
        raise ValueError(f"DataFrame {df_id} not found")
    return _df_store[df_id]
```

### tools/compute_stats.py

```python
from .load_csv import get_df

def compute_stats(df_id: str, columns: list[str] | None = None) -> dict:
    """计算指定列的统计指标"""
    df = get_df(df_id)
    cols = columns or df.select_dtypes(include="number").columns.tolist()
    
    stats = {}
    for col in cols:
        if col not in df.columns:
            continue
        s = df[col].dropna()
        if pd.api.types.is_numeric_dtype(s):
            stats[col] = {
                "count": int(s.count()),
                "mean": round(s.mean(), 2),
                "median": round(s.median(), 2),
                "std": round(s.std(), 2),
                "min": round(s.min(), 2),
                "max": round(s.max(), 2),
                "q25": round(s.quantile(0.25), 2),
                "q75": round(s.quantile(0.75), 2),
                "null_count": int(df[col].isna().sum())
            }
        else:
            stats[col] = {
                "type": "categorical",
                "unique_count": int(s.nunique()),
                "top_values": s.value_counts().head(5).to_dict(),
                "null_count": int(df[col].isna().sum())
            }
    return stats
```

### tools/plot_chart.py

```python
from .load_csv import get_df
import matplotlib.pyplot as plt
import uuid
import os

CHART_DIR = "./charts"
os.makedirs(CHART_DIR, exist_ok=True)

def plot_chart(df_id: str, type: str, x: str | None = None,
               y: str | None = None, title: str = "") -> dict:
    """生成图表
    
    Args:
        type: line / bar / scatter / histogram / heatmap
        x: x 轴列名
        y: y 轴列名
        title: 标题
    """
    df = get_df(df_id)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if type == "line":
        df.plot(x=x, y=y, kind="line", ax=ax, title=title)
    elif type == "bar":
        df[x].value_counts().head(10).plot(kind="bar", ax=ax, title=title)
    elif type == "scatter":
        df.plot(x=x, y=y, kind="scatter", ax=ax, title=title)
    elif type == "histogram":
        df[x].hist(ax=ax, bins=30)
        ax.set_title(title)
    elif type == "heatmap":
        corr = df.corr(numeric_only=True)
        import seaborn as sns
        sns.heatmap(corr, annot=True, ax=ax)
        ax.set_title(title or "相关性热力图")
    
    chart_path = f"{CHART_DIR}/{uuid.uuid4()}.png"
    fig.savefig(chart_path, dpi=100, bbox_inches="tight")
    plt.close(fig)
    
    return {"chart_url": chart_path, "type": type, "title": title}
```

### templates/analysis_report.md

```markdown
# {{ title }}

## 数据概览
- **行数**: {{ rows }}
- **列数**: {{ cols }}
- **数据时间范围**: {{ date_range or "N/A" }}
- **缺失值情况**: {{ missing_summary }}

## 关键发现
{% for finding in findings %}
{{ loop.index }}. {{ finding }}
{% endfor %}

## 详细分析
{{ detailed_analysis }}

## 可视化
{% for chart in charts %}
![{{ chart.title }}]({{ chart.url }})
{% endfor %}

## 行动建议
{% for suggestion in suggestions %}
- **{{ suggestion.priority }}**: {{ suggestion.text }}
{% endfor %}
```

### examples/sales_analysis.md

```markdown
# 示例：分析 sales_q3.csv

用户提问: "分析这份销售数据，找出关键趋势"

## 我的执行过程

1. 调 load_csv("sales_q3.csv") → 1500 行 × 8 列
2. 调 compute_stats() → 发现 revenue 列均值 ¥5320，但有几个超过 ¥50000 的极端值
3. 调 detect_outliers("revenue", "iqr") → 标识出 23 条异常订单
4. 调 plot_chart("line", x="date", y="revenue") → 生成趋势图，发现 8 月底有明显下滑
5. 调 plot_chart("bar", x="region") → 华东占 45%

## 最终输出

[按 templates/analysis_report.md 格式输出]
```

## 用 Claude Agent SDK 加载 Skill

```python
from claude_agent_sdk import Agent, Skill

# 从目录加载 Skill
skill = Skill.from_directory("./skills/csv_analyzer")

# 创建 Agent
agent = Agent(
    model="claude-sonnet-4-5",
    skills=[skill]
)

# 使用
result = agent.run("分析 /data/sales_q3.csv，找出关键趋势")
print(result)
```

Claude 会：
1. 看到用户问题 → 扫描可用 Skills
2. 看到 `csv_analyzer` 的 "When to use" 匹配 → 加载该 Skill
3. 按 Skill 中的 Process 步骤执行
4. 输出符合 templates 的报告

## 实战 2：编写「Code Review」Skill

需求：让 Claude 能对 PR 做高质量 review。

### SKILL.md

```markdown
---
name: code_reviewer
version: 1.0.0
description: 对代码 PR 进行全方位 review
tags: [code, review, quality]
---

# Code Reviewer

## When to use

当用户提供以下内容时使用：
- GitHub PR URL
- 代码 diff
- 完整代码文件
- 要求 "review 这段代码"、"check 这个 PR" 等

## Capabilities

review 维度：
- 安全性（SQL 注入、XSS、密钥泄露等）
- 性能（复杂度、内存、I/O）
- 可读性（命名、注释、结构）
- 可维护性（DRY、SOLID）
- 测试覆盖
- 文档完整性

## Tools available

- `fetch_pr(url)`: 从 GitHub URL 获取 PR diff
- `parse_diff(diff)`: 解析 diff 为结构化数据
- `lint_code(code, language)`: 跑静态检查工具

## Process

1. **理解 context**：
   - 是 PR 还是单文件？语言是什么？
   - 用户是否指定关注点（如"只看安全性"）？
   
2. **加载代码**：
   - PR → fetch_pr
   - 单文件 → 直接读
   
3. **多维度分析**（按 Capabilities 列表）：
   - 对每行/每函数标注问题
   - 严重程度: 🔴 Critical / 🟠 Major / 🟡 Minor / 🟢 Suggestion
   
4. **整理输出**：用 templates/review.md 格式

## Output format

```
## Summary
（1-2 句话概括整体质量）

## Critical Issues 🔴
（必须修复的，如安全漏洞）
- file:line - 问题描述
  建议: ...

## Major Issues 🟠
（应该修复的，如性能问题）

## Minor Issues 🟡
（最好修复的，如代码风格）

## Suggestions 🟢
（值得考虑的改进）

## What's Good ✅
（值得保留的优点，让 PR 作者不沮丧）

## Overall Recommendation
[ ] Approve
[ ] Request Changes
[ ] Comment
```

## Style Guide

- 反馈要**具体可执行**，不要"代码质量需要改进"这种空话
- 严重问题给出**修复代码示例**
- 不要批评编码习惯，要批评具体问题
- 优点要单独列，平衡批评
```

## Skill 编写的 7 个最佳实践

### 1. "When to use" 是关键

模型靠这段判断要不要加载 Skill。**写得越具体、越无歧义，加载准确率越高**。

```markdown
# ❌ 模糊
当用户需要数据相关操作时

# ✅ 具体
当用户提供 CSV/Excel 文件并询问统计、分析、可视化时
```

### 2. Process 步骤化

把"如何做"拆成清晰步骤。模型按步骤执行更稳定。

### 3. 给优秀示例

`examples/` 目录放 Few-shot 案例，模型会模仿。

### 4. 工具描述详尽

工具的 description / docstring 决定模型用不用对。

### 5. 输出模板

用 templates/ 保证产出一致性。

### 6. 限定边界

明确说"不做什么"：

```markdown
## Limitations

- 不支持二进制文件（图片、视频）
- 不会自动修改用户的文件（只输出建议）
- 数据 > 1M 行需要先采样
```

### 7. 版本化

把 Skill 当代码管理：进 Git、有版本号、写 CHANGELOG。

## 调试 Skill

### 看 Claude 怎么"看"你的 Skill

```python
from claude_agent_sdk import Agent
agent = Agent(model="claude-sonnet-4-5", skills=[skill])

# 开启 verbose 模式
agent.run("分析数据", verbose=True)
# 会打印:
# - 哪些 Skills 被考虑加载
# - 最终加载了哪些
# - 每步调用了哪些 tool
# - 每步的中间结果
```

### 单元测试 Skill

```python
def test_csv_analyzer():
    agent = Agent(skills=[Skill.from_directory("./skills/csv_analyzer")])
    
    result = agent.run("分析 /test_data/sample.csv")
    
    # 检查关键步骤
    assert "load_csv" in agent.trace.tool_calls
    assert "compute_stats" in agent.trace.tool_calls
    
    # 检查输出格式
    assert "## 数据概览" in result
    assert "## 关键发现" in result
```

## 总结：Skill 编写检查清单

```
☐ SKILL.md 的 "When to use" 清晰具体
☐ 列出所有 capabilities（让模型知道能做什么）
☐ Tools 描述详尽（含参数说明）
☐ Process 步骤化（按顺序）
☐ 有输出模板（保证一致性）
☐ 至少 1-2 个 examples
☐ 写明 limitations 和 tips
☐ 工具实现有错误处理
☐ 工具失败信息可读（模型能恢复）
☐ 版本号 + Git 管理
```

下一节：[Skills 部署与最佳实践](#skills-deploy) —— 把 Skill 跑在生产环境。
