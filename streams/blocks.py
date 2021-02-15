
from wagtail.core import blocks

class TitleAndTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        help_text="Add your tsitle"
    )
    text = blocks.TextBlock(
        required=True,
        help_text= "Add additional text"
    )

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"


class RichTextBlock(blocks.RichTextBlock):

    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"


class SimpleRichTextBlock(blocks.RichTextBlock):

    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "italic",
            "link",
        ]
        

    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"        