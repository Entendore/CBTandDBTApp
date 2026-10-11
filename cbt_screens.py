from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from base_widgets import MenuScreen, DetailScreen
from data_manager import load_data, save_data, show_popup
from constants import CLR_CBT_PRIMARY, CLR_CBT_SECOND, CLR_SAVE


class CBTMenuScreen(MenuScreen):
    def on_enter(self, *args):
        self.title_label.text = 'CBT Tools'
        self.title_label.color = CLR_CBT_PRIMARY
        grid = self.menu_grid
        grid.clear_widgets()
        buttons = [
            ("Thought Record", 'cbt_thought', CLR_CBT_PRIMARY),
            ("Behavioral Activation", 'cbt_activity', CLR_CBT_SECOND),
            ("Coping Cards", 'cbt_coping', CLR_CBT_PRIMARY),
            ("Values Clarification", 'cbt_values', CLR_CBT_SECOND)
        ]
        for text, screen, color in buttons:
            btn = Button(
                text=text, font_size='18sp',
                size_hint_y=None, height=60,
                background_color=color, color=(1, 1, 1, 1),
                background_normal='', background_down=''
            )
            btn.bind(
                on_press=lambda x, s=screen: setattr(self.manager, 'current', s)
            )
            grid.add_widget(btn)


class CBTThoughtScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Thought Record", **kwargs)
        self.add_label('Situation')
        self.in_sit = self.add_text_input(True, 80)
        self.add_label('Automatic Thought')
        self.in_tho = self.add_text_input(True, 80)
        self.add_label('Cognitive Distortion')
        self.spin = self.add_spinner([
            'All-or-Nothing', 'Catastrophizing', 'Mind Reading',
            'Overgeneralization', 'Emotional Reasoning', 'Personalization'
        ])
        self.add_label('Rational Thought')
        self.in_rat = self.add_text_input(True, 80)
        self.add_action_button('Save', CLR_SAVE, self.save_thought)

    def save_thought(self):
        data = load_data()
        rec = {
            "situation": self.in_sit.text,
            "thought": self.in_tho.text,
            "distortion": self.spin.text,
            "rational": self.in_rat.text
        }
        if not rec["situation"] or not rec["thought"]:
            show_popup('Missing Info', 'Fill out Situation and Thought.')
            return
        data["thoughts"].append(rec)
        save_data(data)
        show_popup('Saved!', 'Thought record saved.')
        self.in_sit.text = ""
        self.in_tho.text = ""
        self.spin.text = 'Select'
        self.in_rat.text = ""


class CBTActivityScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Behavioral Activation", **kwargs)
        self.add_label('Activity Description')
        self.in_act = self.add_text_input(True, 80)
        self.add_label('Mastery (1-10)')
        self.in_mast = self.add_text_input(False, 44)
        self.in_mast.input_filter = 'int'
        self.add_label('Pleasure (1-10)')
        self.in_pleas = self.add_text_input(False, 44)
        self.in_pleas.input_filter = 'int'
        self.add_action_button('Save', CLR_SAVE, self.save_act)

    def save_act(self):
        # FIX: Validate that text is present and within range
        try:
            m = int(self.in_mast.text)
            p = int(self.in_pleas.text)
        except ValueError:
            show_popup('Error', 'Mastery/Pleasure must be whole numbers.')
            return
        if not (1 <= m <= 10 and 1 <= p <= 10):
            show_popup('Error', 'Mastery/Pleasure must be between 1 and 10.')
            return
        if not self.in_act.text.strip():
            show_popup('Error', 'Please describe the activity.')
            return
        data = load_data()
        data["activities"].append({
            "act": self.in_act.text.strip(), "mastery": m, "pleasure": p
        })
        save_data(data)
        show_popup('Saved!', 'Activity logged.')
        self.in_act.text = ""
        self.in_mast.text = ""
        self.in_pleas.text = ""


class CBTCopingScreen(DetailScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Coping Cards", **kwargs)
        self.idx = 0

        # FIX: Don't use Window.width at init time; bind width dynamically
        self.lbl_card = Label(
            text='No cards yet', font_size=26,
            size_hint_y=0.3, color=CLR_CBT_PRIMARY,
            halign='center', valign='middle'
        )
        self.lbl_card.bind(
            width=lambda *a: setattr(
                self.lbl_card, 'text_size',
                (self.lbl_card.width * 0.9, None)
            )
        )
        self.content.add_widget(self.lbl_card)

        # Navigation
        nav = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_prev = Button(
            text='< Prev', background_color=CLR_CBT_PRIMARY,
            color=(1, 1, 1, 1), background_normal='', background_down=''
        )
        btn_prev.bind(on_press=lambda x: self.next_card(-1))
        btn_next = Button(
            text='Next >', background_color=CLR_CBT_PRIMARY,
            color=(1, 1, 1, 1), background_normal='', background_down=''
        )
        btn_next.bind(on_press=lambda x: self.next_card(1))
        nav.add_widget(btn_prev)
        nav.add_widget(btn_next)
        self.content.add_widget(nav)

        self.add_label('New Coping Statement')
        self.in_new = self.add_text_input(False, 44)
        self.add_action_button('Add Card', CLR_CBT_SECOND, self.add_card)
        self._refresh_cards()

    def on_enter(self, *args):
        """FIX: Refresh card display each time screen is entered."""
        self._refresh_cards()

    def _refresh_cards(self):
        data = load_data()
        cards = data.get("coping_cards", [])
        if cards:
            # Clamp idx to valid range
            self.idx = min(self.idx, len(cards) - 1)
            self.lbl_card.text = cards[self.idx]
        else:
            self.idx = 0
            self.lbl_card.text = 'No cards yet — add one below!'

    def next_card(self, direction):
        data = load_data()
        cards = data["coping_cards"]
        if not cards:
            return
        self.idx = (self.idx + direction) % len(cards)
        self.lbl_card.text = cards[self.idx]

    def add_card(self):
        text = self.in_new.text.strip()
        if not text:
            show_popup('Empty', 'Enter a coping statement first.')
            return
        data = load_data()
        data["coping_cards"].append(text)
        save_data(data)
        self.idx = len(data["coping_cards"]) - 1
        self.in_new.text = ""
        self.lbl_card.text = text


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
        if not val:
            show_popup('Missing', 'Enter a core value.')
            return
        data = load_data()
        data["values"].append({
            "value": val, "action": self.in_act.text.strip()
        })
        save_data(data)
        show_popup('Saved!', 'Value saved.')
        self.in_val.text = ""
        self.in_act.text = ""