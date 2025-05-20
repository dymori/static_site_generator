import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    # Test when tag is None
    def test_to_html_with_none_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    # Test when children is None
    def test_to_html_with_none_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    # Test with empty children list
    def test_to_html_with_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    # Test with multiple children
    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("b", "bold")
        child2 = LeafNode("i", "italic")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><b>bold</b><i>italic</i></div>")

    # Test with props
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>child</span></div>')

    # Test with multiple levels of nesting
    def test_to_html_with_deep_nesting(self):
        leaf1 = LeafNode("b", "bold")
        leaf2 = LeafNode("i", "italic")
        parent1 = ParentNode("p", [leaf1, leaf2])
        parent2 = ParentNode("div", [parent1])
        self.assertEqual(parent2.to_html(), "<div><p><b>bold</b><i>italic</i></p></div>")

    # Test with mix of LeafNode and ParentNode children
    def test_to_html_with_mixed_children(self):
        leaf1 = LeafNode("span", "text")
        child_parent = ParentNode("div", [LeafNode("b", "nested")])
        parent = ParentNode("section", [leaf1, child_parent])
        self.assertEqual(parent.to_html(), "<section><span>text</span><div><b>nested</b></div></section>")

    # Test with complex structure including props at multiple levels
    def test_to_html_complex_structure(self):
        child1 = LeafNode("a", "link", {"href": "https://example.com"})
        child2 = ParentNode("div", [LeafNode("p", "paragraph")], {"class": "content"})
        parent = ParentNode("section", [child1, child2], {"id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<section id="main"><a href="https://example.com">link</a><div class="content"><p>paragraph</p></div></section>'
        )


if __name__ == "__main__":
    unittest.main()
