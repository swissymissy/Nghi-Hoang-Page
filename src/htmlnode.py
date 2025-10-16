
class HTMLNode:
    # constructor 
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # tag name (e.g. "p", "a". "h1", etc)
        self.value = value # value of HTML tag (text inside tag)
        self.children = children # list of HTML objects
        self.props = props # dictionary represents attributes of HTML tag

    # return the HTML string of the HTML node
    def to_html(self):
        if self.tag is None:
            return self.value
        if self.children:
            inner_block = "".join(child.to_html() for child in self.children) # joining all the HTML children into one big inner block
        else:
            inner_block = self.value 
        if self.props:
            attributes = " " + " ".join(f'{key}="{value}"' for key,value in self.props.items()) # HTML attributes need quotes and spaces between pairs
        else:
            attributes = ""
        return f'<{self.tag}{attributes}>{inner_block}</{self.tag}>' # return the HTML string
    
    # print a string that represents the HTML attribute of the node
    def props_to_html(self):
        string = ""
        if self.props == None:
            return ""
        if len(self.props) == 0:
            return ""
        for key,val in self.props.items():
            string += f' {key}="{val}"'
        return string
    
    # print an HTMLNode object, useful for debugging
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

# child class of HTMLNode - LeafNode
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        # check if value is empty
        if self.value is None:
            raise ValueError("invalid HTML: no value")

        if self.tag is None:
            return self.value
        elif self.props is None or self.props == {}:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            key, value = next(iter(self.props.items()))
            return f'<{self.tag} {key}="{value}">{self.value}</{self.tag}>'
        
# child class ParentNode
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.tag is None or self.tag == "" :
            raise ValueError("tag is missing")
        if self.children is None:
            raise ValueError("children is None")
        elif (len(self.children) == 0):
            raise ValueError("children list is empty")
        
        string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            string += child.to_html()
        return f"{string}</{self.tag}>"
