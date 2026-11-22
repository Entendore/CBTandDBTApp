import json
import os
import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder

# ═══════════════════════════════════════════════════════════════
# COLOR PALETTE — High contrast, cohesive design system
# ═══════════════════════════════════════════════════════════════

# -- Backgrounds --
CLR_APP_BG       = (0.97, 0.96, 0.94, 1)   # Warm off-white

# -- Navigation Bar --
CLR_NAV_BG       = (0.13, 0.11, 0.21, 1)   # Deep indigo
CLR_NAV_TEXT     = (0.92, 0.91, 0.96, 1)   # Soft white

# -- Typography --
CLR_TITLE        = (0.13, 0.11, 0.21, 1)   # Deep indigo
CLR_HEADING      = (0.22, 0.20, 0.30, 1)   # Dark slate
CLR_BODY         = (0.30, 0.28, 0.36, 1)   # Medium slate
CLR_LIGHT_TEXT   = (0.55, 0.53, 0.60, 1)   # Light slate
CLR_WHITE        = (1.0, 1.0, 1.0, 1)       # Pure white

# -- CBT Section — Ocean Blue --
CLR_CBT_PRIMARY  = (0.11, 0.35, 0.60, 1)   # Deep blue
CLR_CBT_SECOND   = (0.18, 0.50, 0.78, 1)   # Medium blue
CLR_CBT_LIGHT    = (0.30, 0.62, 0.88, 1)   # Light blue
CLR_CBT_BG       = (0.91, 0.94, 0.98, 1)   # Pale blue tint

# -- DBT Section — Rich Plum --
CLR_DBT_PRIMARY  = (0.44, 0.16, 0.48, 1)   # Deep plum
CLR_DBT_SECOND   = (0.56, 0.28, 0.60, 1)   # Medium plum
CLR_DBT_LIGHT    = (0.68, 0.42, 0.72, 1)   # Light plum
CLR_DBT_BG       = (0.95, 0.91, 0.96, 1)   # Pale plum tint

# -- Soothe Section — Forest Teal --
CLR_SOOTHE_PRIMARY  = (0.08, 0.44, 0.40, 1) # Deep teal
CLR_SOOTHE_SECOND   = (0.14, 0.58, 0.52, 1) # Medium teal
CLR_SOOTHE_LIGHT    = (0.22, 0.70, 0.62, 1) # Light teal
CLR_SOOTHE_BG       = (0.91, 0.96, 0.95, 1) # Pale teal tint

# -- Tools Section — Warm Amber --
CLR_TOOLS_PRIMARY  = (0.68, 0.44, 0.08, 1)  # Deep amber
CLR_TOOLS_SECOND   = (0.80, 0.56, 0.14, 1)  # Medium amber
CLR_TOOLS_LIGHT    = (0.90, 0.68, 0.24, 1)  # Light amber
CLR_TOOLS_BG       = (0.98, 0.95, 0.90, 1)  # Pale amber tint

# -- Actions --
CLR_SAVE         = (0.10, 0.50, 0.28, 1)   # Confident green
CLR_BACK         = (0.68, 0.12, 0.12, 1)   # Clear red
CLR_CRISIS       = (0.75, 0.10, 0.10, 1)   # Alert red
CLR_ALERT_ORANGE = (0.85, 0.45, 0.10, 1)   # Warning orange

# -- Specialty --
CLR_MOOD_BLUE    = (0.18, 0.40, 0.62, 1)   # Calm blue for mood
CLR_BREATHE_IN   = (0.18, 0.50, 0.78, 1)   # Inhale blue
CLR_BREATHE_HOLD = (0.80, 0.68, 0.10, 1)   # Hold gold
CLR_BREATHE_OUT  = (0.10, 0.50, 0.28, 1)   # Exhale green
CLR_MINDFUL      = (0.10, 0.48, 0.42, 1)   # Mindful teal

Window.clearcolor = CLR_APP_BG

# ═══════════════════════════════════════════════════════════════
# KV STRING — Core navigation and HomeScreen
# ═══════════════════════════════════════════════════════════════

