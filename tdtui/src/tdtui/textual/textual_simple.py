from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import ListView, ListItem, Label, Static
from pathlib import Path
from tdtui.textual.api_processor import process_response
from tdtui.core.find_instances import main as find_instances
import logging
from typing import Optional, Dict, Any, List

from textual.widgets import Static
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer

from tdtui.textual.textual_instance_config import PortConfigScreen

logging.basicConfig(
    filename= Path.home() / "tabsdata-vm" / "log.log",
    level=logging.INFO,
    format="%(message)s"
)

class InstanceWidget(Static):
    """Rich panel showing the current working instance."""

    def __init__(self, inst: Optional[str] = None, inst_name = None):
        super().__init__()
        self.inst = inst
        self.inst_name = inst_name

    def _make_instance_panel(self) -> Panel:
        inst = self.inst or {}
        inst_name = self.inst_name
        if inst_name is not None:
            inst = [i for i in find_instances() if i["name"] == inst_name][0]


        name = inst.get("name", None)
        status = inst.get("status", None)
        cfg_ext = inst.get("cfg_ext", None)
        cfg_int = inst.get("cfg_int", None)
        arg_ext = inst.get("arg_ext", None)
        arg_int = inst.get("arg_int", None)

        if status == "Running":
            status_color = "#22c55e"
            status_line = f"{name}  ● Running"
            line1 = f"running on → ext: {arg_ext}"
            line2 = f"running on → int: {arg_int}"
        elif status is None:
            status_color = "#3522c5"
            status_line = f"○ No Instance Selected"
            line1 = f"No External Running Port"
            line2 = f"No Internal Running Port"
        else:
            status_color = "#ef4444"
            status_line = f"{name}  ○ Not running"
            line1 = f"configured on → ext: {cfg_ext}"
            line2 = f"configured on → int: {cfg_int}"

        header = Text(status_line, style=f"bold {status_color}")
        body = Text(f"{line1}\n{line2}", style="#3522c5")

        return Panel(
            Group(header, body),
            border_style=status_color,
            expand=False,
        )



    def render(self) -> RenderableType:
        # inner instance panel
        instance_panel = self._make_instance_panel()
        return instance_panel
    
class CurrentInstanceWidget(InstanceWidget):
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
        logging.info(self.app.port_selection)
        instance = self.app.port_selection.get('name')
        yield CurrentInstanceWidget(inst_name=instance)
        choiceLabels = [LabelItem(i) for i in self.choices]
        # self.list = ListView(*[LabelItem('a'), LabelItem('b')])
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


class InstanceSelectionScreen(Screen):
    def __init__(self, id=None):
        super().__init__()
        self.id = id

    def compose(self) -> ComposeResult:
        instance = find_instances()
        yield CurrentInstanceWidget(instance)
        choiceLabels = [LabelItem(i) for i in self.choices]
        # self.list = ListView(*[LabelItem('a'), LabelItem('b')])
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
        "PortConfig": PortConfigScreen
    }
    BINDINGS = [("ctrl+c", "quit", "Quit"),
                ("b", "go_back", "Go Back"),]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        self.port_selection = {
            "name": None,
            "external_port": None,
            "internal_port": None,
        }      

    def on_mount(self) -> None:
        # start with a MainMenu instance
        self.push_screen("PortConfig")

    def action_go_back(self):
        if self.screen.id != "MainScreen":
            self.pop_screen()

        


if __name__ == "__main__":
    NestedMenuApp().run()
