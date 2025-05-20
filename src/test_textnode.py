import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is text node 1", TextType.BOLD)
        node2 = TextNode("This is text node 2", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_not_eq2(self):
        node = TextNode("This has a url", TextType.LINK, "https://google.com")
        node2 = TextNode("This doesn't have a url", TextType.LINK)
        self.assertNotEqual(node, node2)
    def test_not_eq3(self):
        node = TextNode("This is a node", TextType.ITALIC)
        node2 = TextNode("This is a node", TextType.TEXT)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
