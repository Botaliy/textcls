from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import Window, HSplit, VSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.layout.containers import WindowAlign
from prompt_toolkit.filters import Condition
from prompt_toolkit.widgets import Frame
from prompt_toolkit.document import Document
from pygments.lexers.python import PythonLexer
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.formatted_text import FormattedText
import asyncio
from lexer import SqlLexer
from kb import create_key_bindings
from prompt_toolkit.enums import EditingMode
from layout import EditorLayout


background_color="#2C3E50"
text_color="#ECF0F1"
highlight_color="#96aeff"
line_numbers = '#dbbfbf'
special = '#FF0000 bold'

style = Style.from_dict({
            'window': f'bg:{background_color} {text_color}',
            'line-numbers': f'bg:{background_color} #000000',
            'current-line': f'bg:{highlight_color}',
            'sql-keyword': f'{special}',  # Red and bold for special words
        })

class Editor():
    def __init__(self):
        self.buffer = Buffer()
        self.line_buffer = Buffer()
        self.editor_layout = EditorLayout(self)
        self.key_bindings = create_key_bindings(self)
        self.app = self._create_app()

    async def run(self):
        await self.app.run_async()
    
    def get_line_numbers(self):
        lines = self.buffer.document.lines
        current_line = self.buffer.document.cursor_position_row
        result = []
        for i, line in enumerate(lines):
            if i == current_line:
                result.append(('class:current-line', f'{i+1:>2} \n'))
            else:
                result.append(('', f'{i+1:>2} \n'))
        result.append(('', '\n' * (len(lines) - len(result))))
        return result

    def _create_app(self):
        application = Application(
            editing_mode=EditingMode.EMACS,
            layout=self.editor_layout.layout,
            key_bindings=self.key_bindings,
            style=style,
            full_screen=True,
        )
        return application
        


async def main():
    editor = Editor()
    await editor.run()

if __name__ == "__main__":
    asyncio.run(main())
