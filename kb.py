from prompt_toolkit.key_binding import KeyBindings

def create_key_bindings(editor):
    kb = KeyBindings()

    @kb.add('c-q')
    def exit_(event):
       event.app.exit()
    
    @kb.add('enter')
    def enter(event):
       event.current_buffer.insert_text('\n')

    @kb.add(':')
    def comm(event):
         editor.enter_command_mode()

    @kb.add('escape')
    def leave_comm(event):
        editor.leave_command_mode()

    return kb
