from block_markdown import markdown_to_blocks
from htmlnode import HTMLNode


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:

