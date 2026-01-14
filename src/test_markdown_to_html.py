import unittest

from block_markdown import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> Testing a poorly formatted     
>     block quote made in markdown    
>    for testing purposes. To `test` it.       
>
>
>
> This should be valid
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>Testing a poorly formatted</p><p>block quote made in markdown</p><p>for testing purposes. To <code>test</code> it.</p><p>This should be valid</p></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
-  Testing a poorly formatted     
-     unordered list made in markdown    
-    that's got some **bold text** in it    
-    for testing purposes. To test it.       
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li> Testing a poorly formatted     </li><li>    unordered list made in markdown    </li><li>   that's got some <b>bold text</b> in it    </li><li>   for testing purposes. To test it.</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1.  Testing a poorly formatted     
2.     ORDERED list made in markdown    
3.    that's got some _italic text_ in it    
4.    for testing purposes. To test it.       
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li> Testing a poorly formatted     </li><li>    ORDERED list made in markdown    </li><li>   that's got some <i>italic text</i> in it    </li><li>   for testing purposes. To test it.</li></ol></div>",
        )

    def test_heading(self):
        md = """
#    Heading 1

##    Heading 2

### Heading 3   

#### Heading 4   

with some paragraph

######    Jumping to heading 6    

# Back to heading 1

####### this has to be a paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>   Heading 1</h1><h2>   Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><p>with some paragraph</p><h6>   Jumping to heading 6</h6><h1>Back to heading 1</h1><p>####### this has to be a paragraph</p></div>",
        )

if __name__ == "__main__":
    unittest.main()
