# 文档构建系统

零依赖 Markdown → HTML 构建器。每个子模块（如 `app-dev/`、`interview/`）自成一个目录，
内部 `_src/` 是 Markdown 源，`chapter/*.html` 是独立章节页，`chapters.json` 是目录清单，
`docs.html` 是跳转到第一章的兼容入口，`index.html` 是模块首页。

## 目录结构

```
build.py                   # 构建脚本（零依赖纯 Python）
_templates/
  reader.html              # 阅读器 HTML 模板（含 $placeholder）
app-dev/                   # 应用开发子模块（自包含）
  index.html               # cover 页（手写，landing 风格）
  docs.html                # 第一章重定向入口（构建产物）
  chapter/*.html           # 每章一个独立阅读页（构建产物）
  chapters.json            # 章节目录，供首页加载（构建产物）
  _src/                    # markdown 源
    000-overview.md
    001-roadmap.md
    100-prompt-basics.md
    700-evals.md
    800-streaming-ui.md
    ...
interview/                 # 全栈面试子模块（自包含）
  index.html               # cover 页
  docs.html                # 第一章重定向入口（构建产物）
  chapter/*.html           # 指南章节阅读页（构建产物）
  chapters.json            # 指南目录（构建产物）
  questions/q-*.md         # 人工维护的单题内容源，纳入 git
  quiz-index.json          # 列表、统计与标题别名，纳入 git
  quiz-data.json           # 兼容刷题页的完整数据，纳入 git
  requirements.txt        # 题库脚本依赖，文档构建不需要
  _src/
    00-overview.md
    01-plan.md
    ...
```

## 常用命令

```bash
# 构建全部
python build.py

# 只构建单个模块
python build.py app-dev
python build.py interview
```

文档构建仅使用 Python 标准库。题库的四个 `quiz-*.md` 是导入文件，不是指南章节；构建时提示它们缺少 frontmatter 并跳过属于正常行为。

本地预览需要 HTTP 服务，因为目录和题库数据通过 fetch 加载：

```bash
python -m http.server 3000
# 打开 http://localhost:3000/app-dev/ 或 /interview/
```

## 本地实践验证

`app-dev/examples/core_patterns.py` 提供上下文预算、只读工具执行、租户/版本过滤、MCP 工具身份、CSV 金额统计和 SQLite checkpoint 示例，仅依赖 Python 3.10+ 标准库。

```bash
python -m unittest discover -s app-dev/examples -v
python -m unittest discover -s interview -p 'test_*.py' -v
python -m unittest test_build -v
```

算法与训练答案中的 Python 示例另由 `test_answer_examples.py` 验证；NumPy/PyTorch 部分在相应库已安装时执行，否则明确跳过。模型 SDK 的真实调用需要认证和网络，本地示例测试不能替代模型行为评测。

## 新增一个章节

只需 3 步：

**1. 在 `<module>/_src/` 下创建 md 文件，文件名带数字前缀决定顺序**

```bash
# 例：创建 app-dev/_src/703-eval-example.md
# 编写带 frontmatter 的 Markdown 正文
```

文件按完整文件名字典序排列。应用开发采用三位数字前缀，如 `000`、`100`、`700`；同一组内用 `700`、`701`、`702` 区分。新章节应保持本模块的前缀宽度。

**2. 写 frontmatter + 正文**

```markdown
---
group: 7. 评测与生产治理
id: eval-example
title: Evals · 回归样例
toc: Evals · 回归样例
---

正文从这里开始...
```

frontmatter 字段说明：

| 字段 | 必填 | 用途 |
|------|------|------|
| `group` | 是 | 左侧栏分组标题（首次出现的顺序决定组顺序） |
| `id` | 是 | HTML 锚点 ID（必须唯一） |
| `title` | 是 | 左侧栏 + 主内容区 H2 标题 |
| `toc` | 否 | 右侧 On This Page 显示文本，默认同 title |

**3. 跑一次构建**

```bash
python build.py app-dev
```

