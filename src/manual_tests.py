from inline_markdown import extract_markdown_images, split_nodes_image
from textnode import TextNode, TextType

node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    
new_nodes = split_nodes_image([node])
print(new_nodes)
(
    [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.TEXT),
        TextNode(
            "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
        ),
    ],
    new_nodes,
)
