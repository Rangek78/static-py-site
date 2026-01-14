from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT or delimiter.strip() == "":
            split_nodes.append(old_node)
            continue
        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("invalid markdown syntax")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 != 0:
                split_nodes.append(TextNode(split_text[i], text_type))
            else:
                split_nodes.append(TextNode(split_text[i], TextType.TEXT))
    return split_nodes

def extract_markdown_images(text):
    match = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return match

def extract_markdown_links(text):
    match = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return match

def split_nodes_image(old_nodes):
    split_nodes = []
    for old_node in old_nodes:
        extracted_images = extract_markdown_images(old_node.text)
        if len(extracted_images) == 0 or old_node.text_type != TextType.TEXT:
            split_nodes.append(old_node)
            continue
        split_text = old_node.text
        for i in range(len(extracted_images)):
            split_text = split_text.split(f"![{extracted_images[i][0]}]({extracted_images[i][1]})", 1)
            if split_text[0] != "":
                split_nodes.append(TextNode(split_text[0], TextType.TEXT))
            split_nodes.append(TextNode(extracted_images[i][0], TextType.IMAGE, extracted_images[i][1]))
            if i == len(extracted_images) - 1:
                if split_text[1] != "":
                    split_nodes.append(TextNode(split_text[1], TextType.TEXT))
            else:
                split_text = split_text[1]
    return split_nodes

def split_nodes_link(old_nodes):
    split_nodes = []
    for old_node in old_nodes:
        extracted_links = extract_markdown_links(old_node.text)
        if len(extracted_links) == 0 or old_node.text_type != TextType.TEXT:
            split_nodes.append(old_node)
            continue
        split_text = old_node.text
        for i in range(len(extracted_links)):
            split_text = split_text.split(f"[{extracted_links[i][0]}]({extracted_links[i][1]})", 1)
            if split_text[0] != "":
                split_nodes.append(TextNode(split_text[0], TextType.TEXT))
            split_nodes.append(TextNode(extracted_links[i][0], TextType.LINK, extracted_links[i][1]))
            if i == len(extracted_links) - 1:
                if split_text[1] != "":
                    split_nodes.append(TextNode(split_text[1], TextType.TEXT))
            else:
                split_text = split_text[1]
    return split_nodes

def text_to_textnodes(text):
    textnodes = [TextNode(text, TextType.TEXT)]
    textnodes = split_nodes_link(textnodes)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE)
    textnodes = split_nodes_delimiter(textnodes, "**", TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    return textnodes