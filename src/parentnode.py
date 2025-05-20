from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is missing")
        if self.children is None:
            raise ValueError("Children is missing")
        props = ""
        if self.props is not None and len(self.props) > 0:
            for prop in self.props:
                props += f" {prop}=\"{self.props[prop]}\""
        children = ""
        if len(self.children) > 0:
            for child in self.children:
                children += child.to_html()
        return f"<{self.tag}{props}>{children}</{self.tag}>"