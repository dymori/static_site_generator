import unittest

from extract import extract_markdown_images, extract_markdown_links, extract_title

class TestExtractMarkdownImages(unittest.TestCase):
   def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

   def test_extract_markdown_images_multiple(self):
    matches = extract_markdown_images(
        "This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png), another ![image2](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image1", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
   def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is text with an [link](https://example.com)"
    )
    self.assertListEqual([("link", "https://example.com")], matches)

   def test_extract_markdown_links_multiple(self):
    matches = extract_markdown_links(
        "This is text with an [link1](https://example.com), [link2](https://example.com)"
    )
    self.assertListEqual([("link1", "https://example.com"),("link2", "https://example.com")], matches)

class TestExtractMarkdownTitle(unittest.TestCase):
    def test_extract_markdown_title(self):
        matches = extract_title("# Test")
        self.assertEqual("Test", matches)

    def test_extract_markdown_title_multiple_line(self):
        matches = extract_title("""# Test
            ## Test2
            ### Test3
        """)
        self.assertEqual("Test", matches)
    
    def test_extract_markdown_title_no_title(self):
        with self.assertRaises(Exception):
            extract_title("Test")

if __name__ == "__main__":
    unittest.main()
