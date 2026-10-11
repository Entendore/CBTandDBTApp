from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from data_manager import load_data
from constants import CLR_TITLE, CLR_HEADING


class HomeScreen(Screen):
    """Home screen with insights summary. Built in Python for testability."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title = Label(
            text='Therapy Companion', font_size='28sp', bold=True,
            color=CLR_TITLE, size_hint_y=None, height=50
        )
        layout.add_widget(title)

        scroll = ScrollView()
        self.insights_label = Label(
            markup=True, halign='left', valign='top',
            size_hint_y=None, color=CLR_HEADING,
            padding=(10, 10)
        )
        # FIX: Proper dynamic text_size binding for markup rendering
        self.insights_label.bind(
            width=lambda *a: setattr(
                self.insights_label, 'text_size',
                (self.insights_label.width, None)
            ),
            texture_size=lambda *a: setattr(
                self.insights_label, 'height',
                self.insights_label.texture_size[1]
            )
        )
        scroll.add_widget(self.insights_label)
        layout.add_widget(scroll)

        self.add_widget(layout)

    def on_enter(self, *args):
        Clock.schedule_once(self.update_insights, 0)

    def update_insights(self, *args):
        data = load_data()
        moods = data.get("moods", [])
        avg_mood = "N/A"
        if moods:
            recent = moods[-7:]
            # FIX: Guard against missing 'mood' key
            valid = [m['mood'] for m in recent if 'mood' in m]
            if valid:
                avg_mood = f"{sum(valid) / len(valid):.1f}"

        thoughts = len(data.get("thoughts", []))
        gratitudes = len(data.get("gratitude", []))

        self.insights_label.text = (
            "[size=26][b][color=131130]Welcome Back[/color][/b][/size]\n\n"
            "[color=4A4858]Average Mood (Last 7):[/color] "
            f"[b][color=1A5A9E]{avg_mood}[/color][/b]\n"
            "[color=4A4858]Thought Records:[/color] "
            f"[b][color=1A5A9E]{thoughts}[/color][/b]\n"
            "[color=4A4858]Gratitude Entries:[/color] "
            f"[b][color=1A5A9E]{gratitudes}[/color][/b]\n\n"
            "[size=18][i][color=6A6878]"
            "Take it one step at a time.[/color][/i][/size]"
        )