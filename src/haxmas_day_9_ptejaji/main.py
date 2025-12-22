from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Label
from textual.screen import Screen
from textual.containers import Grid, Vertical, Center
import datetime

class DayScreen(Screen):
    """Screen for a day of the advent calendar!"""

    CSS = """
    DayScreen {
        align: center middle;
    }
    
    #dialog {
        width: 50;
        height: auto;
        border: thick #ff8c00;
        background: #2d1a00;
        padding: 2;
        align: center middle;
    }
    
    #dialog Label {
        width: 100%;
        text-align: center;
        margin-bottom: 1;
    }
    
    #dialog Button {
        width: auto;
    }
    """

    gifts = {
        1: "A single sock (matches coming soon™)",
        2: "Python Book (written in Morse code)",
        3: "Coffee Mug (half empty, like my soul)",
        4: "USB-C Cable (the one that only works one way)",
        5: "Wireless Mouse (batteries not included)",
        6: "Notebook (filled with someone else's doodles)",
        7: "Desk Lamp (flickers ominously)",
        8: "Keyboard Switches (your cat's favorite toy)",
        9: "Monitor Stand (wobbles mysteriously)",
        10: "Mechanical Keyboard (wake the neighborhood!)",
        11: "Gaming Headset (one ear works, maybe)",
        12: "A day with me! (refundable)"
    }


    def __init__(self, day: int) -> None:
        self.day = day
        super().__init__()
    
    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label(f"Here's what's in day {str(self.day)}: {self.gifts.get(self.day)}")
            with Center():
                yield Button("Close", id="close")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()
        event.stop()

class AdventCalendarApp(App):
    """A Textual app for an advent calendar."""
    
    CSS = """
    Grid {
        grid-size: 4 3;
        grid-gutter: 1 2;
    }
    
    Grid Button {
        width: 100%;
        height: 100%;
    }
    
    Grid Button:hover {
        background: #ff8c00;
    }
    
    Grid Button.opened {
        background: #ff6600;
    }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("r", "reset_days", "Reset all days")
    ]
    
    START_DATE = datetime.date(2025, 12, 13)

    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Label("Days completed: 0/12", id="counter")
        with Grid():
            for day in range(1, 13):
                yield Button(str(day), id=f"day-{day}")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        button = event.button
        day = str(button.label)
        unlock_day = self.START_DATE + datetime.timedelta(days=int(day) - 1)
        
        if datetime.date.today() < unlock_day:
            self.notify(f"You will be able to unlock day {day} on {unlock_day}")
            return None
        
        if not button.has_class("opened"):
            button.add_class("opened")
            self.update_counter()
        self.push_screen(DayScreen(int(day)))
    
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
    
    def update_counter(self) -> None:
        """Update the counter label with the number of opened days."""
        opened_count = sum(1 for button in self.query(Button) if button.has_class("opened"))
        counter = self.query_one(Label)
        counter.update(f"Days completed: {opened_count}/12")
    
    def action_reset_days(self) -> None:
        """Reset all days to unopened state."""
        for button in self.query(Button):
            button.remove_class("opened")
        self.update_counter()
        self.notify("All days have been reset!")

def main():
    app = AdventCalendarApp()
    app.run()
    
if __name__ == "__main__":
    main()
