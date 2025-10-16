import unittest
from textnode import TextNode, TextType
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnode

class TestFunctions(unittest.TestCase):

    # test unmatched delimiter
    def test_unmatched_delimiter(self):
        node1 = TextNode("this is **unmatched** delimiter**test", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node1], "**" , TextType.BOLD)
    
    # test trailing '' in split list
    def test_trailing_empty(self):
        node1 = TextNode("**This is** trailing **test**" , TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node1], "**" , TextType.BOLD),
                          [
                              TextNode("This is", TextType.BOLD, None),
                              TextNode(" trailing ", TextType.TEXT, None),
                              TextNode("test", TextType.BOLD, None)
                            ])
    
    # test italic delimiter
    def test_italic(self):
        node1 = TextNode("Italic_delimiter_test", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node1], "_" , TextType.ITALIC),
                         [
                             TextNode("Italic", TextType.TEXT, None),
                             TextNode("delimiter", TextType.ITALIC, None),
                             TextNode("test", TextType.TEXT, None)
                         ])
    
    # test extracting markdown images using regex
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    # test split images from node
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
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
    
    # test when node is not TEXT type
    def test_when_node_is_not_TEXT(self):
        node_list = [
            TextNode("This is a bold text", TextType.BOLD, "http://thisisnotsupposedtobedetected.com")]
        new_nodes = split_nodes_image(node_list)
        self.assertEqual(
            [TextNode("This is a bold text", TextType.BOLD, "http://thisisnotsupposedtobedetected.com")], new_nodes
        )

    # test split links from text node
    def test_split_links_from_node(self):
        node = TextNode(
            "This is a sentence that has links [link 1](http://linktosomething.com/abdFgHd) and another link [link link](https://linktoanotherlink.com/sdhfsgfj)", 
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is a sentence that has links ", TextType.TEXT),
                TextNode("link 1", TextType.LINK, "http://linktosomething.com/abdFgHd"),
                TextNode(" and another link ", TextType.TEXT),
                TextNode("link link", TextType.LINK, "https://linktoanotherlink.com/sdhfsgfj")
            ],
            new_nodes
        )

    def test_text_to_text_node_test(self):
        string = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnode(string),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )