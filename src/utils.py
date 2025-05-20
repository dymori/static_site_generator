from textnode import TextNode, TextType
from leafnode import LeafNode
from extract import extract_markdown_images, extract_markdown_links
from enum import Enum
import re
from htmlnode import HTMLNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.text is None:
                raise ValueError("Text is required")
            if text_node.url is None:
                raise ValueError("URL is required")
            return LeafNode("a", text_node.text, { "href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("URL is required")
            if text_node.text is None:
                raise ValueError("Alt text is highly recommended")
            return LeafNode("img", "", { "src": text_node.url, "alt": text_node.text })
        case _:
            raise Exception("No such text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            # Process text nodes - this is where recursion could happen
            processed_nodes = process_text_node(node, delimiter, text_type)
            result.extend(processed_nodes)  # Add all resulting nodes
            
    return result

def split_nodes_image(old_nodes):
    result = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        curr_text = node.text
        if len(images) > 0:
            for image in images:
                split = curr_text.split(f"![{image[0]}]({image[1]})", 1)
                if split[0] != "":
                    result.append(TextNode(f"{split[0]}",TextType.TEXT))
                result.append(TextNode(image[0], TextType.IMAGE, image[1]))
                curr_text = split[1]
            if curr_text != "":
                result.append(TextNode(curr_text, TextType.TEXT))
        else:
            result.append(node)
    return result

def split_nodes_link(old_nodes):
    result = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        curr_text = node.text
        if len(links) > 0:
            for link in links:
                split = curr_text.split(f"[{link[0]}]({link[1]})", 1)
                if split[0] != "":
                    result.append(TextNode(f"{split[0]}",TextType.TEXT))
                result.append(TextNode(link[0], TextType.LINK, link[1]))
                curr_text = split[1]
            if curr_text != "":
                result.append(TextNode(curr_text, TextType.TEXT))
        else:
            result.append(node)
    return result

def process_text_node(node, delimiter, text_type):
    # Base case: no delimiter found
    text = node.text
    start_index = text.find(delimiter)
    
    if start_index == -1:
        return [node]  # Return the node unchanged
        
    # Find closing delimiter
    end_index = text.find(delimiter, start_index + len(delimiter))
    
    if end_index == -1:
        raise Exception(f"No closing delimiter found for {delimiter}")
    
    # Split into three parts
    before_text = text[:start_index]
    delimited_text = text[start_index + len(delimiter):end_index]
    after_text = text[end_index + len(delimiter):]
    
    result = []
    
    # Add the text before the delimiter
    if before_text:
        result.append(TextNode(before_text, TextType.TEXT))
    
    # Add the delimited text with the specified type
    result.append(TextNode(delimited_text, text_type))
    
    # Process any remaining text recursively
    if after_text:
        after_node = TextNode(after_text, TextType.TEXT)
        result.extend(process_text_node(after_node, delimiter, text_type))
    
    return result

def text_to_textnodes(text):
    # Start with a single text node
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply each splitting function in sequence
    # First, split by delimiters for bold, italic, and code
    # Then handle special cases like images and links
    bold_split = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)
    image_split = split_nodes_image(code_split)
    link_split = split_nodes_link(image_split)
    
    # Return the final list of nodes
    return link_split

def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    blocks = []
    current_block = []
    in_code_block = False
    
    for line in lines:
        # Check if this line is a code block delimiter
        if line.strip().startswith("```"):
            # If we're starting a code block
            if not in_code_block:
                # If we have content in current_block, add it as a block
                if current_block:
                    blocks.append("\n".join(current_block))
                    current_block = []
                # Start a new code block
                current_block.append(line)
                in_code_block = True
            # If we're ending a code block
            else:
                # Add the closing delimiter to the current block
                current_block.append(line)
                # Add the complete code block
                blocks.append("\n".join(current_block))
                current_block = []
                in_code_block = False
        # If we're inside a code block, add the line as is
        elif in_code_block:
            current_block.append(line)
        # If line is empty and we're not in a code block
        elif not line.strip() and current_block and not in_code_block:
            # Add the completed block
            blocks.append("\n".join(current_block))
            current_block = []
        # If it's a non-empty line and we're not in a code block
        elif line.strip() and not in_code_block:
            current_block.append(line)
    
    # Don't forget to add the last block if it exists
    if current_block:
        blocks.append("\n".join(current_block))
    
    # Clean the blocks - remove any that are just whitespace
    blocks = [block for block in blocks if block.strip()]
    
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split('\n')
    
    if len(lines) == 1 and re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING
    elif block.strip().startswith("```") and block.strip().endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") and line != "" for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") and line != "" for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{index}. ") and line != "" for index, line in enumerate(lines, 1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def text_to_children(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = HTMLNode("div", None, [], {})
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            # Process the text inside the paragraph for inline markdown
            # This would convert things like **bold** to <b>bold</b>
            normalized_text = re.sub(r'\s+', ' ', block.strip())
            children = text_to_children(normalized_text)
            
            # Create the paragraph node with the processed children
            paragraph_node = HTMLNode("p", None, children, {})
            
            # Add the paragraph node as a child to the parent div
            parent_node.children.append(paragraph_node)
        elif block_type == BlockType.HEADING:
            # Count the leading # characters to determine heading level
            heading_level = 0
            for char in block:
                if char == '#':
                    heading_level += 1
                else:
                    break
            
            # Extract the heading text (removing the leading # and space)
            heading_text = block[heading_level:].strip()
            
            # Convert heading text to HTML nodes
            heading_children = text_to_children(heading_text)
            
            # Create the heading node
            heading_node = HTMLNode(f"h{heading_level}", None, heading_children, {})
            
            # Add the heading node to the parent
            parent_node.children.append(heading_node)
        elif block_type == BlockType.CODE:
            # Extract content between the triple backticks
            lines = block.strip().split("\n")
            
            # Remove the opening and closing ```
            content_lines = lines[1:-1]  
            
            # Join the content lines and add a trailing newline
            content = "\n".join(line.lstrip() for line in content_lines) + "\n"
            
            # Create a text node (no inline parsing)
            text_node = TextNode(content, TextType.TEXT)
            
            # Create the code node
            code_node = HTMLNode("code", None, [text_node_to_html_node(text_node)], {})
            
            # Wrap in a pre tag
            pre_node = HTMLNode("pre", None, [code_node], {})
            parent_node.children.append(pre_node)
        elif block_type == BlockType.QUOTE:
            # Remove the '>' prefix from each line and join them
            lines = block.split('\n')
            quote_content = ""
            for line in lines:
                if line.startswith('>'):
                    # Strip the '>' and any leading space
                    content = line[1:].strip()
                    quote_content += content + " "  # Add space between lines
            
            # Process the quote content for inline markdown
            quote_children = text_to_children(quote_content.strip())
            
            # Create blockquote node
            quote_node = HTMLNode("blockquote", None, quote_children, {})
            
            # Add to parent
            parent_node.children.append(quote_node)
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split('\n')
            list_node = HTMLNode("ol", None, [], {})
            
            for line in lines:
                stripped_line = line.strip()
                # Check if line starts with a digit followed by a period
                if stripped_line and any(stripped_line.startswith(f"{i}.") for i in range(10)):
                    # Find the position of the period to extract content after it
                    period_pos = stripped_line.find('.')
                    if period_pos != -1:
                        # Extract content after the period
                        content = stripped_line[period_pos + 1:].strip()
                        
                        # Process inline markdown in the list item
                        item_children = text_to_children(content)
                        
                        # Create list item node
                        item_node = HTMLNode("li", None, item_children, {})
                        
                        # Add list item to the ordered list
                        list_node.children.append(item_node)
            
            # Add the ordered list to the parent
            parent_node.children.append(list_node)
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split('\n')
            list_node = HTMLNode("ul", None, [], {})  # Changed to ul for unordered list
            
            for line in lines:
                # Check if line is an unordered list item (starts with -, *, or +)
                stripped_line = line.strip()
                if stripped_line and stripped_line.startswith(("-", "*", "+")):
                    # Extract content after the marker
                    content = stripped_line[1:].strip()  # Remove the marker and whitespace
                    
                    # Process inline markdown in the list item
                    item_children = text_to_children(content)
                    
                    # Create list item node
                    item_node = HTMLNode("li", None, item_children, {})
                    
                    # Add list item to the unordered list
                    list_node.children.append(item_node)
            
            # Add the unordered list to the parent
            parent_node.children.append(list_node)
    return parent_node