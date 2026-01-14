import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # HTMLNode
    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )
    
    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())

    def test_props_to_html_full(self):
        node = HTMLNode(props={"href":"https://www.google.com","target": "_blank",})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_repr_empty(self):
        node = HTMLNode()
        self.assertEqual("HTMLNode(None, None, None, None)", repr(node))

    def test_repr_full(self):
        node = HTMLNode("a", "enabled", [], {"href":"https://www.google.com","target": "_blank",})
        self.assertEqual("HTMLNode(a, enabled, [], {'href': 'https://www.google.com', 'target': '_blank'})", repr(node))

    # LeadNode
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href":"https://www.google.com","target": "_blank",})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Hello, world!</a>')

    def test_leaf_to_html_empty(self):
        node = LeafNode("", "")
        self.assertEqual(node.to_html(), "")

    def test_repr_empty(self):
        node = LeafNode("", None)
        self.assertEqual("LeafNode(, None, None)", repr(node))

    def test_repr_full(self):
        node = LeafNode("a", "enabled", {"href":"https://www.google.com","target": "_blank",})
        self.assertEqual("LeafNode(a, enabled, {'href': 'https://www.google.com', 'target': '_blank'})", repr(node))

    # ParentNode
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_mul_children(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("i", "grandchild2")
        grandchild_node3 = LeafNode("ol", "grandchild3")
        grandchild_node4 = LeafNode("blockquote", "grandchild4")
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        child_node2 = ParentNode("img", [grandchild_node3, grandchild_node4], {"src": "url/of/image.jpg", "alt": "Description of image"})
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b>grandchild1</b><i>grandchild2</i></span><img src="url/of/image.jpg" alt="Description of image"><ol>grandchild3</ol><blockquote>grandchild4</blockquote></img></div>',
        )

    def test_repr_parent_node(self):
        node = ParentNode("div", [])
        self.assertEqual(repr(node), "ParentNode(div, [], None)")

if __name__ == "__main__":
    unittest.main()