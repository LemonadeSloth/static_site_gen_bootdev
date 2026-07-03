from block_markdown import BlockType, block_to_type_no_regex, markdown_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    div_node = ParentNode("div", [])
    for block in blocks:
        block_node = make_html_block_nodes(block)
        div_node.children.append(block_node)
    return div_node


def text_to_children(text: str) -> list[HTMLNode]:
    md_nodes: list[TextNode] = text_to_textnodes(text)
    html_nodes = []
    for node in md_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def delete_block_md_markers(text: str, block_type: BlockType) -> str:
    match block_type:
        case BlockType.QUOTE:
            text_lines = text.splitlines()
            result = ""
            for line in text_lines:
                if not line.startswith(">"):
                    raise ValueError("invalid quote block")
                result += f"{line[1:].strip()} "
            return result.strip()
        case BlockType.CODE:
            if not text.startswith("```") or not text.endswith("```"):
                raise ValueError("invalid code block")
            return text.lstrip("`\n").rstrip("`")
        case BlockType.HEADING:
            return text
        case BlockType.PARAGRAPH:
            return text.replace("\n", " ")
        case BlockType.UNORDERED_LIST:
            text_lines = text.splitlines()
            result = ""
            for line in text_lines:
                result += line[2:] + "\n"
            return result.strip("\n")
        case BlockType.ORDERED_LIST:
            text_lines = text.splitlines()
            result = ""
            for line in text_lines:
                result += line[3:] + "\n"
            return result.strip("\n")
        case _:
            raise ValueError("invalid block type")


def make_html_block_nodes(block: str) -> ParentNode:
    block_type = block_to_type_no_regex(block)
    block = delete_block_md_markers(block, block_type)
    match block_type:
        case BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            if level + 1 >= len(block):
                raise ValueError(f"invalid heading")
            children_nodes = text_to_children(block[level+1:])
            return ParentNode(f"h{level}", children_nodes)
        case BlockType.QUOTE:
            children_nodes = text_to_children(block)
            return ParentNode("blockquote", children_nodes)
        case BlockType.PARAGRAPH:
            children_nodes = text_to_children(block)
            return ParentNode("p", children_nodes)
        case BlockType.ORDERED_LIST:
            children = []
            split_lines = block.splitlines()
            for line in split_lines:
                item_node = ParentNode("li", text_to_children(line))
                children.append(item_node)
            return ParentNode("ol", children)
        case BlockType.UNORDERED_LIST:
            children = []
            split_lines = block.splitlines()
            for line in split_lines:
                item_node = ParentNode("li", text_to_children(line))
                children.append(item_node)
            return ParentNode("ul", children)
        case BlockType.CODE:
            code_node = LeafNode("code", block)
            return ParentNode("pre", [code_node])
        case _:
            raise ValueError("invalid block type")
