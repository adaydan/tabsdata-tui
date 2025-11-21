from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import ListView, ListItem, Label, Static
from pathlib import Path
from tdtui.textual.api_processor import process_response
from tdtui.core.find_instances import main as find_instances
import logging

from textual.widgets import Static
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer

logging.basicConfig(
    filename= Path.home() / "tabsdata-vm" / "log.log",
    level=logging.INFO,
    format="%(message)s"
)

class CurrentInstanceWidget(Static):
    """Rich panel showing the current working instance."""

    def __init__(self, inst: dict):
        super().__init__()
        self.inst = inst

    def _make_instance_panel(self) -> Panel:
        inst = self.inst

        name = inst.get("name", "?")
        status = inst.get("status", "Not_Running")
        cfg_ext = inst.get("cfg_ext", "None")
        cfg_int = inst.get("cfg_int", "None")
        arg_ext = inst.get("arg_ext", "None")
        arg_int = inst.get("arg_int", "None")

        if status == "Running":
            status_color = "#22c55e"
            status_line = f"{name}  ● Running"
            line1 = f"running on → ext: {arg_ext}"
            line2 = f"running on → int: {arg_int}"
        else:
            status_color = "#ef4444"
            status_line = f"{name}  ○ Not running"
            line1 = f"configured on → ext: {cfg_ext}"
            line2 = f"configured on → int: {cfg_int}"

        header = Text(status_line, style=f"bold {status_color}")
        body = Text(f"{line1}\n{line2}", style="#e2e8f0")

        return Panel(
            Group(header, body),
            border_style=status_color,
            expand=False,
        )

    def render(self) -> RenderableType:
        # inner instance panel
        instance_panel = self._make_instance_panel()

        header = Align.center(
            Text("Current Working Instance:", style="bold #22c55e")
        )

        inner = Group(
            header,     # spacer
            Align.center(instance_panel),
        )

        outer = Panel(
            inner,
            border_style="#0f766e",
            expand=False,
        )

        # return center-aligned outer panel as the widget renderable
        return Align.center(outer)

class LabelItem(ListItem):

    def __init__(self, label: str) -> None:
        super().__init__()
        self.label = label

    def compose( self ) -> ComposeResult:
        yield Label(self.label)


class ScreenTemplate(Screen):
    def __init__(self, choices=None, id=None):
        super().__init__()
        self.choices = choices
        self.id = id

    def compose(self) -> ComposeResult:
        instance = find_instances()[0]
        yield CurrentInstanceWidget(instance)
        choiceLabels = [LabelItem(i) for i in self.choices]
        self.list = ListView(*choiceLabels)
        yield self.list
        yield Footer()
    
    def on_show(self) -> None:
        # called again when you push this screen a
        #  second time (if reused)
        self.set_focus(self.list)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item.label
        logging.info(type(self.screen).__name__)
        process_response(self, selected)   # push instance


class MainScreen(ScreenTemplate):

    def __init__(self):
        super().__init__(
            choices=[
                "Instance Management",
                "Workflow Management",
                "Asset Management",
                "Config Management",
                "Exit",
            ],
            id="MainScreen",
        )

class AnimalScreen(ScreenTemplate):
    def __init__(self):
        super().__init__(
            choices=[
                "Cat",
                "Dog"
            ],
            id="AnimalScreen",
        )

class NestedMenuApp(App):
    SCREENS = {
        "main": MainScreen,
        "animal": AnimalScreen,
    }
    BINDINGS = [("q", "quit", "Quit"),
                ("b", "go_back", "Go Back"),]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        

    def on_mount(self) -> None:
        # start with a MainMenu instance
        self.push_screen("main")

    def action_go_back(self):
        if self.screen.id != "MainScreen":
            self.pop_screen()

        


if __name__ == "__main__":
    NestedMenuApp().run()
