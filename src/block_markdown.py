from enum import Enum
from htmlnode import *
from inline_markdown import *
from textnode import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks_list = []
    for block in blocks:
        if block == "":
            continue
        blocks_list.append(block.strip())
    return blocks_list

def block_to_block_type(block):
    if len(block) > 1:
        if block[0] == "#":
            for i in range(1, len(block)):
                if block[i] == "#":
                    if i >= 6:
                        return BlockType.PARAGRAPH
                    continue
                elif block[i] == " ":
                    return BlockType.HEADING
                else:
                    return BlockType.PARAGRAPH
        elif block[:2] == "``":
            lines = block.splitlines()
            if len(lines) < 2 or len(lines[0]) != 3 or len(lines[-1]) < 3:
                return BlockType.PARAGRAPH
            if lines[0] == "```":
                if lines[-1][-3:] == "```":
                    return BlockType.CODE
        elif block[0] == ">":
            lines = block.splitlines()
            for line in lines:
                if line.startswith(">"):
                    if len(line.strip()) > 1 and line[1] != " ":
                        return BlockType.PARAGRAPH
                # if line.strip() == "" or line[0] != ">" or line.strip()[0:2] != "> ":
            return BlockType.QUOTE
        elif block[:2] == "- ":
            lines = block.splitlines()
            for line in lines:
                if len(line) < 2 or line[0:2] != "- ":
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        elif block[1] == ".":
            lines = block.splitlines()
            for i in range(len(lines)):
                if len(lines[i]) < 3 or lines[i][:3] != f"{i + 1}. ":
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_nodes.append(block_to_HTMLNode(block, block_type))
    parent_node = ParentNode("div", children=block_nodes)
    return parent_node

def block_to_HTMLNode(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            lines = ""
            child_nodes = []
            texts = block.splitlines()
            for text in texts:
                lines += f"{text.strip()+" "}"
            return ParentNode("p", children=text_to_children(lines.strip()))
        case BlockType.QUOTE:
            lines = ""
            child_nodes = []
            texts = block.splitlines()
            for text in texts:
                if len(text) > 1:
                    child_nodes.append(ParentNode("p", children=text_to_children(f"{text.split("> ", 1)[1]}".strip())))
                    # lines += f"{text.split("> ", 1)[1]}"
            # return ParentNode("blockquote", children=text_to_children(lines[:-1]))
            return ParentNode("blockquote", children=child_nodes)
        case BlockType.UNORDERED_LIST:
            lines = ""
            child_nodes = []
            texts = block.splitlines()
            for text in texts:
                child_nodes.append(ParentNode("li", children=text_to_children(f"{text.split("- ", 1)[1]}")))
            return ParentNode("ul", children=child_nodes)
        case BlockType.ORDERED_LIST:
            lines = ""
            child_nodes = []
            texts = block.splitlines()
            for text in texts:
                child_nodes.append(ParentNode("li", children=text_to_children(f"{text.split(". ", 1)[1]}")))
            return ParentNode("ol", children=child_nodes)
        case BlockType.CODE:
            child_node = text_node_to_html_node(TextNode(block[4:-3], TextType.TEXT))
            parent_node = ParentNode("pre", [ParentNode("code", [child_node])])
            return parent_node
        case BlockType.HEADING:
            for i in range(1, len(block)):
                if block[i] == " ":
                    return ParentNode(f"h{i}", children=text_to_children(f"{block.split(" ", 1)[1]}"))
                

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children_nodes = []
    for text_node in text_nodes:
        children_nodes.append(text_node_to_html_node(text_node))
    return children_nodes

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if block[1] == " ":
                return block[2:].strip()
    raise Exception("No header h1 found")