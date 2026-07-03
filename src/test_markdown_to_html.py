import unittest

from markdown_to_html import markdown_to_html_node


class TestMDtoHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
This _is_ a test **paragraph**

> This _is_
> a
> **test** quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This <i>is</i> a test <b>paragraph</b></p><quoteblock>This <i>is</i>\na\n<b>test</b> quote</quoteblock></div>",
        )

    def test_ordered_list(self):
        md = """
This _is_ a test **paragraph**

1. This _is_
2. a
3. **test** list
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This <i>is</i> a test <b>paragraph</b></p><ol><li>This <i>is</i></li><li>a</li><li><b>test</b> list</li></ol></div>",
        )

    def test_unordered_list(self):
        md = """
This _is_ a test **paragraph**

- This _is_
- a
- **test** list
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This <i>is</i> a test <b>paragraph</b></p><ul><li>This <i>is</i></li><li>a</li><li><b>test</b> list</li></ul></div>",
        )
