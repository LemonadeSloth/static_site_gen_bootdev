from inline_markdown import extract_markdown_images, split_nodes_image
from block_markdown import markdown_to_blocks, block_to_type_regex, block_to_type_no_regex
from textnode import TextNode, TextType
from markdown_to_html import delete_block_md_markers, markdown_to_html_node
from block_markdown import BlockType


md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
md2 = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
res = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
html_node = markdown_to_html_node(md2)
print(html_node.to_html())
print(res)
