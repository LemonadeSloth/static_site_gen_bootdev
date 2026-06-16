from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

node = TextNode("This is text with a `code block` word", TextType.TEXT)
new_nodes_one = split_nodes_delimiter([node], "`", TextType.CODE)

node_three = TextNode("This `line` has multiple `code blocks`", TextType.TEXT)
new_nodes = split_nodes_delimiter([node_three], "`", TextType.CODE)
print(new_nodes)
[
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
