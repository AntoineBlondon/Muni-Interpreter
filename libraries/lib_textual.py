from textual import events
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static, TextArea
from textual.widget import Widget as TWidget
from textual.widgets import Label
from textual.reactive import Reactive
from textual.keys import Keys
from rich.text import Text
import uuid
import logging
import os
import sys

# Get the directory of the current script
current_dir = os.path.dirname(os.path.realpath(__file__))

# Get the parent directory path
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.append(parent_dir)
from muni_types import *


logging.basicConfig(format='%(message)s', level=logging.DEBUG)


def app_log(*args):
    logging.debug(" ".join(str(arg) for arg in args))

class RLabel(Label):
    def __init__(self, content, *args, **kwargs):
        super().__init__(str(content), *args, **kwargs)
        self.content = str(content)

    def change_content(self, new_content):
        self.content = new_content
        self.refresh()  # Add this line to refresh the widget

    def render(self):
        return Text(self.content) 


def generate_valid_id(prefix):
    """Generate a valid textual ID using UUID."""
    return str(prefix) + '-' + str(uuid.uuid4()).replace('-', '_')


def create_app(*args):
    class BasicApp(App):
        
        widgets = []
        button_text = "Yes"
        BINDINGS = [
        ]
        CSS = """
        Screen {
            align: center middle;
            width: auto;
        }
        """
        def __init__(self):
            super().__init__()
            if len(args) > 0: # if there is an argument
                self.title = str(args[0])

        actions = {}
        def compose(self) -> ComposeResult:
            """Called to add widgets to the app."""
            yield Header()
            yield Footer()
            for widget in self.widgets:
                yield widget

        def do_action(self, key):
            action_callable = self.actions[key]
            
            # If a valid callable is found, execute it
            if callable(action_callable):
                action_callable()
        
        def action_do_nothing(self, arg):
            pass

        def on_mount(self):
            # Dock all widgets in the widgets list
            for binding in self.BINDINGS:
                self.bind(keys=binding.key, action="do_nothing('" + binding.key + "')", description=binding.description)


        def on_key(self, event: events.Key):
            # check if the key is one of the bindings
            for binding in self.BINDINGS:
                if binding.key == event.key:
                    self.do_action(event.key)
                
    #app_id = id(BasicApp)  # Use the ID of the class as a unique reference
    #apps[app_id] = BasicApp()
    
    return BasicApp()

def run_app(app):
    app_instance = app
    if app_instance:
        app_instance.run()




def label_create(app_instance, text):
    text = str(text)
    if app_instance:
        text_id = generate_valid_id("txt")
        widget = RLabel(text, id=text_id)
        app_instance.widgets.append(widget)
        return text_id

def label_set_text(app_instance, label_id, text):
    text = str(text)
    label_id = str(label_id)
    if app_instance:
        for widget in app_instance.widgets:
            if widget.id == label_id:
                widget.change_content(text)


def label_get_text(app_instance, label_id):
    label_id = str(label_id)
    if app_instance:
        for widget in app_instance.widgets:
            if widget.id == label_id:
                return widget.content



def button_create(app_instance, button_text, button_variant="primary"):
    button_text = str(button_text)
    button_variant = str(button_variant)
    button_id = generate_valid_id("btn")
    if app_instance:
        button = Button(button_text, id=button_id, variant=button_variant)
        app_instance.widgets.append(button)
        return button_id


def button_set_text(app_instance, button_id, button_text):
    button_id = str(button_id)
    button_text = str(button_text)
    if app_instance:
        for widget in app_instance.widgets:
            if widget.id == button_id:
                widget.label = button_text



def button_get_text(app_instance, button_id):   
    button_id = str(button_id) 
    if app_instance:
        for widget in app_instance.widgets:
            if widget.id == button_id:
                return str(widget.label)
    


def change_variable(variable):
    variable.value = variable.value + 1

def add_binding(app_instance, key, binding_text):
    key = str(key)
    binding_text = str(binding_text)
    variable = Muni_Int(0)
    binding = Binding(key, "do_action", binding_text)
    if app_instance:
        app_instance.BINDINGS.append(binding)
        app_instance.actions[binding.key] = lambda: change_variable(variable)
    return variable
    

def exit_app(app_instance):
    if app_instance:
        app_instance.exit()