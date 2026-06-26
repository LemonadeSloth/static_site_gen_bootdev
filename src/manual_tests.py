from inline_markdown import extract_markdown_images, split_nodes_image
from block_markdown import markdown_to_blocks, block_to_type_regex, block_to_type_no_regex
from textnode import TextNode, TextType

md = """
# HEadin

> itme2
> tem3
>item3

- Hello
- To
- You

- Hello
To
- You


```
code1
```

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line   

- This is a list
- with items   
"""
md2 = """
```
code
```
"""

blocks = markdown_to_blocks(md)
print(blocks)
print("---")
print(blocks[4])
print("---")
print(blocks[4][:4])
print("---")
print(blocks[4][-4:])
print("---")
print(block_to_type_no_regex(blocks[4]))

