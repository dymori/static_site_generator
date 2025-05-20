import unittest

from textnode import TextNode, TextType
from utils import text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "www.imageurl.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "www.imageurl.com")
        self.assertEqual(html_node.props["alt"], "This is a image node")

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_no_delimiter(self):
        # Test when no delimiter is present
        node = TextNode("Plain text with no delimiter", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Plain text with no delimiter")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_bold_delimiter(self):
        # Test with bold delimiter
        node = TextNode("Text with a **bold** word", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " word")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_code_delimiter(self):
        # Test with code delimiter
        node = TextNode("Here is some `inline code` in text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Check we have the correct number of resulting nodes
        self.assertEqual(len(result), 3)
        
        # Check the first node (text before code)
        self.assertEqual(result[0].text, "Here is some ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        
        # Check the second node (the code)
        self.assertEqual(result[1].text, "inline code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        
        # Check the third node (text after code)
        self.assertEqual(result[2].text, " in text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_code_delimiters(self):
        # Test with multiple code blocks
        node = TextNode("Code: `first` and `second` blocks", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Check we have the correct number of resulting nodes
        self.assertEqual(len(result), 5)
        
        # Check each node
        self.assertEqual(result[0].text, "Code: ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        
        self.assertEqual(result[1].text, "first")
        self.assertEqual(result[1].text_type, TextType.CODE)
        
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        
        self.assertEqual(result[3].text, "second")
        self.assertEqual(result[3].text_type, TextType.CODE)
        
        self.assertEqual(result[4].text, " blocks")
        self.assertEqual(result[4].text_type, TextType.TEXT)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_node_image_no_image(self):
        node = TextNode("Testing no image", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])
    
    def test_split_node_images_one_image(self):
        node = TextNode("Testing ![image](https://i.imgur.com/zjjcJKZ.png) image", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result[0], TextNode("Testing ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"))
        self.assertEqual(result[2], TextNode(" image", TextType.TEXT))

    def test_split_node_images_single_image_line(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"))

class TestSplitNodesLink(unittest.TestCase):
    def test_split_node_link_no_link(self):
        node = TextNode("Testing no link", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])
    
    def test_split_node_links_one_link(self):
        node = TextNode("Testing [link](https://i.imgur.com/zjjcJKZ.png) link", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result[0], TextNode("Testing ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"))
        self.assertEqual(result[2], TextNode(" link", TextType.TEXT))

    def test_split_node_links_single_link_line(self):
        node = TextNode("[link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"))

class TestTextToTextNodes(unittest.TestCase):
    def test_split_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "# Test"
        blockType = block_to_block_type(block)
        self.assertEqual(
            blockType,
            BlockType.HEADING,
        )
    def test_block_to_block_type_paragraph(self):
        block = "Test"
        blockType = block_to_block_type(block)
        self.assertEqual(
            blockType,
            BlockType.PARAGRAPH,
        )

class TestMarkDownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
