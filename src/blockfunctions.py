from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from functions import text_to_textnode
from textnode import text_node_to_html_node
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    result = []
    split_string = markdown.split("\n\n")
    for block in split_string:
        # checking empty block
        if not block:
            continue
        else:
            result.append(block.strip())
    return result

# inspect a block of markdown text and determine what type of block it is
def block_to_block_type(markdown_block):
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ", "####### ")) :
        return BlockType.HEADING
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE

    markdown_block = markdown_block.strip()
    split_block = markdown_block.split("\n")

    count = 0
    for line in split_block:
        line = line.lstrip()
        if line.startswith("> ") or line == ">":
            count+=1
    if count == len(split_block):
        return BlockType.QUOTE

    count = 0
    for line in split_block:
        if line.startswith("- "):
            count+=1
    if count == len(split_block):
        return BlockType.UNORDERED_LIST
    
    count = 0
    i=0
    if markdown_block[0].isdigit(): # if there is any number at first, check if it is an ordered list.
        for line in split_block:
            first, second = line.split(".",1)
            if first.isdigit() and first == str(i+1) and second.startswith(" "):
                count+=1
                i+=1
        if count == len(split_block):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

# turn a markdown into HTML
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown) # break raw document into seperate blocks
    all_block_nodes = []

    # process each block
    for block in blocks:
        block_type = block_to_block_type(block)
    
        if block_type == BlockType.CODE:
            all_block_nodes.append(code_block_to_html(block))
        elif block_type == BlockType.HEADING:
            all_block_nodes.append(heading_block_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            all_block_nodes.append(quote_block_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            all_block_nodes.append(ordered_list_block_to_html(block))
        elif block_type == BlockType.UNORDERED_LIST:
            all_block_nodes.append(unordered_list_block_to_html_node(block))
        else:
            all_block_nodes.append(paragraph_block_to_html_node(block))
    
    return HTMLNode("div", None, all_block_nodes)


# helper functions
# =======================================================================================

# take a whole block of paragraph and proceed it, turn it into TextNode and HTML node
def paragraph_block_to_html_node(block):
    lines_list = block.split("\n")
    strip_line = []
    for line in lines_list:
        strip_line.append(line.strip())
    
    # drop empty line after stripping
    new_strip_line = []
    for line in strip_line:
        if line == "":
            continue
        new_strip_line.append(line)

    paragraph = " ".join(new_strip_line) # rejoin line into one string
    children_nodes = text_to_children(paragraph) # list of HTML children node

    return HTMLNode("p", None , children_nodes)

# turn heading block into HTML node
def heading_block_to_html_node(block):
    count = 0
    i=0
    while block[i] != " " and i < len(block):
        if block[i] == "#":
            count += 1
        i +=1

    tag = f"h{count}"
    text = block[count+1:]
    text = text.strip()
    children_nodes = text_to_children(text)
    return HTMLNode(tag, None, children_nodes)

def quote_block_to_html_node(block):
    block = block.split("\n")
    strip_line = []
    for line in block:
        if line == "":
            continue
        line = line[2:]
        strip_line.append(line)

    new_strip_line = []
    for line in strip_line:
        if line == "":  # skipping empty line after strip
            continue
        new_strip_line.append(line)

    rejoin_lines = "\n".join(new_strip_line)
    children_nodes = text_to_children(rejoin_lines)
    return HTMLNode("blockquote", None, children_nodes)

def unordered_list_block_to_html_node(block):
    block = block.split("\n")
    strip_line = []
    for line in block:
        line = line[2:]
        if line.strip() == "":
            continue # skipping white space after strip
        strip_line.append(line)
    
    li_node_children = []
    for item in strip_line:
        children = text_to_children(item) # break each line of item into textnode list
        li_node_children.append(HTMLNode("li", None, children)) # adding tag <li> to each item 
    
    return HTMLNode("ul", None, li_node_children)

def ordered_list_block_to_html(block):
    block = block.split("\n")
    strip_line = []
    
    for line in block:
        i = 0
        while i < len(line) and line[i].isdigit():
            i+=1

        if i == 0: # line is not an item in ordered list, skip
            continue

        if i >= len(line) or line[i] != '.':
            continue    # skip if no dot next to digit
        else:
            i +=1

        if i < len(line) and line[i] == ' ':
            i += 1
        
        line = line[i:]
        if line.strip() == "":
            continue # skip white space after strip
        strip_line.append(line)
    
    li_node_children = []
    for item in strip_line:
        children = text_to_children(item) # break each item into list of HTML children
        li_node_children.append( HTMLNode("li", None , children)) # add <li> tag to each item
    
    return HTMLNode("ol", None, li_node_children)

def code_block_to_html(block):
    lines = block.splitlines(True) # True make it keep the newline character, example "a\nb\nc\n" -> [a\n , b\n, c\n]. if no True -> [a,b,c]

    if not lines: # if it is empty code block, return an empty HTML node
        return HTMLNode("pre", None, [text_node_to_html_node(TextNode("", TextType.CODE))])
    
    if lines[0].startswith('```'):
        lines = lines[1:] # drop first line
    if lines[-1].strip() == '```':
        lines = lines[:-1]  # drop last line

    lines = "".join(lines) # rejoin 
    lines = TextNode(lines, TextType.CODE)
    lines = text_node_to_html_node(lines)
    return HTMLNode("pre", None, [lines])


# turn block into text node, then turn each text node into HTML leafnode 
def text_to_children(block):
    if block is None or block == " ":
        return []
    
    children_list = []
    list_of_textnode = text_to_textnode(block)

    for textnode in list_of_textnode:
        if textnode is None or textnode.text == " ":
            continue  
        children_list.append(text_node_to_html_node(textnode))
    
    return children_list