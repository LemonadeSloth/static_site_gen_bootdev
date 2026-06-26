import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    split_blocks = markdown.split("\n\n")
    return list(filter(lambda x: x != "", map(lambda x: x.strip(), split_blocks)))


def markdown_to_blocks_bootdev_solution(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


# bootdev solution, I added it here since it differes quite a bit from mine
def block_to_type_no_regex(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


# mine solution, works but is not as pretty


def block_to_type_no_regex_mine(block: str) -> BlockType:
    # For headings
    if block[0] == "#":
        for i in range(1, 6):
            if block[i] == "#":
                if i == 5:
                    if block[6] == " ":
                        return BlockType.HEADING
                continue
            elif block[i] == " ":
                return BlockType.HEADING
            else:
                break
        return BlockType.PARAGRAPH
    # for code
    elif block[:4] == "```\n" and block[-4:] == "\n```":
        return BlockType.CODE
    # for quote
    elif block[0] == ">":
        valid = True
        for line in block.splitlines():
            if line[0] != ">":
                valid = False
                break
        if valid:
            return BlockType.QUOTE
        else:
            return BlockType.PARAGRAPH
    # for unordered lists
    elif block[:2] == "- ":
        valid = True
        for line in block.splitlines():
            if line[:2] != "- ":
                valid = False
                break
        if valid:
            return BlockType.UNORDERED_LIST
        else:
            return BlockType.PARAGRAPH
    # for ordered lists
    elif block[:3] == "1. ":
        start = 1
        valid = True
        for line in block.splitlines():
            if line[:3] != str(start) + ". ":
                valid = False
                break
            else:
                start += 1
        if valid:
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH
    else:
        return BlockType.PARAGRAPH


def block_to_type_regex(block: str) -> BlockType:
    if re.match(r"```\n.*\n```", block, re.DOTALL):
        return BlockType.CODE
    elif re.match(r"#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"\A(?:^>.*\n*)+\Z", block, re.MULTILINE):
        return BlockType.QUOTE
    elif re.match(r"\A(?:^- .*\n*)+\Z", block, re.MULTILINE):
        return BlockType.UNORDERED_LIST
    elif re.match(r"\A(?:^[1-9]*\. .*\n*)+\Z", block, re.MULTILINE):
        return (
            BlockType.ORDERED_LIST
        )  # doesn't enforce numerical order of items in the list
    else:
        return BlockType.PARAGRAPH
