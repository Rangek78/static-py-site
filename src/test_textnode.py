import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a DIFFERENT text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_dif_type(self):
        node = TextNode("", TextType.BOLD, "google.com")
        node2 = TextNode("", TextType.TEXT, "google.com")
        self.assertNotEqual(node, node2)

    def test_dif_link(self):
        node = TextNode("", TextType.BOLD, "google.com")
        node2 = TextNode("", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr_no_link(self):
        node = TextNode("This is a text node!!!", TextType.ITALIC)
        self.assertEqual(repr(node), "TextNode(This is a text node!!!, italic, None)")

    def test_repr_with_link(self):
        node = TextNode("This is a text node!!!", TextType.ITALIC, "link.to.webpage")
        self.assertEqual(repr(node), "TextNode(This is a text node!!!, italic, link.to.webpage)")

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_link_text(self):
        node = TextNode("This is a link text node", TextType.LINK, "website.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "website.com"})

    def test_image_text(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "/url/to/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "/url/to/image.jpg", "alt": "This is an image text node"})


if __name__ == "__main__":
    unittest.main()