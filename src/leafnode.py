from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self,  tag=None, value=None,  props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag == None:
            return self.value
        props = ""
        if self.props is not None and len(self.props) > 0:
            for prop in self.props:
                props += f" {prop}=\"{self.props[prop]}\""
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"