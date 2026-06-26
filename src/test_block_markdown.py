import unittest

from block_markdown import markdown_to_blocks, block_to_type_no_regex, block_to_type_regex, BlockType  # pyright: ignore[reportMissingImports]

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
        self.assertEqual (block_to_type_no_regex(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_type_no_regex(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_type_no_regex(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_type_no_regex(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_type_no_regex(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_type_no_regex(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