KV = '''
<NavButton@Button>:
    font_size: '14sp'
    background_color: (0.20, 0.18, 0.32, 1)
    color: (0.92, 0.91, 0.96, 1)
    border: (0, 0, 0, 0)
    background_normal: ''
    background_down: ''
    canvas.before:
        Color:
            rgba: (0.25, 0.22, 0.38, 1) if self.state == 'normal' else (0.35, 0.32, 0.52, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<RootWidget>:
    orientation: 'vertical'
    ScreenManager:
        id: sm
        HomeScreen:
            name: 'home'
        CBTMenuScreen:
            name: 'cbt_menu'
        DBTMenuScreen:
            name: 'dbt_menu'
        SootheMenuScreen:
            name: 'soothe_menu'
        ToolsMenuScreen:
            name: 'tools_menu'
        CBTThoughtScreen:
            name: 'cbt_thought'
        CBTActivityScreen:
            name: 'cbt_activity'
        CBTCopingScreen:
            name: 'cbt_coping'
        CBTValuesScreen:
            name: 'cbt_values'
        DBTDiaryScreen:
            name: 'dbt_diary'
        DBTDEARMANScreen:
            name: 'dbt_dearman'
        DBTOppositeScreen:
            name: 'dbt_opposite'
        DBTSTOPScreen:
            name: 'dbt_stop'
        DBTTIPPScreen:
            name: 'dbt_tipp'
        SootheGroundScreen:
            name: 'soothe_ground'
        SootheSensesScreen:
            name: 'soothe_senses'
        SootheBreatheScreen:
            name: 'soothe_breathe'
        SootheMindfulScreen:
            name: 'soothe_mindful'
        ToolsMoodScreen:
            name: 'tools_mood'
        ToolsGratitudeScreen:
            name: 'tools_gratitude'
        ToolsHabitsScreen:
            name: 'tools_habits'
        ToolsSafetyScreen:
            name: 'tools_safety'
        ToolsCrisisScreen:
            name: 'tools_crisis'

    BoxLayout:
        size_hint_y: 0.07
        spacing: 2
        padding: [2, 2, 2, 2]
        canvas.before:
            Color:
                rgba: (0.10, 0.08, 0.18, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        NavButton:
            text: 'Home'
            on_press: root.go_to('home')
        NavButton:
            text: 'CBT'
            on_press: root.go_to('cbt_menu')
        NavButton:
            text: 'DBT'
            on_press: root.go_to('dbt_menu')
        NavButton:
            text: 'Soothe'
            on_press: root.go_to('soothe_menu')
        NavButton:
            text: 'Tools'
            on_press: root.go_to('tools_menu')

<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 24
        spacing: 16
        Label:
            text: 'MindTools Pro'
            font_size: 38
            size_hint_y: 0.18
            color: (0.13, 0.11, 0.21, 1)
            bold: True
        ScrollView:
            Label:
                id: insights
                text: 'Loading...'
                markup: True
                font_size: '18sp'
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1]
                halign: 'center'
                valign: 'top'

<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        Label:
            id: title_label
            font_size: 28
            size_hint_y: 0.10
            bold: True
            color: (0.13, 0.11, 0.21, 1)
        ScrollView:
            GridLayout:
                id: menu_grid
                cols: 1
                spacing: 12
                size_hint_y: None
                height: self.minimum_height
'''

Builder.load_string(KV)

# --- Data Management ---
DATA_FILE = "therapy_data_final.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    return {
        "moods": [], "thoughts": [], "activities": [], "diary_cards": [],
        "gratitude": [], "coping_cards": ["I can handle this.", "This feeling is temporary."],
        "opposite_actions": [], "safety_plan": {}, "habits": {"sleep": False, "meds": False, "eat": False, "move": False},
        "values": [], "senses": []
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def show_popup(title, text):
    popup = Popup(
        title=title,
        title_color=CLR_WHITE,
        title_font='Roboto',
        title_size='18sp',
        separator_color=CLR_CBT_SECOND,
        content=Label(text=text, text_size=(Window.width*0.7, None), halign='center', color=CLR_HEADING),
        size_hint=(0.85, 0.45),
        background_color=(0.97, 0.96, 0.94, 1)
    )
    popup.open()

# --- Base Classes ---
class RootWidget(BoxLayout):
    def go_to(self, screen_name):
        self.ids.sm.current = screen_name

class MenuScreen(Screen):
    pass

