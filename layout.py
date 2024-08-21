from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import (ConditionalContainer,
                                               VSplit, Window,
                                               HSplit, FloatContainer, Float)
from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl
from prompt_toolkit.filters import Condition

class EditorLayout:
    def __init__(self, editor) -> None:
        self.editor = editor
        self._fc = FloatContainer(
            content=VSplit([
                LineNumbers(self.editor),
                Window(BufferControl()),
            ]),
            floats=[]
        )
        self.layout = Layout(
            container=HSplit([
                self._fc
            ])
        )


class LineNumbers(ConditionalContainer):
    def __init__(self, editor) -> None:
        super().__init__(
            Window(LineControls(editor), height=5),
            filter=Condition(lambda: True)
        )


class LineControls(FormattedTextControl):
    def __init__(self, editor):
        self.editor = editor
        self.show_line_numbers = True
    
        def get_line_numbers():
            return '\n'.join(str(i) for i in range(1, editor.buffer.document.line_count + 1))

        super().__init__(get_line_numbers, style='class:line-numbers')
