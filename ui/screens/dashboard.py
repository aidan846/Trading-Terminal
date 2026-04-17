from core.positions import *

from textual import work
from textual.screen import Screen
from textual.app import ComposeResult
from textual.events import MouseMove
from textual.widgets import Static, DataTable, Sparkline
from textual.containers import Vertical, Horizontal
from textual_plot import HiResMode, PlotWidget
from textual_plotext import PlotextPlot, plotext

BALANCE_HISTORY_X = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]
BALANCE_HISTORY_Y = [10, 12, 11, 15, 14, 18, 17, 20, 19, 22, 21, 25, 24, 28, 27, 30, 29, 32, 31, 35, 34, 38, 37, 40, 39, 42, 41, 45, 44, 48, 47, 50, 49, 52, 51, 55, 54, 58, 57, 60, 59, 62, 61, 65, 64, 68, 67, 70, 69, 72]

y= [10, 12, 11, 15, 14, 18, 17, 20, 19, 22, 21, 25, 24, 28, 27, 30, 29, 32, 31, 35, 34, 38, 37, 40, 39, 42, 41, 45, 44, 48, 47, 50, 49, 52, 51, 55, 54, 58, 57, 60, 59, 62, 61, 65, 64, 68, 67, 70, 69, 72]

def setup_watchlist_table(table: DataTable):
    table.add_columns("Ticker", "Price", "Change")
    table.add_rows([
        ("AAPL", "$150.00", "+1.2%"),
        ("TSLA", "$700.00", "-0.5%"),
        ("BTC", "$45,000", "+3.0%"),
        ("ETH", "$3,200", "+2.1%"),
    ])
    table.expand = True
    table.cursor_type = "row"
    table.zebra_stripes = False

def setup_position_table(table: DataTable):
    table.add_columns("Ticker", "Quantity", "Avg Price", "Current Price", "Daily P/L", "Open P/L", "News")
    table.add_rows([
        ("AAPL", "100", "$145.00", "$150.00", "+$500", "+$1000", "Apple reports strong earnings"),
        ("TSLA", "50", "$720.00", "$700.00", "-$962", "+$2,523", "Tesla announces new factory opening"),
        ("BTC", "0.5", "$40,000", "$45,000", "+$2,500", "+$5,000", "Bitcoin reaches new all-time high"),
        ("ETH", "2", "$3,000", "$3,200", "+$400", "+$800", "Ethereum upgrades network infrastructure"),
        ("MSFT", "150", "$250.00", "$255.00", "+$750", "+$750", "Microsoft acquires gaming company"),
        ("AMZN", "20", "$3,000.00", "$3,100.00", "+$2,000", "+$2,000", "Amazon announces new Prime benefits"),
        ("GOOGL", "30", "$2,500.00", "$2,550.00", "+$1,500", "+$1,500", "Google unveils new AI features"),
        ("META", "80", "$350.00", "$360.00", "+$800", "+$800", "Facebook rebrands to Meta"),
        ("NVDA", "60", "$500.00", "$550.00", "+$3,000", "+$3,000", "NVIDIA releases new GPU architecture"),
    ])
    table.expand = True
    table.cursor_type = "row"
    table.zebra_stripes = False

class Dashboard(Screen):
    
    CSS_PATH = "dashboard.tcss"

    def compose(self):
        yield DataTable(id="static1") 
        with Horizontal(id="static2"):
            with Vertical(id="metrics-column"):
                yield Static("$52,000", classes="metric", id="balance")
                yield Static("Cash: $10,450", classes="metric")
                yield Static("Open P/L: +$1,200", classes="metric", id="profit")
                yield Static("Day's P/L: -$150", classes="metric", id="loss")

            with Vertical(id="chart-column"):
                yield PlotextPlot(id="balance-chart")
        yield DataTable(id="static3")
    
    def on_mount(self):
        self.theme = "nord"

        setup_watchlist_table(self.query_one("#static1", DataTable))

        setup_position_table(self.query_one("#static3", DataTable))

        plot_widget = self.query_one("#balance-chart", PlotextPlot)
        plt = plot_widget.plt
        
        plt.clear_data()
        # Use .plot() instead of .scatter() to connect the points
        plt.plot(BALANCE_HISTORY_X, BALANCE_HISTORY_Y, color="green")
        plt.title("Account Balance Trend")
        
        plot_widget.refresh()

        self.set_interval(1.0, self.refresh_portfolio_data)
    
    def on_mouse_move(self, event: MouseMove) -> None:
        """Called when the mouse moves over the screen."""
        # Check if the mouse is over the chart
        plot = self.query_one("#balance-chart", PlotextPlot)
        
        if plot.region.contains(event.screen_x, event.screen_y):
            # This is a simplified way to show 'Hover' logic in Textual.
            # Real coordinate mapping from pixels to Plotext data is complex,
            # so usually, we display the "Last Value" or update a label.
            self.title = f"Current Hover Position: {event.x}, {event.y}"
        else:
            self.title = "Trading Terminal"
    
    @work(thread=True)
    def refresh_portfolio_data(self) -> None:
        """Background worker to fetch data and update the UI."""
        # 1. Run your logic to get new prices from yfinance and save to JSON
        # update_positions() 
        
        # 2. Read the updated JSON
        portfolio_data = get_portfolio_data() 
        
        # 3. Update the UI safely using call_from_thread
        self.app.call_from_thread(self.update_table_rows, portfolio_data)

    def update_table_rows(self, data) -> None:
        """Update the DataTable with the new data."""
        table = self.query_one("#static3", DataTable)
        table.clear()  # Clear existing rows
        
        new_rows = []
        for pos in data["positions"]:
            new_rows.append((
                pos["ticker"], 
                str(pos["shares"]), 
                f"${pos['avg_price']:.2f}", 
                f"${pos['current_price']:.2f}", 
                f"${pos['daily_pl']:.2f}", 
                f"${pos['open_pl']:.2f}",
                "No news" # Or your news field
            ))
        
        table.add_rows(new_rows)