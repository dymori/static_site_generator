class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            return self.value or ""
        
        # Handle self-closing tags like <img> or <br>
        if self.children is None and self.value is None:
            return f"<{self.tag}{self.props_to_html()}>"
        
        # Handle regular tags with content
        children_html = ""
        if self.children:
            for child in self.children:
                children_html += child.to_html()
        
        value = self.value or ""
        return f"<{self.tag}{self.props_to_html()}>{value}{children_html}</{self.tag}>"
    
    def props_to_html(self):
        html = ""
        if (self.props==None):
            return html
        for prop in self.props:
            html += f" {prop}=\"{self.props[prop]}\""
        return html

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

