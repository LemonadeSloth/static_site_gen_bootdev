import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    split_nodes_list: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes_list.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("no delimiters or no closing delimiter in text")
            for i in range(len(split_text)):
                if not split_text[i]:
                    continue
                if i % 2 == 0:
                    new_node = TextNode(split_text[i], TextType.TEXT)
                    split_nodes_list.append(new_node)
                else:
                    new_node = TextNode(split_text[i], text_type)
                    split_nodes_list.append(new_node)
    return split_nodes_list


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes_list: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes_list.append(node)
            continue
        images_md: list[tuple[str, str]] = extract_markdown_images(node.text)
        if not images_md:
            split_nodes_list.append(node)
            continue
        split_node_text = []
        node_text = node.text
        for image in images_md:
            split_node_text = node_text.split(f"![{image[0]}]({image[1]})", 1)
            if split_node_text[0]:
                split_nodes_list.append(TextNode(split_node_text[0], TextType.TEXT))
            split_nodes_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node_text = split_node_text[1]
        if node_text:
            split_nodes_list.append(TextNode(node_text, TextType.TEXT))
    return split_nodes_list


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes_list: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes_list.append(node)
            continue
        links_md: list[tuple[str, str]] = extract_markdown_links(node.text)
        if not links_md:
            split_nodes_list.append(node)
            continue
        split_node_text = []
        node_text = node.text
        for link in links_md:
            split_node_text = node_text.split(f"[{link[0]}]({link[1]})", 1)
            if split_node_text[0]:
                split_nodes_list.append(TextNode(split_node_text[0], TextType.TEXT))
            split_nodes_list.append(TextNode(link[0], TextType.LINK, link[1]))
            node_text = split_node_text[1]
        if node_text:
            split_nodes_list.append(TextNode(node_text, TextType.TEXT))
    return split_nodes_list


def text_to_textnodes(text: str) -> list[TextNode]:
    split_nodes: list[TextNode]
    base_node = TextNode(text, TextType.TEXT)

    split_nodes = split_nodes_delimiter([base_node], "**", TextType.BOLD)
    split_nodes = split_nodes_delimiter(split_nodes, "_", TextType.ITALIC)
    split_nodes = split_nodes_delimiter(split_nodes, "`", TextType.CODE)
    split_nodes = split_nodes_link(split_nodes)
    split_nodes = split_nodes_image(split_nodes)
    return split_nodes
