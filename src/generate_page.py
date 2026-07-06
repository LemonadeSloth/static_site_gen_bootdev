from ntpath import isfile

from markdown_to_html import markdown_to_html_node
import os

def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("no h1/# title")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.exists(from_path):
        raise ValueError(f"no {from_path} exists")
    with open(from_path) as md_file:
        md_content = md_file.read()
    #print(md_content)

    if not os.path.exists(template_path):
        raise ValueError(f"no {template_path} exists")
    with open(template_path) as template_file:
        template_content = template_file.read()

    title = extract_title(md_content)

    html_nodes = markdown_to_html_node(md_content)
    html_string = html_nodes.to_html()

    html_page = template_content.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as result:
        result.write(html_page)

def generate_page_recursive(dir_path_content: str = "./content/", template_path: str = "./template.html", dest_dir_path: str = "./public/") -> None:

    if not os.path.exists(dir_path_content):
        raise ValueError("invalid content path")
    
    items = os.listdir(dir_path_content)
    for item in items:
        item_src_path = os.path.join(dir_path_content, item)
        item_dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_src_path):
            if item.endswith(".md"):
                item_dest_path = item_dest_path.replace(".md", ".html")
                generate_page(item_src_path, template_path, item_dest_path)
        else: #item is a dir
            generate_page_recursive(item_src_path, template_path, item_dest_path)
