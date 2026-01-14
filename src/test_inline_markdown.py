import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestTextNodeSplitNodes(unittest.TestCase):
    def test_split_inline(self):
        node = TextNode("This text has some `inline code`, _some italic_ and **some bold** in it", TextType.TEXT)
        split = split_nodes_delimiter([node], "`", TextType.CODE)
        split = split_nodes_delimiter(split, "**", TextType.BOLD)
        split = split_nodes_delimiter(split, "_", TextType.ITALIC)
        
        self.assertEqual([
            TextNode("This text has some ", TextType.TEXT, None),
            TextNode("inline code", TextType.CODE, None),
            TextNode(", ", TextType.TEXT, None),
            TextNode("some italic", TextType.ITALIC, None),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("some bold", TextType.BOLD, None),
            TextNode(" in it", TextType.TEXT, None),
        ],
        split)

    def test_split_empty_separator_and_wrong_delimitor(self):
        node = TextNode("This text has nothing special to it", TextType.TEXT)
        split = split_nodes_delimiter([node], "    ", TextType.TEXT)
        split1 = split_nodes_delimiter([node], "*", TextType.TEXT)
        self.assertEqual([
            TextNode("This text has nothing special to it", TextType.TEXT, None),
        ],
        split)
        self.assertEqual([
            TextNode("This text has nothing special to it", TextType.TEXT, None),
        ],
        split1)

    def test_invalid_syntax(self):
        node = TextNode("This text has ****invalid***** syntax**", TextType.TEXT)
        with self.assertRaises(ValueError) as e:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(e.exception), "invalid markdown syntax")

    def test_mul_nodes(self):
        node = TextNode("This text has some `inline code` in it", TextType.TEXT)
        node2 = TextNode("This text has some **bold string** and `inline code` in it", TextType.TEXT)
        node3 = TextNode("This text is completely bold", TextType.BOLD)
        split = split_nodes_delimiter([node, node2, node3], "`", TextType.CODE)
        split = split_nodes_delimiter(split, "**", TextType.BOLD)
        self.assertEqual([
            TextNode("This text has some ", TextType.TEXT, None),
            TextNode("inline code", TextType.CODE, None),
            TextNode(" in it", TextType.TEXT, None),
            TextNode("This text has some ", TextType.TEXT, None),
            TextNode("bold string", TextType.BOLD, None),
            TextNode(" and ", TextType.TEXT),
            TextNode("inline code", TextType.CODE, None),
            TextNode(" in it", TextType.TEXT, None),
            TextNode("This text is completely bold", TextType.BOLD, None)
        ],
        split)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with one ![image](https://i.imgur.com/zjjcJKZ.png), two ![image](https://i.imgur.com/zjjcJKZ.png) and three ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://youtube.com)"
        )
        self.assertListEqual([("link", "https://youtube.com")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with one [link](https://youtube.com), two [link](https://youtube.com) and three [link](https://youtube.com)"
        )
        self.assertListEqual([("link", "https://youtube.com"), ("link", "https://youtube.com"), ("link", "https://youtube.com")], matches)

    def test_extract_link_and_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and also a [link](https://youtube.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and also a [link](https://youtube.com)"
        )
        self.assertListEqual([("link", "https://youtube.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), a [link](https://youtube.com) and [another link](https://youtube.com.br)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(", a [link](https://youtube.com) and [another link](https://youtube.com.br)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://youtube.com) and another [second link](https://youtube.com.br)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://youtube.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://youtube.com.br"
                ),
            ],
            new_nodes,
        )

    def test_split_images_and_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://youtube.com"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes,
                             [
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
        
    def test_text_to_textnode_nested(self):
        text = "This is **text** with an _italic and some `code`_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        with self.assertRaises(ValueError) as e:
            text_to_textnodes(text)
        self.assertEqual(str(e.exception), "invalid markdown syntax")
    
    def test_text_to_textnode_link(self):
        text = "This is a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes,
                             [
                                TextNode("This is a ", TextType.TEXT),
                                TextNode("link", TextType.LINK, "https://boot.dev"),
                            ])
if __name__ == "__main__":
    unittest.main()