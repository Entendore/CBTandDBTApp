import json
import os
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from constants import DATA_FILE, CLR_WHITE, CLR_CBT_SECOND, CLR_HEADING

_DEFAULT_DATA = {
    "moods": [], "thoughts": [], "activities": [], "diary_cards": [],
    "gratitude": [], "coping_cards": ["I can handle this.",
                                       "This feeling is temporary."],
    "opposite_actions": [], "safety_plan": {},
    "habits": {"sleep": False, "meds": False, "eat": False, "move": False},
    "values": [], "senses": []
}


def load_data():
    """Load persisted data; return defaults on any error."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # FIX: Merge with defaults so new keys are always present
                merged = _DEFAULT_DATA.copy()
                merged.update(data)
                # Ensure nested dicts/lists also have defaults
                for key in _DEFAULT_DATA:
                    if key not in data:
                        merged[key] = _DEFAULT_DATA[key]
                return merged
        except (json.JSONDecodeError, IOError, OSError):
            pass
    # Return a *copy* so mutations don't alter the module constant
    import copy
    return copy.deepcopy(_DEFAULT_DATA)


def save_data(data):
    """Persist data to disk with error handling."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except (IOError, OSError) as e:
        show_popup('Save Error', f'Could not save data: {e}')


def show_popup(title, text):
    popup = Popup(
        title=title,
        title_color=CLR_WHITE,
        title_font='Roboto',
        title_size='18sp',
        separator_color=CLR_CBT_SECOND,
        content=Label(
            text=text,
            text_size=(Window.width * 0.7, None),
            halign='center', valign='middle',
            color=CLR_HEADING
        ),
        size_hint=(0.85, 0.45),
        background_color=(0.97, 0.96, 0.94, 1)
    )
    popup.open()