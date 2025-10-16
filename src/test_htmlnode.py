import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode     

test_dict = {
    "href": "http://www.google.com",
    "target": "_blank"
}

class TestHTMLNode(unittest.TestCase):

    def test_props(self):
        node= HTMLNode("p", "hai con than lan con", None, test_dict)
        node.props_to_html()

    # test props = None
    def test_props1(self):
        node= HTMLNode("a", "mot ong sao sang", None, None)
        node.props_to_html()

    # test props = {}
    def test_props2(self):
        node = HTMLNode("a", "hai ong sang sao", None, {})
        node.props_to_html()
    

    def test_repr(self):
        node = HTMLNode("a", "ba ong sao sang", None, test_dict)
        node.__repr__()
    
    # test LeafNode =======
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_tag(self):
        node = LeafNode(None, "Is this real?!", test_dict)
        self.assertEqual(node.to_html(),"Is this real?!")

    def test_leaf_to_html_value(self):
        node = LeafNode("p", None, test_dict)
        with self.assertRaises(ValueError):
            node.to_html()
    
    # test ParentNode 
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
        
if __name__ == "__main__":
    unittest.main()