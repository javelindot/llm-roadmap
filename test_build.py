"""构建器块语法回归测试：python -m unittest test_build。"""
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import io
from html.parser import HTMLParser

import build
from build import render_blocks, render_inline, resolve_chapter_links


class RenderBlocksTests(unittest.TestCase):
    """验证提示块和未识别标记不会使 Markdown 解析停滞。"""

    def test_callout_without_icon(self):
        """省略图标时使用默认提示，并继续渲染后面的正文。"""
        output = render_blocks(":::callout\n注意权限。\n:::\n\n后续正文。")
        self.assertIn('class="callout"', output)
        self.assertIn("注意权限", output)
        self.assertIn("后续正文", output)

    def test_unsupported_block_markers_fall_back_to_text(self):
        """孤立表格行和提示块标记应保留为文本，不产生无限循环。"""
        output = render_blocks("| 单独一行\n\n:::\n\n正常正文。")
        self.assertIn("单独一行", output)
        self.assertIn(":::", output)
        self.assertIn("正常正文", output)

    def test_chapter_navigation_resolves_to_parent_pages(self):
        """独立章节里的封面和主站链接要按章节子目录计算相对位置。"""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "app-dev" / "_src"
            source.mkdir(parents=True)
            (source / "000-test.md").write_text(
                "---\ngroup: 测试\nid: test\ntitle: 测试章节\n---\n\n正文。\n", encoding="utf-8")
            with patch.object(build, "ROOT", root), redirect_stdout(io.StringIO()):
                build.build_module("app-dev", build.MODULES["app-dev"])
            output = (root / "app-dev/chapter/000-test.html").read_text(encoding="utf-8")
            self.assertIn('class="brand" href="../index.html"', output)
            self.assertIn('href="../../index.html">首页', output)

    def test_legacy_links_resolve_without_touching_code_or_external_urls(self):
        """旧章节锚点应跳到独立页面，外链、未知锚点和代码不改。"""
        source = ('<a href="#second" title="A &amp; B">下一章</a>\n'
                  '<a href="https://example.com/#second">外链</a>'
                  '<a href="#unknown">本地未知</a>'
                  '<pre>&lt;a href=&quot;#second&quot;&gt;</pre>')
        result = resolve_chapter_links(source, {"second": "001-second.html#second"})
        self.assertIn('href="001-second.html#second" title="A &amp; B"', result)
        self.assertIn('href="https://example.com/#second"', result)
        self.assertIn('href="#unknown"', result)
        self.assertIn('<pre>&lt;a href=&quot;#second&quot;&gt;</pre>', result)

    def test_cross_chapter_link_is_rewritten_during_build(self):
        """完整构建应将正文中的跨章节锚点改为目标文件。"""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "app-dev" / "_src"
            source.mkdir(parents=True)
            (source / "000-first.md").write_text(
                "---\ngroup: 测试\nid: first\ntitle: 第一章\n---\n\n[第二章](#second)\n",
                encoding="utf-8")
            (source / "001-second.md").write_text(
                "---\ngroup: 测试\nid: second\ntitle: 第二章\n---\n\n正文。\n",
                encoding="utf-8")
            with patch.object(build, "ROOT", root), redirect_stdout(io.StringIO()):
                build.build_module("app-dev", build.MODULES["app-dev"])
            output = (root / "app-dev/chapter/000-first.html").read_text(encoding="utf-8")
            self.assertIn('href="001-second.html#second"', output)

    def test_generated_python_example_retains_original_indentation(self):
        """章节包装与语法高亮不得改变可复制 Python 代码的缩进。"""
        code = 'def hello():\n    """返回演示值。"""\n    return "ok"'

        class CodeParser(HTMLParser):
            """提取高亮标签中的文本，比较实际复制得到的内容。"""

            def __init__(self):
                """初始化代码范围和文本缓存。"""
                super().__init__()
                self.inside = False
                self.text = []

            def handle_starttag(self, tag, attrs):
                """标记进入代码标签。"""
                if tag == "code":
                    self.inside = True

            def handle_endtag(self, tag):
                """标记离开代码标签。"""
                if tag == "code":
                    self.inside = False

            def handle_data(self, data):
                """收集代码范围内的原始文本。"""
                if self.inside:
                    self.text.append(data)

        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "app-dev" / "_src"
            source.mkdir(parents=True)
            (source / "000-code.md").write_text(
                f"---\ngroup: 测试\nid: code\ntitle: 代码\n---\n\n```python\n{code}\n```\n",
                encoding="utf-8")
            with patch.object(build, "ROOT", root), redirect_stdout(io.StringIO()):
                build.build_module("app-dev", build.MODULES["app-dev"])
            parser = CodeParser()
            parser.feed((root / "app-dev/chapter/000-code.html").read_text(encoding="utf-8"))
            self.assertEqual("".join(parser.text), code)

    def test_local_links_stay_in_current_tab_and_escape_url_attributes(self):
        """站内阅读连续导航，外链独立打开，URL 引号不破坏标签。"""
        self.assertEqual(render_inline("[下一章](chapter.html)"), '<a href="chapter.html">下一章</a>')
        external = render_inline('[资源](https://example.com/?q="text"&a=1)')
        self.assertIn('href="https://example.com/?q=&quot;text&quot;&amp;a=1"', external)
        self.assertIn('target="_blank" rel="noopener"', external)


if __name__ == "__main__":
    unittest.main()
