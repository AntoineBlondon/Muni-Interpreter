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
import uuid


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



def add_button(app_instance, button_text, button_variant="primary"):
    button_id = generate_valid_id("btn")
    if app_instance:
        button = Button(button_text, id=button_id, variant=button_variant)
        app_instance.widgets.append(button)
        return button_id