from ui.screens.dashboard import Dashboard

from textual.app import App
from textual.widgets import DataTable, Static
from textual.binding import Binding

class TradingApp(App):
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", priority=True)
    ]

    CSS_PATH = "layout.tcss"
    
    def on_mount(self):
        self.push_screen(Dashboard())