from extract import extract_title
from utils import markdown_to_html_node
import os

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, 'r').read()
    template_file = open(template_path, 'r').read()
    from_node = markdown_to_html_node(from_file)
    from_string = from_node.to_html()
    title = extract_title(from_file)
    hydrated_template = template_file.replace("{{ Title }}", title).replace("{{ Content }}", from_string).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        print(f"{hydrated_template}", file=f)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}")
    items = os.listdir(dir_path_content)
    for item in items:
        from_item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(from_item_path):
            item = item.replace("md", "html")
            dest_item_path = os.path.join(dest_dir_path, item)
            generate_page(from_item_path, template_path, dest_item_path, basepath)
        else:
            generate_pages_recursive(from_item_path, template_path, dest_item_path, basepath)