import datetime
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from base_widgets import MenuScreen, DetailScreen
from data_manager import load_data, save_data, show_popup
from constants import (
    CLR_DBT_PRIMARY, CLR_DBT_SECOND, CLR_SAVE, CLR_ALERT_ORANGE,
    CLR_CBT_SECOND, CLR_SOOTHE_PRIMARY, CLR_HEADING
)


class DBTMenuScreen(MenuScreen):
    def on_enter(self, *args):
        self.title_label.text = 'DBT Tools'
        self.title_label.color = CLR_DBT_PRIMARY
        grid = self.menu_grid
        grid.clear_widgets()
        buttons = [
            ("Diary Card", 'dbt_diary', CLR_DBT_PRIMARY),
            ("DEAR MAN", 'dbt_dearman', CLR_DBT_SECOND),
            ("Opposite Action", 'dbt_opposite', CLR_DBT_PRIMARY),
            ("STOP Skill", 'dbt_stop', CLR_DBT_SECOND),
            ("TIPP (Crisis)", 'dbt_tipp', CLR_DBT_PRIMARY)
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


class DBTDiaryScreen(DetailScreen):
    SKILLS = [
        "Observe", "Describe", "Participate",
        "Non-Judgmentally", "One-Mindfully", "Effectively",
        "DEAR MAN", "GIVE", "FAST", "TIPP"
    ]

    def __init__(self, **kwargs):
        super().__init__(title="Diary Card", **kwargs)
        self.add_label('Check the skills you practiced today:')
        self.grid = GridLayout(cols=2, size_hint_y=None, spacing=5)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.content.add_widget(self.grid)

        # FIX: Store checkbox references explicitly instead of
        #      relying on fragile grid.children iteration
        self.checkboxes = {}
        for sk in self.SKILLS:
            lbl = Label(
                text=sk, halign='left', size_hint_x=0.7,
                color=CLR_HEADING
            )
            lbl.bind(size=lbl.setter('text_size'))
            cb = CheckBox(active=False, size_hint_x=0.3)
            self.grid.add_widget(lbl)
            self.grid.add_widget(cb)
            self.checkboxes[sk] = cb

        self.add_action_button('Save Diary', CLR_DBT_PRIMARY, self.save_diary)

    def save_diary(self):
        # FIX: Use explicit checkbox references — much more reliable
        checked = [
            skill for skill, cb in self.checkboxes.items() if cb.active
        ]
        data = load_data()
        data["diary_cards"].append({
            "time": datetime.datetime.now().isoformat(),
            "skills": checked
        })
        save_data(data)
        show_popup('Saved!', f'{len(checked)} skills logged.')
        # Reset checkboxes
        for cb in self.checkboxes.values():
            cb.active = False


class DBTDEARMANScreen(DetailScreen):
    # FIX: Complete DEAR MAN — was missing M, A, N
    def __init__(self, **kwargs):
        super().__init__(title="DEAR MAN", **kwargs)
        self.add_label('D — Describe the facts objectively')
        self.in_d = self.add_text_input(True, 60)
        self.add_label('E — Express your feelings and opinions')
        self.in_e = self.add_text_input(True, 60)
        self.add_label('A — Assert your request clearly')
        self.in_a = self.add_text_input(True, 60)
        self.add_label('R — Reinforce the positive outcome')
        self.in_r = self.add_text_input(True, 60)
        self.add_label('M — be Mindful — stay focused on your goal')
        self.in_m = self.add_text_input(True, 60)
        self.add_label('A — Appear confident — use eye contact and tone')
        self.in_a2 = self.add_text_input(True, 60)
        self.add_label('N — Negotiate — be willing to give to get')
        self.in_n = self.add_text_input(True, 60)
        self.add_action_button('Generate Script', CLR_DBT_PRIMARY,
                               self.gen_script)

    def gen_script(self):
        script = (
            f"D: {self.in_d.text}\n"
            f"E: {self.in_e.text}\n"
            f"A: {self.in_a.text}\n"
            f"R: {self.in_r.text}\n"
            f"M: {self.in_m.text}\n"
            f"A: {self.in_a2.text}\n"
            f"N: {self.in_n.text}"
        )
        show_popup('Your DEAR MAN Script', script)


class DBTOppositeScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Opposite Action", **kwargs)
        self.add_label('1. Emotion you are feeling')
        self.in_emo = self.add_text_input(True, 60)
        self.add_label('2. Urge that comes with it')
        self.in_urg = self.add_text_input(True, 60)
        self.add_label('3. Opposite Action to take')
        self.in_opp = self.add_text_input(True, 80)
        self.add_action_button('Save Plan', CLR_DBT_PRIMARY, self.save_opp)

    def save_opp(self):
        if not self.in_emo.text.strip():
            show_popup('Missing', 'Describe the emotion you are feeling.')
            return
        data = load_data()
        data["opposite_actions"].append({
            "emo": self.in_emo.text.strip(),
            "urge": self.in_urg.text.strip(),
            "opp": self.in_opp.text.strip()
        })
        save_data(data)
        show_popup('Saved!', 'Opposite action saved.')
        self.in_emo.text = ""
        self.in_urg.text = ""
        self.in_opp.text = ""


class DBTSTOPScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="STOP Skill", **kwargs)
        self.add_label('S — Stop!', color=(0.75, 0.10, 0.10, 1))
        self.add_label('Do not react. Freeze.', color=CLR_HEADING)
        self.add_label('T — Take a step back', color=CLR_ALERT_ORANGE)
        self.add_label('Pause. Breathe. Do not act on urges.',
                       color=CLR_HEADING)
        self.add_label('O — Observe', color=CLR_CBT_SECOND)
        self.add_label('Notice what is happening inside and outside.',
                       color=CLR_HEADING)
        self.add_label('P — Proceed mindfully', color=CLR_SAVE)
        self.add_label('Act with awareness. Consider your goals.',
                       color=CLR_HEADING)


class DBTTIPPScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="TIPP Crisis Skills", **kwargs)
        btns = [
            ('T — Temperature', CLR_ALERT_ORANGE,
             'Temperature',
             'Splash cold water on your face or hold ice. '
             'This activates the dive reflex to slow your heart rate.'),
            ('I — Intense Exercise', CLR_DBT_SECOND,
             'Exercise',
             'Run, jumping jacks, or push-ups for 5–10 minutes '
             'to burn off intense emotion.'),
            ('P — Paced Breathing', CLR_CBT_SECOND,
             'Breathing',
             'Exhale more slowly than you inhale. '
             'Try inhale 4 counts, exhale 6–8 counts.'),
            ('P — Muscle Relaxation', CLR_SOOTHE_PRIMARY,
             'Muscles',
             'Tense each muscle group on the inhale, '
             'then release on the exhale. Work head to toe.'),
        ]
        for text, color, title, desc in btns:
            btn = Button(
                text=text, background_color=color, color=(1, 1, 1, 1),
                size_hint_y=None, height=60,
                background_normal='', background_down=''
            )
            btn.bind(
                on_press=lambda x, t=title, d=desc: show_popup(t, d)
            )
            self.content.add_widget(btn)