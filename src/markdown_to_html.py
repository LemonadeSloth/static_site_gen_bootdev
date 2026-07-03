from block_markdown import markdown_to_blocks, block_to_type_no_regex, BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    div_node = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_type_no_regex(block)
        block_no_md = delete_block_md_markers(block, block_type)
        match block_type:
            case BlockType.HEADING:
                if block.startswith("# "):
                    block_node = ParentNode("h1", [])
                    children_nodes = text_to_children(block[2:])
                    for child in children_nodes:
                        block_node.children.append(child)
                elif block.startswith("## "):
                    block_node = ParentNode("h2", [])
                    children_nodes = text_to_children(block[3:])
                    for child in children_nodes:
                        block_node.children.append(child)
                elif block.startswith("### "):
                    block_node = ParentNode("h3", [])
                    children_nodes = text_to_children(block[4:])
                    for child in children_nodes:
                        block_node.children.append(child)
                elif block.startswith("#### "):
                    block_node = ParentNode("h4", [])
                    children_nodes = text_to_children(block[5:])
                    for child in children_nodes:
                        block_node.children.append(child)
                elif block.startswith("##### "):
                    block_node = ParentNode("h5", [])
                    children_nodes = text_to_children(block[6:])
                    for child in children_nodes:
                        block_node.children.append(child)
                else:
                    block_node = ParentNode("h6", [])
                    children_nodes = text_to_children(block[7:])
                    for child in children_nodes:
                        block_node.children.append(child)
            case BlockType.QUOTE:
                block_node = ParentNode("quoteblock", [])
                children_nodes = text_to_children(block_no_md)
                for child in children_nodes:
                    block_node.children.append(child)
            case BlockType.PARAGRAPH:
                block_node = ParentNode("p", [])
                children_nodes = text_to_children(block_no_md)
                for child in children_nodes:
                    block_node.children.append(child)
            case BlockType.ORDERED_LIST:
                block_node = ParentNode("ol", [])
                split_lines = block_no_md.splitlines()
                for line in split_lines:
                    children_nodes = text_to_children(line)
                    item_node = ParentNode("li", [])
                    for child in children_nodes:
                        item_node.children.append(child)
                    block_node.children.append(item_node)
            case BlockType.UNORDERED_LIST:
                block_node = ParentNode("ul", [])
                split_lines = block_no_md.splitlines()
                for line in split_lines:
                    children_nodes = text_to_children(line)
                    item_node = ParentNode("li", [])
                    for child in children_nodes:
                        item_node.children.append(child)
                    block_node.children.append(item_node)
            case BlockType.CODE:
                code_node = LeafNode("code", block_no_md)
                block_node = ParentNode("pre", [code_node])
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
                result += line[1:].strip() + "\n"
            return result.strip("\n")
        case BlockType.CODE:
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


