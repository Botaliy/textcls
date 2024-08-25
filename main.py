import os
from turtle import width
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

SPECIAL_WORDS = [
    "FROM",
    "SELECT",
    "WHERE",
    "AND",
    "OR",
    "ORDER",
    "BY",
    "GROUP",
    "HAVING",
]


class SpecialWordsLexer(Lexer):
    def lex_document(self, document):
        def get_line(lineno):
            line = document.lines[lineno]
            formatted_line = []
            for word in line.split():
                if word.upper() in SPECIAL_WORDS:
                    formatted_line.append(("class:special", word))
                    formatted_line.append(("", " "))
                else:
                    formatted_line.append(("", word + " "))
            return FormattedText(formatted_line)

        return get_line


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
    def __init__(
        self,
        background_color="#000000",
        text_color="#ffffff",
        highlight_color="#4CAF50",
    ):
        self.filename = None
        self.words = set()
        self.completer = SmartCompleter(self.words)
        self.background_color = background_color
        self.text_color = text_color
        self.highlight_color = highlight_color

        self.buffer = Buffer(completer=self.completer, complete_while_typing=True)
        self.buffer.on_text_changed += self.on_text_changed

        self.main_window = Window(
            content=BufferControl(
                buffer=self.buffer,
                lexer=SpecialWordsLexer(),
            ),
            get_line_prefix=self.process_prefix,
            wrap_lines=True,
        )

        self.body = VSplit([self.main_window])

        self.layout = Layout(self.body)

        self.kb = KeyBindings()

        @self.kb.add("c-s")
        def save_file(event):
            if self.filename:
                with open(self.filename, "w") as f:
                    f.write(self.buffer.text)
            else:
                self.filename = input("Enter filename to save: ")
                with open(self.filename, "w") as f:
                    f.write(self.buffer.text)

        @self.kb.add("c-q")
        def exit_editor(event):
            event.app.exit()

        @self.kb.add("c-space")
        def update_completer(event):
            self.update_completer()

        @self.kb.add("enter")
        def handle_enter(event):
            event.current_buffer.insert_text("\n")
            self.update_line_numbers()

        self.style = Style.from_dict(
            {
                "window": f"bg:{self.background_color} {self.text_color}",
                "line-numbers": f"bg:{self.background_color} #888888",
                "current-line": f"bg:{self.highlight_color}",
                "special": "#FF0000 bold",  # Red and bold for special words
            }
        )

        self.app = Application(
            layout=self.layout,
            key_bindings=self.kb,
            full_screen=True,
            style=self.style,
            mouse_support=True,
        )

    def run(self):
        self.app.run()

    def update_completer(self):
        new_words = set(
            word.strip() for word in self.buffer.text.split() if len(word.strip()) > 1
        )
        self.words.update(new_words)
        self.completer = SmartCompleter(self.words)
        self.buffer.completer = self.completer

    def update_line_numbers(self):
        self.app.invalidate()

    def on_text_changed(self, buffer):
        self.update_line_numbers()

    def process_prefix(self, lineno, width):
        return f"{lineno+1:>4} "


if __name__ == "__main__":
    editor = TextEditor(
        background_color="#2C3E50", text_color="#ECF0F1", highlight_color="#4CAF50"
    )
    editor.run()
