from docutils import nodes
from docutils.parsers.rst import Directive

class TextBoxDirective(Directive):
    has_content = True

    def run(self):
        text_box_node = nodes.container()
        text_box_node['classes'].append('admonition')
        text_box_node['classes'].append('note')

        if self.content:
            self.state.nested_parse(self.content, self.content_offset, text_box_node)

        return [text_box_node]

def setup(app):
    app.add_directive("text-box", TextBoxDirective)