class DetailScreen(Screen):
    def __init__(self, title="", **kwargs):
        super().__init__(**kwargs)
        self.root_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Top bar
        top_bar = BoxLayout(size_hint_y=0.08, spacing=10)
        back_btn = Button(text='< Back', size_hint_x=0.3,
                          background_color=CLR_BACK, color=CLR_WHITE,
                          background_normal='', background_down='')
        back_btn.bind(on_press=lambda x: self.go_back())
        title_lbl = Label(text=title, font_size=22, bold=True,
                          halign='left', valign='middle', color=CLR_TITLE)
        title_lbl.bind(size=title_lbl.setter('text_size'))
        top_bar.add_widget(back_btn)
        top_bar.add_widget(title_lbl)

        # Content
        self.scroll = ScrollView(size_hint_y=0.82)
        self.content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=12)
        self.content.bind(minimum_height=self.content.setter('height'))
        self.scroll.add_widget(self.content)

        # Action bar
        self.action_bar = BoxLayout(size_hint_y=0.1, spacing=10)

        self.root_layout.add_widget(top_bar)
        self.root_layout.add_widget(self.scroll)
        self.root_layout.add_widget(self.action_bar)
        self.add_widget(self.root_layout)

    def go_back(self):
        name = self.name
        if name.startswith('cbt'): self.manager.current = 'cbt_menu'
        elif name.startswith('dbt'): self.manager.current = 'dbt_menu'
        elif name.startswith('soothe'): self.manager.current = 'soothe_menu'
        elif name.startswith('tools'): self.manager.current = 'tools_menu'

    def add_label(self, text, color=None):
        lbl = Label(text=text, halign='left', size_hint_y=None, height=25,
                    font_size='16sp', color=color or CLR_BODY)
        lbl.bind(size=lbl.setter('text_size'))
        self.content.add_widget(lbl)
        return lbl

    def add_text_input(self, multiline=False, height=60, hint=''):
        ti = TextInput(multiline=multiline, size_hint_y=None, height=height,
                       hint_text=hint,
                       foreground_color=CLR_HEADING,
                       hint_text_color=CLR_LIGHT_TEXT,
                       background_color=(0.92, 0.91, 0.89, 1))
        self.content.add_widget(ti)
        return ti

    def add_spinner(self, values):
        sp = Spinner(text='Select', values=values, size_hint_y=None, height=44,
                     color=CLR_HEADING, background_color=(0.92, 0.91, 0.89, 1))
        self.content.add_widget(sp)
        return sp

    def add_action_button(self, text, color, callback):
        btn = Button(text=text, background_color=color, color=CLR_WHITE,
                     background_normal='', background_down='',
                     font_size='16sp', bold=True)
        btn.bind(on_press=lambda x: callback())
        self.action_bar.add_widget(btn)

# --- Screens ---

# HOME
class HomeScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.update_insights, 0)

    def update_insights(self, *args):
        data = load_data()
        moods = data.get("moods", [])
        avg_mood = "N/A"
        if moods:
            avg_mood = f"{sum(m['mood'] for m in moods[-7:]) / len(moods[-7:]):.1f}"

        thoughts = len(data.get("thoughts", []))
        gratitudes = len(data.get("gratitude", []))

        if 'insights' in self.ids:
            self.ids.insights.text = (
                f"[size=26][b][color=131130]Welcome Back[/color][/b][/size]\n\n"
                f"[color=4A4858]Average Mood (Last 7):[/color] [b][color=1A5A9E]{avg_mood}[/color][/b]\n"
                f"[color=4A4858]Thought Records:[/color] [b][color=1A5A9E]{thoughts}[/color][/b]\n"
                f"[color=4A4858]Gratitude Entries:[/color] [b][color=1A5A9E]{gratitudes}[/color][/b]\n\n"
                f"[size=18][i][color=6A6878]Take it one step at a time.[/color][/i][/size]"
            )

# CBT — Ocean Blue theme
class CBTMenuScreen(MenuScreen):
    def on_enter(self, *args):
        self.ids.title_label.text = 'CBT Tools'
        self.ids.title_label.color = CLR_CBT_PRIMARY
        grid = self.ids.menu_grid
        grid.clear_widgets()
        buttons = [
            ("Thought Record", 'cbt_thought', CLR_CBT_PRIMARY),
            ("Behavioral Activation", 'cbt_activity', CLR_CBT_SECOND),
            ("Coping Cards", 'cbt_coping', CLR_CBT_PRIMARY),
            ("Values Clarification", 'cbt_values', CLR_CBT_SECOND)
        ]
        for text, screen, color in buttons:
            btn = Button(text=text, font_size='18sp', size_hint_y=None, height=60,
                         background_color=color, color=CLR_WHITE,
                         background_normal='', background_down='')
            btn.bind(on_press=lambda x, s=screen: setattr(self.manager, 'current', s))
            grid.add_widget(btn)

class CBTThoughtScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Thought Record", **kwargs)
        self.add_label('Situation')
        self.in_sit = self.add_text_input(True, 80)
        self.add_label('Automatic Thought')
        self.in_tho = self.add_text_input(True, 80)
        self.add_label('Cognitive Distortion')
        self.spin = self.add_spinner(['All-or-Nothing', 'Catastrophizing', 'Mind Reading', 'Overgeneralization', 'Emotional Reasoning', 'Personalization'])
        self.add_label('Rational Thought')
        self.in_rat = self.add_text_input(True, 80)
        self.add_action_button('Save', CLR_SAVE, self.save_thought)

    def save_thought(self):
        data = load_data()
        rec = {"situation": self.in_sit.text, "thought": self.in_tho.text, "distortion": self.spin.text, "rational": self.in_rat.text}
        if not rec["situation"] or not rec["thought"]:
            show_popup('Missing Info', 'Fill out Situation and Thought.'); return
        data["thoughts"].append(rec); save_data(data); show_popup('Saved!', 'Thought record saved.')
        self.in_sit.text = ""; self.in_tho.text = ""; self.spin.text = 'Select'; self.in_rat.text = ""

class CBTActivityScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Behavioral Activation", **kwargs)
        self.add_label('Activity Description')
        self.in_act = self.add_text_input(True, 80)
        self.add_label('Mastery (1-10)')
        self.in_mast = self.add_text_input(False, 44); self.in_mast.input_filter = 'int'
        self.add_label('Pleasure (1-10)')
        self.in_pleas = self.add_text_input(False, 44); self.in_pleas.input_filter = 'int'
        self.add_action_button('Save', CLR_SAVE, self.save_act)

    def save_act(self):
        try: m, p = int(self.in_mast.text), int(self.in_pleas.text)
        except: show_popup('Error', 'Mastery/Pleasure must be numbers.'); return
        data = load_data(); data["activities"].append({"act": self.in_act.text, "mastery": m, "pleasure": p})
        save_data(data); show_popup('Saved!', 'Activity logged.')
        self.in_act.text = ""; self.in_mast.text = ""; self.in_pleas.text = ""

class CBTCopingScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Coping Cards", **kwargs)
        self.idx = 0
        self.lbl_card = Label(text='No cards', font_size=26, size_hint_y=0.3,
                              text_size=(Window.width*0.8, None), color=CLR_CBT_PRIMARY)
        self.content.add_widget(self.lbl_card)

        nav = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_prev = Button(text='< Prev', background_color=CLR_CBT_PRIMARY,
                          color=CLR_WHITE, background_normal='', background_down='')
        btn_prev.bind(on_press=lambda x: self.next_card(-1))
        btn_next = Button(text='Next >', background_color=CLR_CBT_PRIMARY,
                          color=CLR_WHITE, background_normal='', background_down='')
        btn_next.bind(on_press=lambda x: self.next_card(1))
        nav.add_widget(btn_prev); nav.add_widget(btn_next)
        self.content.add_widget(nav)

        self.add_label('New Coping Statement')
        self.in_new = self.add_text_input(False, 44)
        self.add_action_button('Add Card', CLR_CBT_SECOND, self.add_card)

        self._show_initial_card()

    def _show_initial_card(self):
        data = load_data()
        cards = data.get("coping_cards", [])
        if cards:
            self.lbl_card.text = cards[0]

    def next_card(self, dir):
        data = load_data(); cards = data["coping_cards"]
        if not cards: return
        self.idx = (self.idx + dir) % len(cards); self.lbl_card.text = cards[self.idx]

    def add_card(self):
        text = self.in_new.text.strip()
        if text:
            data = load_data(); data["coping_cards"].append(text); save_data(data)
            self.idx = len(data["coping_cards"]) - 1; self.in_new.text = ""; self.lbl_card.text = text

class CBTValuesScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Values Clarification", **kwargs)
        self.add_label('Core Value (e.g., Honesty, Family)')
        self.in_val = self.add_text_input(False, 44)
        self.add_label('Intention/Action for today')
        self.in_act = self.add_text_input(True, 80)
        self.add_action_button('Save', CLR_SAVE, self.save_val)

    def save_val(self):
        val = self.in_val.text.strip()
        if val:
            data = load_data(); data["values"].append({"value": val, "action": self.in_act.text}); save_data(data)
            show_popup('Saved!', 'Value saved.'); self.in_val.text = ""; self.in_act.text = ""

# DBT — Rich Plum theme
class DBTMenuScreen(MenuScreen):
    def on_enter(self, *args):
        self.ids.title_label.text = 'DBT Tools'
        self.ids.title_label.color = CLR_DBT_PRIMARY
        grid = self.ids.menu_grid; grid.clear_widgets()
        buttons = [
            ("Diary Card", 'dbt_diary', CLR_DBT_PRIMARY),
            ("DEAR MAN", 'dbt_dearman', CLR_DBT_SECOND),
            ("Opposite Action", 'dbt_opposite', CLR_DBT_PRIMARY),
            ("STOP Skill", 'dbt_stop', CLR_DBT_SECOND),
            ("TIPP (Crisis)", 'dbt_tipp', CLR_DBT_PRIMARY)
        ]
        for text, screen, color in buttons:
            btn = Button(text=text, font_size='18sp', size_hint_y=None, height=60,
                         background_color=color, color=CLR_WHITE,
                         background_normal='', background_down='')
            btn.bind(on_press=lambda x, s=screen: setattr(self.manager, 'current', s))
            grid.add_widget(btn)

