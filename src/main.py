from textnode import TextNode, TextType
from copystatic import copy_static
from generate import generate_page, generate_pages_recursive
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_static("static", "docs")
    generate_pages_recursive("content/", "template.html", "docs/", basepath)

if __name__ == "__main__":
    main()