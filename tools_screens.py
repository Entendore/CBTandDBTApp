import datetime
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from base_widgets import MenuScreen, DetailScreen
from data_manager import load_data, save_data, show_popup
from constants import (
    CLR_TOOLS_PRIMARY, CLR_TOOLS_SECOND, CLR_CRISIS,
    CLR_MOOD_BLUE, CLR_HEADING, CLR_BODY, CLR_SAVE
)


class ToolsMenuScreen(MenuScreen):
    def on_enter(self, *args):
        self.title_label.text = 'Tracking & Tools'
        self.title_label.color = CLR_TOOLS_PRIMARY
        grid = self.menu_grid
        grid.clear_widgets()
        buttons = [
            ("Mood Tracker", 'tools_mood', CLR_TOOLS_PRIMARY),
            ("Gratitude Log", 'tools_gratitude', CLR_TOOLS_SECOND),
            ("Daily Habits", 'tools_habits', CLR_TOOLS_PRIMARY),
            ("Safety Plan", 'tools_safety', CLR_TOOLS_SECOND),
            ("Crisis Resources", 'tools_crisis', CLR_CRISIS)
        ]
        for text, screen, color in buttons:
            btn = Button(
                text=text, font_size='18sp',
                size_hint_y=None, height=60,
                background_color=color, color=(1, 1, 1, 1),
                background_normal='', background_down=''
            )
            btn.bind(
                on_press=lambda x, s=screen: setattr(
                    self.manager, 'current', s
                )
            )
            grid.add_widget(btn)


class ToolsMoodScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Mood Tracker", **kwargs)
        self.slider = Slider(min=1, max=10, step=1, value=5)
        self.slider.bind(value=self.update_slider)
        self.content.add_widget(self.slider)

        self.mood_val = Label(
            text='5', font_size=48, color=CLR_MOOD_BLUE,
            size_hint_y=None, height=70
        )
        self.content.add_widget(self.mood_val)

        btn = Button(
            text='Log Mood', background_color=CLR_TOOLS_PRIMARY,
            color=(1, 1, 1, 1), background_normal='', background_down='',
            size_hint_y=None, height=50
        )
        btn.bind(on_press=lambda x: self.log_mood())
        self.content.add_widget(btn)

        self.mood_hist = Label(
            text='No history yet', halign='left',
            size_hint_y=None, height=120,
            color=CLR_BODY
        )
        self.mood_hist.bind(
            width=lambda *a: setattr(
                self.mood_hist, 'text_size', (self.mood_hist.width, None)
            )
        )
        self.content.add_widget(self.mood_hist)

    def on_enter(self, *args):
        """FIX: Refresh mood history when returning to this screen."""
        self.update_history()

    def update_slider(self, inst, val):
        self.mood_val.text = str(int(val))

    def log_mood(self):
        data = load_data()
        data["moods"].append({
            "time": datetime.datetime.now().isoformat(),
            "mood": int(self.slider.value)
        })
        save_data(data)
        self.update_history()
        show_popup('Logged!', 'Mood recorded.')

    def update_history(self):
        data = load_data()
        hist = data["moods"][-5:]
        if not hist:
            self.mood_hist.text = "No history yet."
            return
        txt = "-- Recent Moods --\n"
        for e in reversed(hist):
            try:
                date_part = e['time'].split('T')[0]
                time_part = e['time'].split('T')[1][:5]
                txt += f"{date_part} {time_part}: {e['mood']}/10\n"
            except (KeyError, IndexError):
                # FIX: Gracefully handle malformed entries
                txt += "— (invalid entry)\n"
        self.mood_hist.text = txt


class ToolsGratitudeScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Gratitude Log", **kwargs)
        self.add_label('1.')
        self.in_g1 = self.add_text_input(True, 60)
        self.add_label('2.')
        self.in_g2 = self.add_text_input(True, 60)
        self.add_label('3.')
        self.in_g3 = self.add_text_input(True, 60)
        self.add_action_button('Save', CLR_TOOLS_PRIMARY, self.save_grat)

    def save_grat(self):
        g1 = self.in_g1.text.strip()
        g2 = self.in_g2.text.strip()
        g3 = self.in_g3.text.strip()
        if not g1 and not g2 and not g3:
            show_popup('Empty', 'Write at least one gratitude entry.')
            return
        data = load_data()
        data["gratitude"].append({
            "date": datetime.datetime.now().isoformat(),
            "items": [g1, g2, g3]
        })
        save_data(data)
        show_popup('Saved!', 'Gratitude logged.')
        self.in_g1.text = ""
        self.in_g2.text = ""
        self.in_g3.text = ""


class ToolsHabitsScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Daily Habits", **kwargs)
        lbl = self.add_label('Daily Biological Needs')
        lbl.font_size = '22sp'

        self.grid = GridLayout(cols=2, size_hint_y=None, spacing=10)
        # FIX: Bind minimum_height so the grid expands properly in the ScrollView
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.content.add_widget(self.grid)

        self.cb_sleep = CheckBox()
        self.cb_meds = CheckBox()
        self.cb_eat = CheckBox()
        self.cb_move = CheckBox()

        habits = [
            ("Slept 7+ Hours", self.cb_sleep),
            ("Took Medication", self.cb_meds),
            ("Eaten Nutritiously", self.cb_eat),
            ("Moved Body", self.cb_move)
        ]
        for txt, cb in habits:
            lbl = Label(text=txt, halign='left', color=CLR_HEADING)
            lbl.bind(size=lbl.setter('text_size'))
            self.grid.add_widget(lbl)
            self.grid.add_widget(cb)

        self.add_action_button('Save Habits', CLR_TOOLS_PRIMARY, self.save_habits)
        self.load_habits()

    def load_habits(self):
        data = load_data()
        h = data.get("habits", {})
        self.cb_sleep.active = h.get("sleep", False)
        self.cb_meds.active = h.get("meds", False)
        self.cb_eat.active = h.get("eat", False)
        self.cb_move.active = h.get("move", False)

    def save_habits(self):
        data = load_data()
        data["habits"] = {
            "sleep": self.cb_sleep.active,
            "meds": self.cb_meds.active,
            "eat": self.cb_eat.active,
            "move": self.cb_move.active
        }
        save_data(data)
        show_popup('Saved!', 'Daily habits updated.')


class ToolsSafetyScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Safety Plan", **kwargs)
        self.add_label('Warning Signs')
        self.in_warn = self.add_text_input(True, 80)
        self.add_label('Internal Coping Strategies')
        self.in_cope = self.add_text_input(True, 80)
        self.add_label('Making Environment Safe')
        self.in_safe = self.add_text_input(True, 80)
        self.add_label('People I Can Talk To')
        self.in_people = self.add_text_input(True, 80)
        self.add_action_button('Save Plan', CLR_CRISIS, self.save_plan)
        self.load_plan()

    def load_plan(self):
        data = load_data()
        p = data.get("safety_plan", {})
        self.in_warn.text = p.get("warning", "")
        self.in_cope.text = p.get("cope", "")
        self.in_safe.text = p.get("safe", "")
        self.in_people.text = p.get("people", "")

    def save_plan(self):
        data = load_data()
        data["safety_plan"] = {
            "warning": self.in_warn.text.strip(),
            "cope": self.in_cope.text.strip(),
            "safe": self.in_safe.text.strip(),
            "people": self.in_people.text.strip()
        }
        save_data(data)
        show_popup('Saved!', 'Safety plan updated.')


class ToolsCrisisScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Crisis Resources", **kwargs)
        txt = (
            "If you are in immediate danger, "
            "call emergency services (911/999/112).\n\n"
            "USA/Canada Suicide & Crisis Lifeline:\n  Call or text 988\n\n"
            "UK Samaritans:\n  Call 116 123\n\n"
            "International:\n  findahelpline.com\n\n"
            "You are not alone. Help is available."
        )
        lbl = Label(
            text=txt, font_size=20, color=CLR_CRISIS,
            halign='center', valign='middle',
            size_hint_y=None
        )
        #      label height adjusts inside the ScrollView
        lbl.bind(
            width=lambda *a: setattr(lbl, 'text_size', (lbl.width, None)),
            texture_size=lambda *a: setattr(lbl, 'height', lbl.texture_size[1])
        )
        self.content.add_widget(lbl)