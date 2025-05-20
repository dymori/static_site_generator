import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        # Test with no props
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")
        
    def test_props_to_html_single_prop(self):
        # Test with a single prop
        node = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
        
    def test_props_to_html_multiple_props(self):
        # Test with multiple props
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        # You'll need to check if it contains both attributes with leading spaces
        result = node.props_to_html()
        self.assertTrue(' href="https://example.com"' in result)
        self.assertTrue(' target="_blank"' in result)


if __name__ == "__main__":
    unittest.main()
