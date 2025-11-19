from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import ListView, ListItem, Label
from pathlib import Path
import logging

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Button
from textual.containers import Grid, Vertical, Horizontal

logging.basicConfig(
    filename= Path.home() / "tabsdata-vm" / "log.log",
    level=logging.INFO,
    format="%(message)s"
)

class QuitScreen(Footer):
    """Screen with a dialog to quit."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Button("back", variant="default", id="back"),
            Button("quit", variant="error", id="quit"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()


class LabelItem(ListItem):

    def __init__(self, label: str) -> None:
        super().__init__()
        self.label = label

    def compose( self ) -> ComposeResult:
        yield Label(self.label)



class MainMenu(Screen):

    def compose(self) -> ComposeResult:

        with Vertical():
            # Main content area
            yield Label("Main Menu")
            yield ListView(
                LabelItem("Fruits"),
                LabelItem("Animals"),
            )

            # Bottom "footer" section with 2 buttons in a grid 
        with Horizontal(id="dialog"):
            yield Button("Back", variant="default", id="back")
            yield Button("Quit", variant="error", id="quit")


    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item.label
        logging.info(selected)
        if selected == "Fruits":
            self.app.push_screen(FruitMenu())    # push instance
        elif selected == "Animals":
            self.app.push_screen(AnimalMenu())   # push instance
    def on_key(self, event) -> None:
    # Intercept DOWN when we're on the last list item and move to footer
        if event.key == "down":
            menu = self.query_one("#menu", ListView)
            if self.focused is menu and menu.index == len(menu.children) - 1:
                footer = self.query_one("#footer", FooterBar)
                footer.focus_button(0)  # first footer button
                event.stop()
                return
        super().on_key(event)

class FruitMenu(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Choose a fruit")
        yield ListView(
            LabelItem("Apple"),
            LabelItem("Banana"),
            LabelItem("Back"),
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        val = event.item
        if val == "Back":
            self.app.pop_screen()
        else:
            print(f"You picked: {val}")
            self.app.pop_screen()


class AnimalMenu(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Choose an animal")
        yield ListView(
            LabelItem("Cat"),
            LabelItem("Dog"),
            LabelItem("Back"),
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        val = event.item
        if val == "Back":
            self.app.pop_screen()
        else:
            print(f"You picked: {val}")
            self.app.pop_screen()


class NestedMenuApp(App):
    BINDINGS = [("q", "quit", "Quit")]

    def on_mount(self) -> None:
        # start with a MainMenu instance
        self.push_screen(MainMenu())

        


if __name__ == "__main__":
    NestedMenuApp().run()
