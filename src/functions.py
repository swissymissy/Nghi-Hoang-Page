import re #regex
from textnode import TextType, TextNode

# used for spliting the texts in each node by using the delimiter from text type
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
                temp_list = []
                split_text = node.text.split(delimiter)
                for i in range(len(split_text)):
                    #checking unmatched delimiter
                    if len(split_text) % 2 == 0:
                         raise Exception("unmatched delimiter")
                    
                    # skipping trailing " "
                    if split_text[i] == '':
                         continue
                    
                    if (i % 2 == 0):
                        temp_list.append(TextNode(split_text[i], TextType.TEXT))
                    else:
                        temp_list.append(TextNode(split_text[i], text_type))
                result.extend(temp_list)
        else:
             result.append(node)
    return result

# takes raw markdown text and returns a list of tuples
def extract_markdown_images(text):
     result = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
     return result

# extract markdown links from text
def extract_markdown_links(text):
     result = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
     return result

# split raw markdown text into TextNode's based on images and links
def split_nodes_image(old_nodes):
     textnode_list = []
     for node in old_nodes:

          # checking is node is empty text node
          if node.text == None or node.text == "":
               continue

          # checking if node has text_type of TEXT
          if node.text_type != TextType.TEXT:
               textnode_list.append(node)
               continue
          
          temp_list = []
          extracted_imgs = extract_markdown_images(node.text) # list of (img, url) pair
          rest = node.text 

          # no image in this node, append it to list unchanged
          if len(extracted_imgs) == 0:
               textnode_list.append(node)
               continue

          # start spliting text into parts using (img, url) as delim
          for img in extracted_imgs:
               delim = f"![{img[0]}]({img[1]})"
               before, rest = rest.split(delim, maxsplit=1) # assign before(str) = the string before the delimiter, rest(str) = string after the delimiter 

               if before:
                    temp_list.append(TextNode(before, TextType.TEXT))   # adding TEXT node to the list
               temp_list.append(TextNode(img[0], TextType.IMAGE, img[1]))  # adding IMAGE node to the list 

          if rest:
               temp_list.append(TextNode(rest, TextType.TEXT)) # if after spliting and there is still text remaining, add the text node to list, but skip the trailing empty string
          textnode_list.extend(temp_list)

     return textnode_list

# split raw markdown text into TextNode based on link. Return a list of new nodes
def split_nodes_link(old_nodes):
     textnode_list = []
     for node in old_nodes:

          # checking is node is empty text node
          if node.text == None or node.text == "":
               continue

          # checking if node has text_type of TEXT
          if node.text_type != TextType.TEXT:
               textnode_list.append(node)
               continue
          
          temp_list = []
          extracted_links = extract_markdown_links(node.text) # list of (link, url) pair
          rest = node.text 

          # no image in this node, append it to list unchanged
          if len(extracted_links) == 0:
               textnode_list.append(node)
               continue

          # start spliting text into parts using (link, url) as delim
          for link in extracted_links:
               delim = f"[{link[0]}]({link[1]})"
               before, rest = rest.split(delim, maxsplit=1) # assign before(str) = the string before the delimiter, rest(str) = string after the delimiter 

               if before:
                    temp_list.append(TextNode(before, TextType.TEXT))   # adding TEXT node to the list
               temp_list.append(TextNode(link[0], TextType.LINK, link[1]))  # adding LINK node to the list 

          if rest:
               temp_list.append(TextNode(rest, TextType.TEXT)) # if after spliting and there is still text remaining, add the text node to list, but skip the trailing empty string
          textnode_list.extend(temp_list)

     return textnode_list

# convert a raw string markdown text into a list of TextNode objects
def text_to_textnode(text):

     # create new text node
     textnode = TextNode(text, TextType.TEXT)
     node_list = [textnode]

     # delimiting by type: BOLD, ITALIC, CODE
     node_list = split_nodes_delimiter(node_list, '**', TextType.BOLD) # bold
     node_list = split_nodes_delimiter(node_list, '_' , TextType.ITALIC) # italic 
     node_list = split_nodes_delimiter(node_list, '`' , TextType.CODE) # split by code

     # extract images and links
     node_list = split_nodes_image(node_list)
     node_list = split_nodes_link(node_list)

     return node_list



