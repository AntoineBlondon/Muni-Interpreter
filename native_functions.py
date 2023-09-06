import os
from copy import deepcopy
from tkinter import *
from rich import print as rprint
import random
import readline
import time
import subprocess
import json

def read_json(filename):
    with open(filename) as f:
        return json.load(f)

def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def call_native_function(name, args, run_ast, symbol_table, context):
    func_info = native_functions_list.get(name)
    if func_info is None:
        raise KeyError(f"Native function {name} not found")
    
    native_context = ExecutionNativeContext(args, run_ast, symbol_table, context)
    return func_info(native_context)

def call_function(name, args, run_ast, symbol_table, context):
    func_info = context.function_table.get(name)
    if func_info is None:
        raise KeyError(f"Function {name} not found")
    
    function_context = run_ast(('function_call', name, args), context)
    return function_context

class ExecutionNativeContext:
    def __init__(self, raw_args, run_ast, symbol_table, context):
        self.raw_args = raw_args
        self.run_ast = run_ast
        self.symbol_table = symbol_table
        self.context = context

    def get_arg(self, index):
        return self.run_ast(self.raw_args[index], self.context)
    def get_args(self):
        args = []
        for arg in self.raw_args:
            args.append(self.run_ast(arg, self.context))
        return args


def native_get_terminal_size(native_context):
    rows, columns = subprocess.check_output(['stty', 'size']).decode().split()
    return [int(rows), int(columns)]



def native_print(native_context):
    rprint(" ".join(str(arg) for arg in native_context.get_args()))


def native_clear_screen(native_context):
    print("\033c", end="")

def native_printend(native_context):
    print(native_context.get_arg(0), end=native_context.get_arg(1))

def native_input(native_context):
    return input(" ".join(str(arg) for arg in native_context.get_args()))

def native_print_local(native_context):
    print(native_context.context.local_scope)

def native_print_global(native_context):
    print(native_context.symbol_table)

def native_get_files(native_context):
    directory = native_context.get_arg(0)
    try:
        filenames = os.listdir(directory)
        return filenames
    except FileNotFoundError:
        print(f"The directory {directory} was not found.")
        return []
    except PermissionError:
        print(f"You don't have permission to access {directory}.")
        return []


def native_length(native_context):
    return len(native_context.get_arg(0))

def native_sorted(native_context):
    if(len(native_context.get_args()) == 1):
        return sorted(native_context.get_arg(0))
    basic_list = native_context.get_arg(0)
    need_of_ordering = native_context.get_arg(1)

    d = {}
    for a in range(len(basic_list)):
        d[basic_list[a]] = need_of_ordering[a]

    return sorted(basic_list, key=lambda x: d[x])

def native_split(native_context):
    if(len(native_context.get_args()) == 1):
        l = []
        for c in native_context.get_arg(0):
            l.append(c)
        return l
    return native_context.get_arg(0).split(native_context.get_arg(1))

def native_strip(native_context):
    return native_context.get_arg(0).strip()

def native_mkdir(native_context):
    directory = native_context.get_arg(0)
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass

def native_rmdir(native_context):
    directory = native_context.get_arg(0)
    try:
        os.rmdir(directory)
    except FileNotFoundError:
        pass

def native_system(native_context):
    os.system(native_context.get_arg(0))

def native_contains(native_context):
    return native_context.get_arg(0) in native_context.get_arg(1)

def native_is_directory(native_context):
    return os.path.isdir(native_context.get_arg(0))
def native_write_file(native_context):
    file_path = native_context.get_arg(0)
    content = native_context.get_arg(1)

    try:
        with open(file_path, 'w') as f:
            f.write(content)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

def native_read_file(native_context):
    file_path = native_context.get_arg(0)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("")

    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return ""

def native_create_file(native_context):
    file_path = native_context.get_arg(0)
    try:
        open(file_path, 'a').close()
    except Exception as e:
        print(f"An error occurred while creating the file: {e}")

def native_file_exists(native_context):
    return os.path.exists(native_context.get_arg(0))

def native_resolve_path(native_context):
    if(isinstance(native_context, list)):
        base = native_context[0]
        relative = native_context[1]
    else:
        base = native_context.get_arg(0)
        relative = native_context.get_arg(1)

    if relative.startswith(base):
        return relative
    
    # Split the relative path into components
    components = relative.split("/")
    
    # Start with the base directory
    path = base
    
    # Process each component in the relative path
    for component in components:
        if component in [".", ""]:
            # Current directory: do nothing
            pass
        elif component == "..":
            # Parent directory: remove the last component from the path
            path = os.path.dirname(path)
        else:
            # Regular directory or file name: append it to the path
            path = os.path.join(path, component)
    
    # Return the resolved path
    return path