class DBTDiaryScreen(DetailScreen):
    SKILLS = ["Observe", "Describe", "Participate", "Non-Judgmentally", "One-Mindfully", "Effectively", "DEAR MAN", "GIVE", "FAST", "TIPP"]
    def __init__(self, **kwargs):
        super().__init__(title="Diary Card", **kwargs)
        self.add_label('Check the skills you practiced today:')
        self.grid = GridLayout(cols=2, size_hint_y=None, spacing=5)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.content.add_widget(self.grid)
        for sk in self.SKILLS:
            lbl = Label(text=sk, halign='left', size_hint_x=0.7, color=CLR_HEADING)
            lbl.bind(size=lbl.setter('text_size'))
            cb = CheckBox(active=False, size_hint_x=0.3)
            self.grid.add_widget(lbl); self.grid.add_widget(cb)
        self.add_action_button('Save Diary', CLR_DBT_PRIMARY, self.save_diary)

    def save_diary(self):
        data = load_data(); checked = []; ch = self.grid.children[::-1]
        for i in range(0, len(ch), 2):
            if ch[i+1].active: checked.append(ch[i].text)
        data["diary_cards"].append({"time": datetime.datetime.now().isoformat(), "skills": checked})
        save_data(data); show_popup('Saved!', f'{len(checked)} skills logged.')

class DBTDEARMANScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="DEAR MAN", **kwargs)
        self.add_label('D - Describe facts'); self.in_d = self.add_text_input(True, 60)
        self.add_label('E - Express feelings'); self.in_e = self.add_text_input(True, 60)
        self.add_label('A - Assert request'); self.in_a = self.add_text_input(True, 60)
        self.add_label('R - Reinforce outcome'); self.in_r = self.add_text_input(True, 60)
        self.add_action_button('Generate Script', CLR_DBT_PRIMARY, self.gen_script)

    def gen_script(self):
        show_popup('Script', f"D: {self.in_d.text}\nE: {self.in_e.text}\nA: {self.in_a.text}\nR: {self.in_r.text}")

class DBTOppositeScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Opposite Action", **kwargs)
        self.add_label('1. Emotion you are feeling'); self.in_emo = self.add_text_input(True, 60)
        self.add_label('2. Urge that comes with it'); self.in_urg = self.add_text_input(True, 60)
        self.add_label('3. Opposite Action to take'); self.in_opp = self.add_text_input(True, 80)
        self.add_action_button('Save Plan', CLR_DBT_PRIMARY, self.save_opp)

    def save_opp(self):
        data = load_data(); data["opposite_actions"].append({"emo": self.in_emo.text, "opp": self.in_opp.text})
        save_data(data); show_popup('Saved!', 'Opposite action saved.')

class DBTSTOPScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="STOP Skill", **kwargs)
        lbl1 = self.add_label('S - Stop!', color=(0.75, 0.10, 0.10, 1))
        self.add_label('Do not react. Freeze.', color=CLR_HEADING)
        lbl2 = self.add_label('T - Take a step back', color=CLR_ALERT_ORANGE)
        self.add_label('Pause. Breathe. Do not act on urges.', color=CLR_HEADING)
        lbl3 = self.add_label('O - Observe', color=CLR_CBT_SECOND)
        self.add_label('Notice what is happening inside and outside.', color=CLR_HEADING)
        lbl4 = self.add_label('P - Proceed mindfully', color=CLR_SAVE)
        self.add_label('Act with awareness. Consider your goals.', color=CLR_HEADING)

class DBTTIPPScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="TIPP Crisis Skills", **kwargs)
        btns = [
            ('T - Temperature', CLR_ALERT_ORANGE, 'Temperature', 'Splash cold water or hold ice.'),
            ('I - Intense Exercise', CLR_DBT_SECOND, 'Exercise', 'Run, jumping jacks, push-ups 5-10m.'),
            ('P - Paced Breathing', CLR_CBT_SECOND, 'Breathing', 'Exhale slower than inhale.'),
            ('P - Muscle Relaxation', CLR_SOOTHE_PRIMARY, 'Muscles', 'Tense on inhale, release on exhale.')
        ]
        for text, color, title, desc in btns:
            btn = Button(text=text, background_color=color, color=CLR_WHITE,
                         size_hint_y=None, height=60,
                         background_normal='', background_down='')
            btn.bind(on_press=lambda x, t=title, d=desc: show_popup(t, d))
            self.content.add_widget(btn)

