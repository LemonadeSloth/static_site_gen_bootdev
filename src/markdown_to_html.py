from block_markdown import BlockType, block_to_type_no_regex, markdown_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    div_node = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_type_no_regex(block)
        block_node = make_html_block_nodes(block, block_type)
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
                result += f"{line[1:].strip()} "
            return result.strip(" ")
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


def make_html_block_nodes(block: str, block_type: BlockType) -> HTMLNode:
    block = delete_block_md_markers(block, block_type)
    match block_type:
        case BlockType.HEADING:
            if block.startswith("# "):
                block_node = ParentNode("h1", [])
                children_nodes = text_to_children(block[2:])
                for child in children_nodes:
                    block_node.children.append(child)
                return block_node
            elif block.startswith("## "):
                block_node = ParentNode("h2", [])
                children_nodes = text_to_children(block[3:])
                for child in children_nodes:
                    block_node.children.append(child)
                return block_node
            elif block.startswith("### "):
                block_node = ParentNode("h3", [])
                children_nodes = text_to_children(block[4:])
                for child in children_nodes:
                    block_node.children.append(child)
                return block_node
            elif block.startswith("#### "):
                block_node = ParentNode("h4", [])
                children_nodes = text_to_children(block[5:])
                for child in children_nodes:
                    block_node.children.append(child)
                return block_node
            elif block.startswith("##### "):
                block_node = ParentNode("h5", [])
                children_nodes = text_to_children(block[6:])
                for child in children_nodes:
                    block_node.children.append(child)
                return block_node
            else:
                block_node = ParentNode("h6", [])
                children_nodes = text_to_children(block[7:])
                for child in children_nodes:
                    block_node.children.append(child)
                return block_node
        case BlockType.QUOTE:
            block_node = ParentNode("blockquote", [])
            children_nodes = text_to_children(block)
            for child in children_nodes:
                block_node.children.append(child)
            return block_node
        case BlockType.PARAGRAPH:
            block_node = ParentNode("p", [])
            children_nodes = text_to_children(block)
            for child in children_nodes:
                block_node.children.append(child)
            return block_node
        case BlockType.ORDERED_LIST:
            block_node = ParentNode("ol", [])
            split_lines = block.splitlines()
            for line in split_lines:
                children_nodes = text_to_children(line)
                item_node = ParentNode("li", [])
                for child in children_nodes:
                    item_node.children.append(child)
                block_node.children.append(item_node)
            return block_node
        case BlockType.UNORDERED_LIST:
            block_node = ParentNode("ul", [])
            split_lines = block.splitlines()
            for line in split_lines:
                children_nodes = text_to_children(line)
                item_node = ParentNode("li", [])
                for child in children_nodes:
                    item_node.children.append(child)
                block_node.children.append(item_node)
            return block_node
        case BlockType.CODE:
            code_node = LeafNode("code", block)
            block_node = ParentNode("pre", [code_node])
            return block_node
