import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_tag_value_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        
    def test_tag_value_to_html_single_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
        
    def test_tag_value_to_html_multiple_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\" target=\"_blank\">Click me!</a>")
        
    def test_value_to_html(self):
        node = LeafNode(None, "Click me!")
        self.assertEqual(node.to_html(), "Click me!")


if __name__ == "__main__":
    unittest.main()
