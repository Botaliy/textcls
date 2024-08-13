import os
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import Completer, Completion
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

        self.window = Window(
            content=BufferControl(
                buffer=self.buffer,
                lexer=PygmentsLexer(PythonLexer)
            )
        )

        self.layout = Layout(self.window)

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
        })
        self.app.style = self.style

if __name__ == "__main__":
    editor = TextEditor(background_color="#2C3E50", text_color="#ECF0F1")
    editor.run()