from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable, List

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Vertical, Horizontal, VerticalScroll, Container
from textual.widgets import Label, Footer, Static, Button
from textual.widgets import RichLog  # ← Correct widget

from tdtui.textual.spinners import SpinnerWidget
import logging
from pathlib import Path
import asyncio.subprocess
import random
from tdtui.core.yaml_getter_setter import set_yaml_value
from time import sleep
from tdtui.core.find_instances import main as find_instances


# Configure file logging
logging.basicConfig(
    filename=Path(__file__).resolve().parent / "log.log",
    level=logging.INFO,
    format="%(message)s",
)


class DemoApp(App):
    BINDINGS = [("ctrl+c", "quit", "Quit")]

    def on_mount(self):
        self.push_screen(TaskScreen())


if __name__ == "__main__":
    DemoApp().run()
