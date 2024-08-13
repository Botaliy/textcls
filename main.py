import os
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import Window, HSplit, VSplit, ConditionalContainer
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

class SmartCompleter(Completer):
    def __init__(self, words):
        self.words = words

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        if word:
            for w in self.words:
                if w.startswith(word):
                    yield Completion(w, start_position=-len(word))

class TextEditor:
    def __init__(self, background_color="#000000", text_color="#ffffff"):
        self.filename = None
        self.words = set()
        self.completer = SmartCompleter(self.words)
        self.background_color = background_color
        self.text_color = text_color
        
        self.buffer = Buffer(completer=self.completer,
                             complete_while_typing=True)
        self.main_window = Window(
            content=BufferControl(
                buffer=self.buffer,
                lexer=PygmentsLexer(PythonLexer)
            )
        )

        self.line_numbers = FormattedTextControl(self.get_line_numbers)
        line_numbers_window = Window(content=self.line_numbers, width=6)

        self.completion_window = ConditionalContainer(
            Window(
                content=FormattedTextControl(self.get_completion_text),
                width=30,
                height=5,
            ),
            filter=Condition(lambda: self.buffer.complete_state is not None)
        )

        self.body = VSplit([
            line_numbers_window,
            HSplit([
                self.main_window,
                self.completion_window
            ])
        ])

        self.layout = Layout(self.body)

        self.kb = KeyBindings()

        @self.kb.add('c-s')
        def save_file(event):
            if self.filename:
                with open(self.filename, 'w') as f:
                    f.write(self.buffer.text)
            else:
                self.filename = input("Enter filename to save: ")
                with open(self.filename, 'w') as f:
                    f.write(self.buffer.text)

        @self.kb.add('c-q')
        def exit_editor(event):
            event.app.exit()

        @self.kb.add('c-space')
        def update_completer(event):
            self.update_completer()

        self.style = Style.from_dict({
            'window': f'bg:{self.background_color} {self.text_color}',
            'line-numbers': '#888888',
            'completion-menu': 'bg:#444444 #ffffff',
        })

        self.app = Application(
            layout=self.layout,
            key_bindings=self.kb,
            full_screen=True,
            style=self.style
        )

    def run(self):
        self.app.run()

    def update_completer(self):
        new_words = set(word.strip() for word in self.buffer.text.split() if len(word.strip()) > 1)
        self.words.update(new_words)
        self.completer = SmartCompleter(self.words)
        self.buffer.completer = self.completer

    def change_background_color(self, new_color):
        self.background_color = new_color
        self.update_style()

    def change_text_color(self, new_color):
        self.text_color = new_color
        self.update_style()

    def update_style(self):
        self.style = Style.from_dict({
            'window': f'bg:{self.background_color} {self.text_color}',
            'line-numbers': '#888888',
            'completion-menu': 'bg:#444444 #ffffff',
        })
        self.app.style = self.style

    def get_line_numbers(self):
        lines = self.buffer.document.lines
        line_numbers = []
        for i in range(len(lines)):
            if i == self.buffer.document.cursor_position_row:
                line_numbers.append(('class:line-numbers,current-line', f'{i+1:4d} '))
            else:
                line_numbers.append(('class:line-numbers', f'{i+1:4d} '))
        return line_numbers

    def get_completion_text(self):
        if self.buffer.complete_state:
            completions = self.buffer.complete_state.completions
            return [('class:completion-menu', f' {c.text}\n') for c in completions[:5]]
        return []

if __name__ == "__main__":
    editor = TextEditor(background_color="#2C3E50", text_color="#ECF0F1")
    editor.run()