from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode

# create an enum using class syntax
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

# create class TextNode
class TextNode:
    #constructor
    def __init__(self, text, text_type, url=None):
        self.text = text                          # text content of the node
        self.text_type = text_type                # type of the text:bold, italic, etc.
        self.url = url                            # link or imag

    # if all of properties of 2 TextNode obj are equal
    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True

    # method that returns string representation of the TextNode
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b",text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", { "src": text_node.url , "alt": text_node.text} )
    else:
        raise Exception("Text type not supported")

