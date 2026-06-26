import unittest

from block_markdown import (BlockType,  # pyright: ignore[reportMissingImports]
                            block_to_type_no_regex, block_to_type_regex,
                            markdown_to_blocks)


class TestMDtoBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToType(unittest.TestCase):

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_type_no_regex(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_type_no_regex(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_type_no_regex(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_type_no_regex(
            block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_type_no_regex(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)
    
    def test_ordered_list(self):
        block = "1. list\n2. items\n3. items\n4. items\n5. items"
        self.assertEqual(block_to_type_no_regex(block), BlockType.ORDERED_LIST)
        block = "1. list"
        self.assertEqual(block_to_type_no_regex(block), BlockType.ORDERED_LIST)

    def test_incorrect_ordered_list(self):
        block = "2. list\n2. items\n3. items\n4. items\n5. items"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)
        block = "1. list\n3. items\n2. items"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)
        block = "1. list\n2. items\n3.items"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)
        block = "1. list\n2.items\n3.items"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)
        block = "1. list\n2."
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)

    def test_incorrect_unordererd_list(self):
        block = "- item1\n- item2\n-item3"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)
        block = "- item1\n- item2\nitem3"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)
        block = "- item1\n- item2\n-"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)

    def test_quote(self):
        block = "> quote\n> quote2 \n>quote3"
        self.assertEqual(block_to_type_no_regex(block), BlockType.QUOTE)

    def test_incorrect_quote(self):
        block = "> quote\n >quote2 \n>quote3"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)
        block = "> quote\n> quote2 \nquote3"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)

    def test_code(self):
        block = "```\ncode\ncode2\ncode4\n \n```"
        self.assertEqual(block_to_type_no_regex(block), BlockType.CODE)

    def test_incorrect_codel(self):
        block = "```\ncode\ncode2\n``"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)

    def test_headings(self):
        block = "# heading1"
        self.assertEqual(block_to_type_no_regex(block), BlockType.HEADING)
        block = "## heading 2"
        self.assertEqual(block_to_type_no_regex(block), BlockType.HEADING)
        block = "### heading 3"
        self.assertEqual(block_to_type_no_regex(block), BlockType.HEADING)
        block = "#### heading 4"
        self.assertEqual(block_to_type_no_regex(block), BlockType.HEADING)
        block = "##### heading 5"
        self.assertEqual(block_to_type_no_regex(block), BlockType.HEADING)
        block = "###### heading 6"
        self.assertEqual(block_to_type_no_regex(block), BlockType.HEADING)

    def test_incorrect_headings(self):
        block = "####### headings"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)
        block = "#heading"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)
        block = "######heading"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