def native_move_file(native_context):
    source = native_context.get_arg(0)
    destination = native_context.get_arg(1)
    if(os.path.isdir(destination)):
        destination = os.path.join(destination, source.split("/")[-1])
    try:
        os.rename(source, destination)
    except FileNotFoundError:
        pass


def native_slice(native_context):
    lst = native_context.get_arg(0)
    start = native_context.get_arg(1)
    end = native_context.get_arg(2)
    return lst[start:end]

def native_replace(native_context):
    original_string = native_context.get_arg(0)
    search_string = native_context.get_arg(1)
    replace_string = native_context.get_arg(2)
    return original_string.replace(search_string, replace_string)

def native_join(native_context):
    lst = native_context.get_arg(0)
    sep = native_context.get_arg(1)
    return sep.join(lst)

def native_rm(native_context):
    file_path = native_context.get_arg(0)
    try:
        if os.path.isdir(file_path):
            os.rmdir(file_path)
        else:
            os.remove(file_path)
    except FileNotFoundError:
        pass

def get_args(native_context):
    return native_context.context.args

def native_get_ran_location(native_context):
    return native_context.context.location

def get_location(native_context):
    try:
        with open("/home/antoineblondon/perso/octaros/cache.txt", 'r') as f:
            return f.read()
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return ""

def set_location(native_context):
    with open("/home/antoineblondon/perso/octaros/cache.txt", 'w') as f:
        f.write(native_context.get_arg(0))

def copy(native_context):
    return deepcopy(native_context.get_arg(0))



windows = {}  # To keep track of created windows
entries = {}  # To keep track of created entries
texts = {}  # To keep track of created text widgets
canvases = {}  # To keep track of created canvases
widgets = {}

def native_create_window(native_context):
    window_name = native_context.get_arg(0)
    window = Tk()
    windows[window_name] = window

def native_create_label(native_context):
    window_name = native_context.get_arg(0)
    text = native_context.get_arg(1)
    window = windows.get(window_name)
    if window:
        label = Label(window, text=text)
        label.pack()

def native_mainloop(native_context):
    window_name = native_context.get_arg(0)
    window = windows.get(window_name)
    if window:
        window.mainloop()

def native_create_button(native_context):
    window_name = native_context.get_arg(0)
    text = native_context.get_arg(1)
    window = windows.get(window_name)
    if window:
        button = Button(window, text=text)
        button.pack()

def native_bind_button(native_context):
    window_name = native_context.get_arg(0)
    text = native_context.get_arg(1)
    function_name = native_context.get_arg(2)
    window = windows.get(window_name)
    if window:
        button = Button(window, text=text, command=lambda: call_function(function_name, [], native_context.run_ast, native_context.symbol_table, native_context.context))
        button.pack()


def native_create_entry(native_context):
    window_name = native_context.get_arg(0)
    entry_name = native_context.get_arg(1)
    window = windows.get(window_name)
    if window:
        entry = Entry(window)
        entry.pack()
        entries[entry_name] = entry

def native_get_entry(native_context):
    entry_name = native_context.get_arg(0)
    entry = entries.get(entry_name)
    if entry:
        return entry.get()


def native_create_text(native_context):
    window_name = native_context.get_arg(0)
    text_name = native_context.get_arg(1)
    window = windows.get(window_name)
    if window:
        text = Text(window)
        text.pack()
        texts[text_name] = text

def native_get_text(native_context):
    text_name = native_context.get_arg(0)
    text = texts.get(text_name)
    if text:
        return text.get("1.0", "end-1c")
    

def native_create_canvas(native_context):
    window_name = native_context.get_arg(0)
    canvas_name = native_context.get_arg(1)
    window = windows.get(window_name)
    if window:
        canvas = Canvas(window)
        canvas.pack()
        canvases[canvas_name] = canvas

def native_draw_rectangle(native_context):
    canvas_name = native_context.get_arg(0)
    x1, y1, x2, y2 = native_context.get_arg(1), native_context.get_arg(2), native_context.get_arg(3), native_context.get_arg(4)
    canvas = canvases.get(canvas_name)
    if canvas:
        canvas.create_rectangle(x1, y1, x2, y2)

def native_set_text(native_context):
    text_name = native_context.get_arg(0)
    new_text = native_context.get_arg(1)
    text_widget = texts.get(text_name)
    if text_widget:
        text_widget.delete("1.0", "end")  # Clear existing text
        text_widget.insert("1.0", new_text)  # Insert new text


def native_create_listbox(native_context):
    window_name = native_context.get_arg(0)
    listbox_name = native_context.get_arg(1)
    window = windows.get(window_name)
    if window:
        listbox = Listbox(window)
        listbox.pack()
        widgets[listbox_name] = listbox  # Store in widgets dictionary

def native_update_listbox(native_context):
    listbox_name = native_context.get_arg(0)
    items = native_context.get_arg(1)
    listbox = widgets.get(listbox_name)
    if listbox:
        listbox.delete(0, "end")  # Clear existing items
        for item in items:
            listbox.insert("end", item)  # Insert new item at the end

