import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, extract_title, BlockType

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_empty_blocks(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list

- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list",
                "- with items",
            ],
        )

    def test_block_type_heading(self):
        block = """
# Heading one

## Heading two

### Heading three

#### Heading four

##### Heading five

###### Heading six

#a# Not an actual header

:# Not a header

######Not a header

######## Too many hashtags
"""
        blocks = markdown_to_blocks(block)
        block_types = []
        for heading in blocks:
            block_types.append(block_to_block_type(heading))
        
        self.assertListEqual(
            block_types,
            [
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ]
        )

    def test_block_type_code(self):
        block = """
```
```

```
valid as well
```

```
also valid```

```invalid
code block```

``
not valid
```

```
invalid
``
"""
        blocks = markdown_to_blocks(block)
        block_types = []
        for code_block in blocks:
            block_types.append(block_to_block_type(code_block))
        
        self.assertListEqual(
            block_types,
            [
                BlockType.CODE,
                BlockType.CODE,
                BlockType.CODE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ]
        )
    
    def test_block_type_quote(self):
        block = """
> valid quote
> another valid quote
> all of these are valid!

> this is not valid
>because of this second line
> not because of this line
"""
        blocks = markdown_to_blocks(block)
        block_types = []
        for quote_block in blocks:
            block_types.append(block_to_block_type(quote_block))
        
        self.assertListEqual(
            block_types,
            [
                BlockType.QUOTE,
                BlockType.PARAGRAPH,
            ]
        )


    def test_block_type_unord_list(self):
        block = """
- valid unordered list
- another valid unordered list
- all of these are valid!

- this is not valid
-because of this second line
- not because of this line
"""
        blocks = markdown_to_blocks(block)
        block_types = []
        for ul_block in blocks:
            block_types.append(block_to_block_type(ul_block))
        
        self.assertListEqual(
            block_types,
            [
                BlockType.UNORDERED_LIST,
                BlockType.PARAGRAPH,
            ]
        )

    def test_block_type_ord_list(self):
        block = """
1. valid unordered list
2. another valid unordered list
3. all of these
4. are valid!

1. this is not valid
2.because of this second line
3. not because of this line

1- this is also not valid
2- because we can only use period
3- no dashes allowed after the number

1. this list
3. is not ordered
2. so it fails
"""
        blocks = markdown_to_blocks(block)
        block_types = []
        for ul_block in blocks:
            block_types.append(block_to_block_type(ul_block))
        
        self.assertListEqual(
            block_types,
            [
                BlockType.ORDERED_LIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ]
        )

    def test_extract_title(self):
        block = "# Heading extracted"
        title = extract_title(block)
        self.assertEqual("Heading extracted", title)

    def test_extract_title_among_text(self):
        block = """
This text will not be extracted

`this won't either`

###   Especially this one   

#  Now this, this is going to be extracted nicely    

```
code block
```
"""
        title = extract_title(block)
        self.assertEqual("Now this, this is going to be extracted nicely", title)

if __name__ == "__main__":
    unittest.main()
