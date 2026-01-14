from textnode import *
import shutil, os, sys
from block_markdown import *
from pathlib import Path


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    

    try:
        clean_copy("static", "docs", False)
        # generate_page("content/index.md", "template.html", "public/index.html")
        generate_pages_recursive("content", "template.html", "docs", basepath)
    except Exception as e:
        print(e)


def clean_copy(src, dst, deleted=True):
    if not os.path.exists(src):
        raise Exception(f"invalid path: {src}")
    if not deleted:
        if not os.path.exists(dst):
            os.mkdir(dst)
        elif os.path.isdir(dst):
            shutil.rmtree(dst)
            os.mkdir(dst)
        else:
            raise Exception(f"invalid path to directory: {dst}")
    if os.listdir(src) == os.listdir(dst):
        return
    for path in os.listdir(src):
        file_path = os.path.join(src, path)
        if os.path.isfile(file_path):
            shutil.copy(file_path, dst)
        else:
            dst_path = os.path.join(dst, path)
            os.mkdir(dst_path)
            clean_copy(file_path, dst_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md_src = f.read()
    with open(template_path) as f:
        template = f.read()
    
    html = markdown_to_html_node(md_src).to_html()
    title = extract_title(md_src)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    template = Path(template_path).read_text()
    for entry in Path(dir_path_content).iterdir():
        if entry.is_file() and entry.suffix == ".md":
            md = entry.read_text()
            html = markdown_to_html_node(md).to_html()
            title = extract_title(md)
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html)
            template = template.replace('href="/', f'href="{basepath}')
            final_html = template.replace('src="/', f'src="{basepath}')

            file = Path(dest_dir_path) / Path(f"{entry.stem}.html")
            file.write_text(final_html)
        else:
            dst_path = Path(dest_dir_path) / Path(entry.name)
            dst_path.mkdir()
            generate_pages_recursive(entry, template_path, dst_path, basepath)

main()

# P = Path("content")
# for entry in P.iterdir():
    # print(entry)