def native_bind_listbox(native_context):
    listbox_name = native_context.get_arg(0)
    event_type = native_context.get_arg(1)
    function_name = native_context.get_arg(2)
    listbox = widgets.get(listbox_name)
    if listbox:
        listbox.bind(event_type, lambda e: call_function(function_name, [], native_context.run_ast, native_context.symbol_table, native_context.context))

def native_get_selected_listbox_item(native_context):
    listbox_name = native_context.get_arg(0)
    listbox = widgets.get(listbox_name)
    if listbox:
        selected_indexes = listbox.curselection()
        if selected_indexes:
            return listbox.get(selected_indexes[0])


def native_randint(native_context):
    return random.randint(native_context.get_arg(0), native_context.get_arg(1))


command_history = []

def native_add_command_to_history(native_context):
    command_history.append(native_context.get_arg(0))
    readline.set_auto_history(command_history)

commands = []

def completer(text, state):
    full_line = readline.get_line_buffer()
    first_word = full_line.split(' ')[0]
    
    if first_word == text:
        options = [cmd + ' ' for cmd in commands if cmd.startswith(text)]
    else:
        last_word = full_line.split(' ')[-1]

        # Get the directory name from the last token
        dir_name = native_resolve_path([get_location([]), "/".join(last_word.split("/")[:-1])])


        
        # If the directory name is empty, use the current directory
        if dir_name == '':
            dir_name = get_location([])
        
        # List all files in the directory
        try:
            if(not dir_name.endswith("/")):
                dir_name += "/"
            files = os.listdir(dir_name)
        except FileNotFoundError:
            files = []
        
        # Generate a list of options (appending a '/' to directories)
        options = []
        for f in files:
            if os.path.isdir(os.path.join(dir_name, f)):
                options.append(f + '/')
            else:
                options.append(f)

        
        # Filter the options based on the last token
        options = [f for f in options if f.startswith(last_word.split("/")[-1])]


        
    
    if state < len(options):
        return options[state]
    else:
        return None

def native_add_autocomplete(native_context):
    global commands
    commands = native_context.get_arg(0)
    readline.parse_and_bind("tab: complete")

def native_update_autocomplete(native_context):
    readline.set_completer(completer)

def native_sleep(native_context):
    time.sleep(native_context.get_arg(0))


def native_store_value(native_context):
    file = native_context.get_arg(0)
    key = native_context.get_arg(1)
    value = native_context.get_arg(2)
    json_file = read_json(file)
    json_file[key] = value
    write_json(file, json_file)

def native_read_value(native_context):
    file = native_context.get_arg(0)
    key = native_context.get_arg(1)
    json_file = read_json(file)
    return json_file.get(key)
    

native_functions_list = {
    'print': native_print,
    'printlocal': native_print_local,
    'printglobal': native_print_global,
    'input': native_input,
    'get_files': native_get_files,
    'length': native_length,
    'sorted': native_sorted,
    'split': native_split,
    'strip': native_strip,
    'create_directory': native_mkdir,
    'remove_directory': native_rmdir,
    'system': native_system,
    'contains': native_contains,
    'is_directory': native_is_directory,
    'write_file': native_write_file,
    'read_file': native_read_file,
    'create_file': native_create_file,
    'slice': native_slice,
    'replace': native_replace,
    'join': native_join,
    'remove_file': native_rm,
    'get_args': get_args,
    'get_location': get_location,
    'set_location': set_location,
    'copy': copy,
    'create_window': native_create_window,
    'create_label': native_create_label,
    'mainloop': native_mainloop,
    'create_button': native_create_button,
    'bind_button': native_bind_button,
    'create_entry': native_create_entry,
    'get_entry': native_get_entry,
    'create_text': native_create_text,
    'get_text': native_get_text,
    'create_canvas': native_create_canvas,
    'draw_rectangle': native_draw_rectangle,
    'set_text': native_set_text,
    'move_file': native_move_file,
    'resolve_path': native_resolve_path,
    'randint': native_randint,
    'add_command_to_history': native_add_command_to_history,
    'add_autocomplete': native_add_autocomplete,
    'update_autocomplete': native_update_autocomplete,
    'create_listbox': native_create_listbox,
    'update_listbox': native_update_listbox,
    'bind_listbox': native_bind_listbox,
    'get_selected_listbox_item': native_get_selected_listbox_item,
    'file_exists': native_file_exists,
    'sleep': native_sleep,
    "printend": native_printend,
    "clear_screen": native_clear_screen,
    "get_terminal_size": native_get_terminal_size,
    "store_value": native_store_value,
    "read_value": native_read_value,
    "get_ran_location": native_get_ran_location,

}



def declare(func_name, function):
    native_functions_list[func_name] = function