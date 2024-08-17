from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import Window, HSplit, VSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.filters import Condition
from prompt_toolkit.widgets import Frame
from prompt_toolkit.document import Document
from pygments.lexers.python import PythonLexer
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.formatted_text import FormattedText
import asyncio

kb = KeyBindings()
bg_color = '#000000'
line_numbers = '#DCDCDC'
special = '#FF0000 bold'

style = Style.from_dict({
            'window': f'{bg_color}',
            'line-numbers': f'bg:{line_numbers}',
            'special': f'{special}',  # Red and bold for special words
        })

class Editor():
    def __init__(self):
        self.app = None


    async def run(self):
        layot = self.create_layout()
        self.app = Application(
            layout=layot,
            key_bindings=kb,
            style=style,
            full_screen=True
        )
        await self.app.run_async()

    def create_layout(self):
        main_window = Window(
            content=BufferControl(
                buffer=Buffer()
            ),
            wrap_lines=True
        )
        line_numbers = Window(
            width=6,
            content=FormattedTextControl(
                [('', '1\n'), ('', '2\n')]
            ),
            style='class:line-numbers'
        )
        return Layout(
            container=HSplit([
                line_numbers,
                main_window
            ])
        )
    
    @kb.add('c-q')
    def exit_(event):
        event.app.exit()

async def main():
    editor = Editor()
    await editor.run()

if __name__ == "__main__":
    asyncio.run(main())