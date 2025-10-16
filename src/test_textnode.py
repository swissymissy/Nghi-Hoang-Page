import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node1= TextNode("Test different url", TextType.LINK, "http://webpage_number_1")
        node2= TextNode("Test different url", TextType.LINK)
        self.assertNotEqual(node1, node2)

    def test_text(self):
        node1 = TextNode("This is text of node number 1", TextType.BOLD)
        node2 = TextNode("Mot con vit xoe ra 2 cai canh", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_type(self):
        node1 = TextNode("mot ong sao sang", TextType.IMAGE)
        node2 = TextNode("mot ong sao sang", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_text_node_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()