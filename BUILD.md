# 文档构建系统

零依赖 Markdown → HTML 构建器。每个子模块（如 `app-dev/`、`interview/`）自成一个目录，
内部 `_src/` 是 markdown 源、`docs.html` 是构建产物、`index.html` 是 cover 页。

## 目录结构

```
build.py                   # 构建脚本（零依赖纯 Python）
_templates/
  reader.html              # 阅读器 HTML 模板（含 $placeholder）
app-dev/                   # 应用开发子模块（自包含）
  index.html               # cover 页（手写，landing 风格）
  docs.html                # 阅读器（构建产物，不入 git）
  _src/                    # markdown 源
    00-overview.md
    01-roadmap.md
    10-prompt-basics.md
    ...
interview/                 # 全栈面试子模块（自包含）
  index.html               # cover 页
  docs.html                # 构建产物
  _src/
    00-overview.md
    01-plan.md
    ...
```

## 常用命令

```bash
# 构建全部
python3 build.py

# 只构建单个模块
python3 build.py app-dev
python3 build.py interview
```

## 新增一个章节

只需 3 步：

**1. 在 `<module>/_src/` 下创建 md 文件，文件名带数字前缀决定顺序**

```bash
# 例：在「应用开发」第 6 大类下加一节
touch app-dev/_src/60-eval-overview.md
```

文件名前两位数字决定章节出现顺序（如 `00-`、`10-`、`60-`），同一组内用尾号区分（如 `60-`、`61-`）。

**2. 写 frontmatter + 正文**

```markdown
---
group: 6. 评测体系
id: eval-overview
title: 评测 · 为什么需要
toc: 评测 · 为什么需要
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
python3 build.py app-dev
```

完成。`app-dev/docs.html` 自动重新生成。

## 新增一个子模块

要做的步骤：

```bash
# 1. 复制现有子模块作模板
cp -r app-dev/ my-new-module/
rm -rf my-new-module/_src/*.md   # 清空源文件

# 2. 编辑 my-new-module/index.html（cover 页）
#    - 改文案、改 CTA 链接到 docs.html

# 3. 在 build.py 顶部 MODULES dict 添加新模块配置
#    （复制 app-dev 那段，改名 + 改颜色）

# 4. 写 _src/ 下的 markdown

# 5. 跑 python3 build.py my-new-module
```

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

- **样式或布局改动**：编辑 `_templates/reader.html`，重跑 `python3 build.py`
- **模块颜色/品牌文案**：编辑 `build.py` 顶部的 `MODULES` 字典
- **代码高亮关键字**：编辑 `build.py` 中的 `KEYWORDS` 字典

## 注意事项

- **生成的 `*/docs.html` 不要手改**，下次构建会覆盖。所有修改写到 `_src/` 或 `_templates/`。
- 这些 `docs.html` 已加入 `.gitignore`；本地预览前请先 `python3 build.py`。
- 文件名前缀决定顺序，建议留出空号（10/20/30...），方便后续插入。
- frontmatter 必须以 `---` 开头和结尾，且后面跟一个空行。
- callout 块的 `:::` 必须各自独占一行，前后不能有空格。
