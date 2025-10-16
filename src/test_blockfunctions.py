from blockfunctions import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node, paragraph_block_to_html_node, heading_block_to_html_node, quote_block_to_html_node, code_block_to_html, unordered_list_block_to_html_node, ordered_list_block_to_html
import unittest

class TestBlockFunctions(unittest.TestCase):
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

    def test_block_to_block_type_header(self):
        md = "# This is header"
        md1 = "## This is second header"
        md3 = "### This is third header"
        md4 = "#### This is forth header"
        md5 ="##This is not header"
        md6 = "########## To many #"

        self.assertEqual(block_to_block_type(md), BlockType.HEADING)
        self.assertEqual(block_to_block_type(md1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(md3), BlockType.HEADING)
        self.assertEqual(block_to_block_type(md4), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(md5), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(md6), BlockType.HEADING)
    
    def test_block_to_block_code(self):
        md = "```This is a lind of code```"
        md2 = "``` This is also line of code ```"
        md3 = "``` This is not line of code"

        self.assertEqual(block_to_block_type(md), BlockType.CODE)
        self.assertEqual(block_to_block_type(md2), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(md3), BlockType.CODE)
    
    def test_block_to_block_quote(self):
        md = """
> This is a quote
> "more quote"
> Please works normally
> Thank you~"""

        md1 = """> This is a quote\nbut this is not a quote"""

        md2 = "> This is another quote\n>but one is not\nthis also not quote"

        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(md1), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(md2), BlockType.QUOTE)
    
    def test_block_to_block_unordered_list(self):
        md = """- List
- yes
- yeah"""

        md1 = """- This is list\n- still list\nnot anymore"""

        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type(md1), BlockType.UNORDERED_LIST)

    def test_block_to_block_ordered_list(self):
        md = "1. one\n2. two\n3. three\n4. four\n5. five"

        md1 = "1.one\n2. two\n2. three"
        md2 = "21. one\n22. two"
        md3 = "1. one\n2. two\n3. three\n4. four\n5. five\n6. six\n7. seven\n8. eight\n9. nine\n10. ten\n11. eleven"

        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(md1), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(md2), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(md3), BlockType.ORDERED_LIST)
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_unordered_list(self):
        md = """
- This is a list:
- one
- two with _italic_
- three with **bold**
"""
        node = markdown_to_html_node(md)
        html_node = node.to_html()
        self.assertEqual(
            html_node,
            "<div><ul><li>This is a list:</li><li>one</li><li>two with <i>italic</i></li><li>three with <b>bold</b></li></ul></div>"
        )
    
    def test_ordered_list(self):
        md = """
1. first
2. second with `code`
3. third with **bold** and _em_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second with <code>code</code></li><li>third with <b>bold</b> and <i>em</i></li></ol></div>",
        )

    def test_paragraph_block_to_html_helper(self):
        md = """
This is just a normal paragraph
with lines.
And other elements
such as a **bold statement**
and an _italic statement_."""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                         "<div><p>This is just a normal paragraph with lines. And other elements such as a <b>bold statement</b> and an <i>italic statement</i>.</p></div>")

    def test_mixed_blocks(self):
        md ="""
# Title

This is a para with **bold** and `code`.""""""

- item one
- item two

```
raw _no_ **inline**
```

> quote line
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>This is a para with <b>bold</b> and <code>code</code>.</p><ul><li>item one</li><li>item two</li></ul><pre><code>raw _no_ **inline**\n</code></pre><blockquote>quote line</blockquote></div>"
        )