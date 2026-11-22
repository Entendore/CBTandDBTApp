from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from base_widgets import MenuScreen, DetailScreen
from data_manager import load_data, save_data, show_popup
from constants import (
    CLR_SOOTHE_PRIMARY, CLR_SOOTHE_SECOND, CLR_CBT_SECOND, CLR_HEADING,
    CLR_BREATHE_IN, CLR_BREATHE_HOLD, CLR_BREATHE_OUT, CLR_MINDFUL
)


class SootheMenuScreen(MenuScreen):
    def on_enter(self, *args):
        self.title_label.text = 'Soothe & Ground'
        self.title_label.color = CLR_SOOTHE_PRIMARY
        grid = self.menu_grid
        grid.clear_widgets()
        buttons = [
            ("5-4-3-2-1 Grounding", 'soothe_ground', CLR_SOOTHE_PRIMARY),
            ("Self-Soothe (5 Senses)", 'soothe_senses', CLR_SOOTHE_SECOND),
            ("Box Breathing", 'soothe_breathe', CLR_SOOTHE_PRIMARY),
            ("Mindfulness Timer", 'soothe_mindful', CLR_SOOTHE_SECOND)
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


class SootheGroundScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="5-4-3-2-1 Grounding", **kwargs)
        self.add_label('5 Things You Can SEE')
        self.in_see = self.add_text_input(True, 60)
        self.add_label('4 Things You Can TOUCH')
        self.in_tou = self.add_text_input(True, 60)
        self.add_label('3 Things You Can HEAR')
        self.in_hear = self.add_text_input(True, 60)
        self.add_label('2 Things You Can SMELL')
        self.in_sme = self.add_text_input(True, 60)
        self.add_label('1 Thing You Can TASTE')
        self.in_tas = self.add_text_input(True, 60)
        self.add_action_button('Save Entry', CLR_SOOTHE_PRIMARY,
                               self.save_ground)

    def save_ground(self):
        """FIX: Actually persist grounding entries so they aren't lost."""
        entry = {
            "see": self.in_see.text.strip(),
            "touch": self.in_tou.text.strip(),
            "hear": self.in_hear.text.strip(),
            "smell": self.in_sme.text.strip(),
            "taste": self.in_tas.text.strip()
        }
        if not any(entry.values()):
            show_popup('Empty', 'Fill in at least one sense.')
            return
        data = load_data()
        # Store in a dedicated key; add to defaults if missing
        data.setdefault("grounding", []).append(entry)
        save_data(data)
        show_popup('Saved!', 'Grounding exercise recorded.')
        self.in_see.text = ""
        self.in_tou.text = ""
        self.in_hear.text = ""
        self.in_sme.text = ""
        self.in_tas.text = ""


class SootheSensesScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Self-Soothe (Senses)", **kwargs)
        self.add_label('Vision (What is beautiful?)')
        self.in_v = self.add_text_input(True, 60)
        self.add_label('Hearing (Calming sounds?)')
        self.in_h = self.add_text_input(True, 60)
        self.add_label('Smell (Favorite scents?)')
        self.in_s = self.add_text_input(True, 60)
        self.add_label('Taste (Comforting food?)')
        self.in_t = self.add_text_input(True, 60)
        self.add_label('Touch (Soft, warm?)')
        self.in_o = self.add_text_input(True, 60)
        self.add_action_button('Save Plan', CLR_SOOTHE_PRIMARY,
                               self.save_senses)

    def save_senses(self):
        data = load_data()
        data["senses"].append({
            "v": self.in_v.text.strip(),
            "h": self.in_h.text.strip(),
            "s": self.in_s.text.strip(),
            "t": self.in_t.text.strip(),
            "o": self.in_o.text.strip()
        })
        save_data(data)
        show_popup('Saved!', 'Sensory plan saved.')
        self.in_v.text = ""
        self.in_h.text = ""
        self.in_s.text = ""
        self.in_t.text = ""
        self.in_o.text = ""


class SootheBreatheScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Box Breathing", **kwargs)

        self.lbl_breath = Label(
            text='Press Start', font_size=60, color=CLR_CBT_SECOND,
            size_hint_y=None, height=120
        )
        self.content.add_widget(self.lbl_breath)

        self.lbl_btime = Label(
            text='0', font_size=40, color=CLR_HEADING,
            size_hint_y=None, height=80
        )
        self.content.add_widget(self.lbl_btime)

        self.btn_bstart = Button(
            text='Start', background_color=CLR_SOOTHE_PRIMARY,
            color=(1, 1, 1, 1), background_normal='', background_down=''
        )
        self.btn_bstart.bind(on_press=lambda x: self.toggle_breath())
        self.action_bar.add_widget(self.btn_bstart)

        self.is_running = False
        self.breath_event = None
        self.step_index = 0
        self.counter = 0
        self.steps = [
            ("Inhale",  4, CLR_BREATHE_IN),
            ("Hold",    4, CLR_BREATHE_HOLD),
            ("Exhale",  4, CLR_BREATHE_OUT),
            ("Hold",    4, CLR_BREATHE_HOLD)
        ]

    def on_leave(self, *args):
        self.stop_breath()

    def toggle_breath(self):
        if self.is_running:
            self.stop_breath()
        else:
            self.start_breath()

    def start_breath(self):
        self.is_running = True
        self.btn_bstart.text = 'Stop'
        self.step_index = 0
        self.counter = 0
        self.update_breath_ui()
        self.breath_event = Clock.schedule_interval(self.breath_tick, 1)

    def stop_breath(self):
        self.is_running = False
        self.btn_bstart.text = 'Start'
        if self.breath_event:
            self.breath_event.cancel()
            self.breath_event = None
        self.lbl_breath.text = 'Press Start'
        self.lbl_breath.color = CLR_CBT_SECOND
        self.lbl_btime.text = '0'

    def breath_tick(self, dt):
        self.counter += 1
        step_name, step_dur, step_color = self.steps[self.step_index]
        if self.counter >= step_dur:
            self.counter = 0
            self.step_index = (self.step_index + 1) % len(self.steps)
            self.update_breath_ui()
        else:
            self.lbl_btime.text = str(step_dur - self.counter)

    def update_breath_ui(self):
        step_name, step_dur, step_color = self.steps[self.step_index]
        self.lbl_breath.text = step_name
        self.lbl_breath.color = step_color
        self.lbl_btime.text = str(step_dur)


class SootheMindfulScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Mindfulness Timer", **kwargs)

        self.lbl_mtime = Label(
            text='00:00', font_size=72, color=CLR_MINDFUL,
            size_hint_y=None, height=150
        )
        self.content.add_widget(self.lbl_mtime)

        time_grid = BoxLayout(size_hint_y=None, height=60, spacing=10)
        for m in [1, 5, 10]:
            btn = Button(
                text=f'{m} Min', background_color=CLR_SOOTHE_SECOND,
                color=(1, 1, 1, 1), background_normal='', background_down=''
            )
            btn.bind(on_press=lambda x, mins=m: self.set_time(mins * 60))
            time_grid.add_widget(btn)
        self.content.add_widget(time_grid)

        self.btn_mstart = Button(
            text='Start', background_color=CLR_SOOTHE_PRIMARY,
            color=(1, 1, 1, 1), background_normal='', background_down=''
        )
        self.btn_mstart.bind(on_press=lambda x: self.toggle_mindful())
        self.action_bar.add_widget(self.btn_mstart)

        self.is_running = False
        self.timer_event = None
        self.time_left = 0

    def on_leave(self, *args):
        self.stop_mindful(reset=True)

    def set_time(self, sec):
        if not self.is_running:
            self.time_left = sec
            self.update_mindful_ui()

    def toggle_mindful(self):
        if self.is_running:
            self.stop_mindful()
        else:
            self.start_mindful()

    def start_mindful(self):
        if self.time_left <= 0:
            self.set_time(60)
        self.is_running = True
        self.btn_mstart.text = 'Pause'
        self.timer_event = Clock.schedule_interval(self.mindful_tick, 1)

    def stop_mindful(self, reset=False):
        """FIX: Added reset param to distinguish pause vs. completion."""
        self.is_running = False
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        if reset or self.time_left <= 0:
            self.btn_mstart.text = 'Start'
        else:
            self.btn_mstart.text = 'Resume'

    def mindful_tick(self, dt):
        if self.time_left <= 0:
            # FIX: Properly reset on completion
            self.stop_mindful(reset=True)
            self.time_left = 0
            self.update_mindful_ui()
            show_popup('Session Complete', 'Great job staying mindful.')
            return
        self.time_left -= 1
        self.update_mindful_ui()

    def update_mindful_ui(self):
        mins, secs = divmod(max(self.time_left, 0), 60)
        self.lbl_mtime.text = f"{mins:02d}:{secs:02d}"