完成。`app-dev/chapter/703-eval-example.html` 和目录清单自动生成。章节间链接使用产物文件名，如 `[评测](700-evals.html)`。

旧文档的章节 `#id` 链接会在构建时转换为独立章节文件；未知锚点保留原样。新文档建议直接写目标 HTML 文件名，构建后检查文件和锚点均存在。

已有组的章节会从清单加载；新增整个主题组时，还需更新 `app-dev/index.html` 的 `MODULE_META_BY_GROUP` 和离线回退目录，并在 `_sidebar.md` 加入口。

## 新增一个子模块

要做的步骤：

1. 创建 `<module>/_src/` 和模块首页，首页入口指向 `chapter/` 下的第一篇。
2. 在 `build.py` 顶部 `MODULES` 添加模块文案配置，复用阅读器模板。
3. 编写带 frontmatter 的 Markdown，运行 `python build.py <module>`。
4. 将该模块的 `docs.html`、`chapter/*.html`、`chapters.json` 加入 `.gitignore`，并补充主站导航。

## 维护面试题库

```bash
# 题库脚本需要 PyYAML，先安装一次
python -m pip install -r interview/requirements.txt

# 在 interview/_src/quiz-*.md 录入新题，再增量导入
python interview/parse_questions.py

# 只导入一个源文件，其他已存在题目仍保留
python interview/parse_questions.py quiz-main.md

# 在 questions/q-*.md 补答案，并把 hasAnswer 改为 true
python interview/sync_answers.py

# 验证题号和人工内容保护
python -m unittest discover -s interview -p "test_*.py"
```

`questions/q-*.md` 是已导入题目的权威内容源。已有题的答案、标题、公司、分类和创建日期不会被旧 dump 覆盖；新题使用当前最大编号之后的题号，不重新编号，且按完整标题匹配。首次录入的新题会跨公司聚合。

标题编辑后，导入脚本通过 `quiz-index.json` 的 `variants` 保存原始标题别名；因此索引也要纳入版本控制。不要手工删除旧题再重新编号，这会影响浏览器按题号保存的学习状态。

只改答案用 `sync_answers.py`；改标题、分类、标签或公司后用 `parse_questions.py` 重建索引。答案位于 `## 答案` 之后，可以包含二级标题、公式和代码块；同步会完整保留这些内容。格式错误会中止，先修正 Markdown 再重新运行。

## 支持的 Markdown 语法

```markdown
# H1   ## H2   ### H3

**加粗**   *斜体*   `inline code`

[链接文本](https://example.com)

- 无序列表
- 第二项

1. 有序列表
2. 第二项

> 普通引用块（边框 + 浅色背景）

| 表头 1 | 表头 2 |
|--------|--------|
| 单元格 | 单元格 |

` ` `python                  ← 围栏代码块（Python 关键字自动高亮）
def hello():
    return "world"
` ` `

:::callout 💡              ← 自定义提示框（带图标 + 边框 + 背景）
**支持嵌套 markdown**：可以放 - 列表、`代码`、**加粗** 等
:::
```

## 修改模板 / 颜色

- **样式或布局改动**：编辑 `_templates/reader.html`，重跑 `python build.py`
- **模块颜色/品牌文案**：编辑 `build.py` 顶部的 `MODULES` 字典
- **代码高亮关键字**：编辑 `build.py` 中的 `KEYWORDS` 字典

## 注意事项

- **生成的章节 HTML、重定向页和目录清单不要手改**，下次构建会覆盖。指南修改写到 `_src/` 或 `_templates/`。
- 文档构建产物已加入 `.gitignore`；本地预览前先运行 `python build.py`。单题 Markdown 和题库 JSON 需要提交。
- 文件名前缀决定顺序，建议留出空号（10/20/30...），方便后续插入。
- frontmatter 必须以 `---` 开头和结尾，且后面跟一个空行。
- callout 块的 `:::` 必须各自独占一行，前后不能有空格。
- `:::callout` 后面的图标可以省略，默认显示提示图标；不支持的块标记按普通文本保留。
