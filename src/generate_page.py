from blockfunctions import *
from htmlnode import *
import os
from pathlib import Path

# find the title
def extract_title(markdown):
    lines = markdown.splitlines()

    for line in lines:
        if line.startswith("# "):
            line = line[2:]
            return line.strip()
    
    raise Exception("Missing h1 header")


def generate_page(from_path , template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    # read input markdown
    with open(from_path , "r") as f:
        input_file = f.read()
    
    # read template
    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(input_file).to_html() # turn the markdown file into HTML
    title = extract_title(input_file) # get the title

    # replace title and content placeholder in the template with the title and content from input file
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    
    # get the parent folder path string of the destination file/folder
    dest_parent_path = os.path.dirname(dest_path)

    # validate the parent folders, create these folders if they don't exist
    if dest_parent_path:
        os.makedirs(dest_parent_path, exist_ok=True)

    # write page with the content from input file (generate the page)
    with open(dest_path , "w") as f:
        f.write(template)



def generate_pages_recursive(dir_path_content , template_path , dest_dir_path, basepath):

    if not os.path.exists(dir_path_content):
        raise Exception("Content path is not valid")
    
    content_list = os.listdir(dir_path_content)
    print(f"content_list = {content_list}")
    for item in content_list:
        item_path = os.path.join(dir_path_content, item)
        print(item_path)
        p = Path(item_path)

        # checking if it's a file or dir
        if os.path.isfile(item_path):
            if p.suffix == ".md":
                print(os.path.join(dest_dir_path, p.stem+".html"))
                generate_page(item_path, template_path, os.path.join(dest_dir_path, p.stem + ".html"), basepath) # create a new HTML file at the destination
            else:
                continue # skip file that is not .md
        elif p.is_dir(): # check if directory
            generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item), basepath)