# SOOTHE — Forest Teal theme
class SootheMenuScreen(MenuScreen):
    def on_enter(self, *args):
        self.ids.title_label.text = 'Soothe & Ground'
        self.ids.title_label.color = CLR_SOOTHE_PRIMARY
        grid = self.ids.menu_grid; grid.clear_widgets()
        buttons = [
            ("5-4-3-2-1 Grounding", 'soothe_ground', CLR_SOOTHE_PRIMARY),
            ("Self-Soothe (5 Senses)", 'soothe_senses', CLR_SOOTHE_SECOND),
            ("Box Breathing", 'soothe_breathe', CLR_SOOTHE_PRIMARY),
            ("Mindfulness Timer", 'soothe_mindful', CLR_SOOTHE_SECOND)
        ]
        for text, screen, color in buttons:
            btn = Button(text=text, font_size='18sp', size_hint_y=None, height=60,
                         background_color=color, color=CLR_WHITE,
                         background_normal='', background_down='')
            btn.bind(on_press=lambda x, s=screen: setattr(self.manager, 'current', s))
            grid.add_widget(btn)

class SootheGroundScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="5-4-3-2-1 Grounding", **kwargs)
        self.add_label('5 Things You Can SEE'); self.in_see = self.add_text_input(True, 60)
        self.add_label('4 Things You Can TOUCH'); self.in_tou = self.add_text_input(True, 60)
        self.add_label('3 Things You Can HEAR'); self.in_hear = self.add_text_input(True, 60)
        self.add_label('2 Things You Can SMELL'); self.in_sme = self.add_text_input(True, 60)
        self.add_label('1 Thing You Can TASTE'); self.in_tas = self.add_text_input(True, 60)

class SootheSensesScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Self-Soothe (Senses)", **kwargs)
        self.add_label('Vision (What is beautiful?)'); self.in_v = self.add_text_input(True, 60)
        self.add_label('Hearing (Calming sounds?)'); self.in_h = self.add_text_input(True, 60)
        self.add_label('Smell (Favorite scents?)'); self.in_s = self.add_text_input(True, 60)
        self.add_label('Taste (Comforting food?)'); self.in_t = self.add_text_input(True, 60)
        self.add_label('Touch (Soft, warm?)'); self.in_o = self.add_text_input(True, 60)
        self.add_action_button('Save Plan', CLR_SOOTHE_PRIMARY, self.save_senses)

    def save_senses(self):
        data = load_data(); data["senses"].append({"v": self.in_v.text, "h": self.in_h.text, "s": self.in_s.text, "t": self.in_t.text, "o": self.in_o.text})
        save_data(data); show_popup('Saved!', 'Sensory plan saved.')

class SootheBreatheScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Box Breathing", **kwargs)
        self.lbl_breath = Label(text='Press Start', font_size=60, color=CLR_CBT_SECOND)
        self.content.add_widget(self.lbl_breath)
        self.lbl_btime = Label(text='0', font_size=40, color=CLR_HEADING)
        self.content.add_widget(self.lbl_btime)
        self.btn_bstart = Button(text='Start', background_color=CLR_SOOTHE_PRIMARY,
                                 color=CLR_WHITE, background_normal='', background_down='')
        self.btn_bstart.bind(on_press=lambda x: self.toggle_breath())
        self.action_bar.add_widget(self.btn_bstart)
        self.is_running = False; self.breath_event = None; self.step_index = 0; self.counter = 0
        self.steps = [
            ("Inhale",  4, CLR_BREATHE_IN),
            ("Hold",    4, CLR_BREATHE_HOLD),
            ("Exhale",  4, CLR_BREATHE_OUT),
            ("Hold",    4, CLR_BREATHE_HOLD)
        ]

    def on_leave(self, *args): self.stop_breath()

    def toggle_breath(self):
        if self.is_running: self.stop_breath()
        else: self.start_breath()

    def start_breath(self):
        self.is_running = True; self.btn_bstart.text = 'Stop'; self.step_index = 0; self.counter = 0
        self.update_breath_ui(); self.breath_event = Clock.schedule_interval(self.breath_tick, 1)

    def stop_breath(self):
        self.is_running = False; self.btn_bstart.text = 'Start'
        if self.breath_event: self.breath_event.cancel()
        self.lbl_breath.text = 'Press Start'; self.lbl_breath.color = CLR_CBT_SECOND; self.lbl_btime.text = '0'

    def breath_tick(self, dt):
        self.counter += 1; step_name, step_dur, step_color = self.steps[self.step_index]
        if self.counter >= step_dur: self.counter = 0; self.step_index = (self.step_index + 1) % len(self.steps); self.update_breath_ui()
        else: self.lbl_btime.text = str(step_dur - self.counter)

    def update_breath_ui(self):
        step_name, step_dur, step_color = self.steps[self.step_index]
        self.lbl_breath.text = step_name; self.lbl_breath.color = step_color; self.lbl_btime.text = str(step_dur)

class SootheMindfulScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Mindfulness Timer", **kwargs)
        self.lbl_mtime = Label(text='00:00', font_size=72, color=CLR_MINDFUL)
        self.content.add_widget(self.lbl_mtime)
        time_grid = BoxLayout(size_hint_y=None, height=60, spacing=10)
        for m in [1, 5, 10]:
            btn = Button(text=f'{m} Min', background_color=CLR_SOOTHE_SECOND,
                         color=CLR_WHITE, background_normal='', background_down='')
            btn.bind(on_press=lambda x, mins=m: self.set_time(mins*60))
            time_grid.add_widget(btn)
        self.content.add_widget(time_grid)
        self.btn_mstart = Button(text='Start', background_color=CLR_SOOTHE_PRIMARY,
                                 color=CLR_WHITE, background_normal='', background_down='')
        self.btn_mstart.bind(on_press=lambda x: self.toggle_mindful())
        self.action_bar.add_widget(self.btn_mstart)
        self.is_running = False; self.timer_event = None; self.time_left = 0

    def on_leave(self, *args): self.stop_mindful()

    def set_time(self, sec):
        if not self.is_running: self.time_left = sec; self.update_mindful_ui()

    def toggle_mindful(self):
        if self.is_running: self.stop_mindful()
        else: self.start_mindful()

    def start_mindful(self):
        if self.time_left <= 0: self.set_time(60)
        self.is_running = True; self.btn_mstart.text = 'Pause'; self.timer_event = Clock.schedule_interval(self.mindful_tick, 1)

    def stop_mindful(self):
        self.is_running = False; self.btn_mstart.text = 'Resume'
        if self.timer_event: self.timer_event.cancel()

    def mindful_tick(self, dt):
        if self.time_left <= 0:
            self.stop_mindful(); self.btn_mstart.text = 'Start'; self.time_left = 0
            self.update_mindful_ui(); show_popup('Session Complete', 'Great job staying mindful.'); return
        self.time_left -= 1; self.update_mindful_ui()

    def update_mindful_ui(self):
        mins, secs = divmod(self.time_left, 60); self.lbl_mtime.text = f"{mins:02d}:{secs:02d}"

# TOOLS — Warm Amber theme
class ToolsMenuScreen(MenuScreen):
    def on_enter(self, *args):
        self.ids.title_label.text = 'Tracking & Tools'
        self.ids.title_label.color = CLR_TOOLS_PRIMARY
        grid = self.ids.menu_grid; grid.clear_widgets()
        buttons = [
            ("Mood Tracker", 'tools_mood', CLR_TOOLS_PRIMARY),
            ("Gratitude Log", 'tools_gratitude', CLR_TOOLS_SECOND),
            ("Daily Habits", 'tools_habits', CLR_TOOLS_PRIMARY),
            ("Safety Plan", 'tools_safety', CLR_TOOLS_SECOND),
            ("Crisis Resources", 'tools_crisis', CLR_CRISIS)
        ]
        for text, screen, color in buttons:
            btn = Button(text=text, font_size='18sp', size_hint_y=None, height=60,
                         background_color=color, color=CLR_WHITE,
                         background_normal='', background_down='')
            btn.bind(on_press=lambda x, s=screen: setattr(self.manager, 'current', s))
            grid.add_widget(btn)

class ToolsMoodScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Mood Tracker", **kwargs)
        self.slider = Slider(min=1, max=10, step=1, value=5)
        self.slider.bind(value=self.update_slider)
        self.content.add_widget(self.slider)
        self.mood_val = Label(text='5', font_size=48, color=CLR_MOOD_BLUE)
        self.content.add_widget(self.mood_val)
        btn = Button(text='Log Mood', background_color=CLR_TOOLS_PRIMARY,
                     color=CLR_WHITE, background_normal='', background_down='')
        btn.bind(on_press=lambda x: self.log_mood())
        self.content.add_widget(btn)
        self.mood_hist = Label(text='No history', halign='left', size_hint_y=None,
                               height=100, color=CLR_BODY)
        self.mood_hist.bind(size=self.mood_hist.setter('text_size'))
        self.content.add_widget(self.mood_hist)

    def update_slider(self, inst, val): self.mood_val.text = str(int(val))

    def log_mood(self):
        data = load_data(); data["moods"].append({"time": datetime.datetime.now().isoformat(), "mood": int(self.slider.value)})
        save_data(data); self.update_history(); show_popup('Logged!', 'Mood recorded.')

    def update_history(self):
        data = load_data(); hist = data["moods"][-5:]
        if not hist: self.mood_hist.text = "No history yet."; return
        txt = "-- Recent Moods --\n"
        for e in reversed(hist):
            t = e['time'].split('T')[0] + " " + e['time'].split('T')[1][:5]; txt += f"{t}: {e['mood']}/10\n"
        self.mood_hist.text = txt

class ToolsGratitudeScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Gratitude Log", **kwargs)
        self.add_label('1.'); self.in_g1 = self.add_text_input(True, 60)
        self.add_label('2.'); self.in_g2 = self.add_text_input(True, 60)
        self.add_label('3.'); self.in_g3 = self.add_text_input(True, 60)
        self.add_action_button('Save', CLR_TOOLS_PRIMARY, self.save_grat)

    def save_grat(self):
        g1, g2, g3 = self.in_g1.text.strip(), self.in_g2.text.strip(), self.in_g3.text.strip()
        if not g1 and not g2 and not g3: return
        data = load_data(); data["gratitude"].append({"date": datetime.datetime.now().isoformat(), "items": [g1, g2, g3]})
        save_data(data); show_popup('Saved!', 'Gratitude logged.'); self.in_g1.text = ""; self.in_g2.text = ""; self.in_g3.text = ""

class ToolsHabitsScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Daily Habits", **kwargs)
        lbl = self.add_label('Daily Biological Needs'); lbl.font_size = '22sp'
        self.grid = GridLayout(cols=2, size_hint_y=None, height=150, spacing=10)
        self.content.add_widget(self.grid)
        self.cb_sleep = CheckBox(); self.cb_meds = CheckBox()
        self.cb_eat = CheckBox(); self.cb_move = CheckBox()
        for txt, cb in [("Slept 7+ Hours", self.cb_sleep), ("Took Medication", self.cb_meds),
                        ("Eaten Nutritiously", self.cb_eat), ("Moved Body", self.cb_move)]:
            lbl = Label(text=txt, halign='left', color=CLR_HEADING)
            lbl.bind(size=lbl.setter('text_size'))
            self.grid.add_widget(lbl); self.grid.add_widget(cb)
        self.add_action_button('Save Habits', CLR_TOOLS_PRIMARY, self.save_habits)
        self.load_habits()

    def load_habits(self):
        data = load_data(); h = data.get("habits", {})
        self.cb_sleep.active = h.get("sleep", False); self.cb_meds.active = h.get("meds", False)
        self.cb_eat.active = h.get("eat", False); self.cb_move.active = h.get("move", False)

    def save_habits(self):
        data = load_data()
        data["habits"] = {"sleep": self.cb_sleep.active, "meds": self.cb_meds.active, "eat": self.cb_eat.active, "move": self.cb_move.active}
        save_data(data); show_popup('Saved!', 'Daily habits updated.')

class ToolsSafetyScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Safety Plan", **kwargs)
        self.add_label('Warning Signs'); self.in_warn = self.add_text_input(True, 80)
        self.add_label('Internal Coping Strategies'); self.in_cope = self.add_text_input(True, 80)
        self.add_label('Making Environment Safe'); self.in_safe = self.add_text_input(True, 80)
        self.add_action_button('Save Plan', CLR_CRISIS, self.save_plan)
        self.load_plan()

    def load_plan(self):
        data = load_data(); p = data.get("safety_plan", {})
        self.in_warn.text = p.get("warning", ""); self.in_cope.text = p.get("cope", "")
        self.in_safe.text = p.get("safe", "")

    def save_plan(self):
        data = load_data()
        data["safety_plan"] = {"warning": self.in_warn.text, "cope": self.in_cope.text, "safe": self.in_safe.text}
        save_data(data); show_popup('Saved!', 'Safety plan updated.')

class ToolsCrisisScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Crisis Resources", **kwargs)
        txt = "If you are in immediate danger, call emergency services.\n\nUSA/Canada: Call or text 988\nUK: Call 116 123\nInternational: findahelpline.com\n\nYou are not alone."
        lbl = Label(text=txt, font_size=20, color=CLR_CRISIS)
        lbl.bind(size=lbl.setter('text_size'))
        self.content.add_widget(lbl)

# --- App Main ---
class TherapyApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    TherapyApp().run()