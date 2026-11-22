from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

from constants import (
    CLR_BACK, CLR_WHITE, CLR_TITLE, CLR_HEADING, CLR_LIGHT_TEXT,
    CLR_NAV_BG, CLR_NAV_TEXT, CLR_CBT_PRIMARY, CLR_DBT_PRIMARY,
    CLR_SOOTHE_PRIMARY, CLR_TOOLS_PRIMARY
)


class RootWidget(BoxLayout):
    """Root layout: ScreenManager on top, navigation bar on bottom.
    Built entirely in Python so the app works without a .kv file."""

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Screen manager
        self.sm = ScreenManager()
        self.add_widget(self.sm)

        # Navigation bar
        nav = BoxLayout(size_hint_y=None, height=60, padding=5, spacing=5)

        # Use canvas.before for background color
        with nav.canvas.before:
            self._nav_color = Color(*CLR_NAV_BG)
            self._nav_rect = Rectangle(pos=nav.pos, size=nav.size)
        nav.bind(pos=lambda i, v: setattr(self._nav_rect, 'pos', v),
                 size=lambda i, v: setattr(self._nav_rect, 'size', v))

        nav_buttons = [
            ('Home',   'home',         CLR_NAV_BG),
            ('CBT',    'cbt_menu',     CLR_CBT_PRIMARY),
            ('DBT',    'dbt_menu',     CLR_DBT_PRIMARY),
            ('Soothe', 'soothe_menu',  CLR_SOOTHE_PRIMARY),
            ('Tools',  'tools_menu',   CLR_TOOLS_PRIMARY),
        ]
        for text, screen_name, bg_color in nav_buttons:
            btn = Button(text=text, font_size='14sp',
                         background_color=bg_color, color=CLR_NAV_TEXT,
                         background_normal='', background_down='')
            btn.bind(on_press=lambda x, s=screen_name: self.go_to(s))
            nav.add_widget(btn)

        self.add_widget(nav)

    def go_to(self, screen_name):
        self.sm.current = screen_name


class MenuScreen(Screen):
    """Base menu screen with a title label and a scrollable grid of buttons.
    Built entirely in Python so tests work without a KV file."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Title
        self.title_label = Label(
            font_size='28sp', bold=True,
            size_hint_y=None, height=50, color=CLR_TITLE
        )
        layout.add_widget(self.title_label)

        # Scrollable grid for menu buttons
        scroll = ScrollView()
        self.menu_grid = GridLayout(
            cols=1, size_hint_y=None, spacing=10, padding=10
        )
        self.menu_grid.bind(
            minimum_height=self.menu_grid.setter('height')
        )
        scroll.add_widget(self.menu_grid)
        layout.add_widget(scroll)

        self.add_widget(layout)


class DetailScreen(Screen):
    """Base detail screen with back button, scrollable content, and action bar."""

    def __init__(self, title="", **kwargs):
        super().__init__(**kwargs)
        self.root_layout = BoxLayout(
            orientation='vertical', padding=15, spacing=10
        )

        # Top bar
        top_bar = BoxLayout(size_hint_y=0.08, spacing=10)
        back_btn = Button(
            text='< Back', size_hint_x=0.3,
            background_color=CLR_BACK, color=CLR_WHITE,
            background_normal='', background_down=''
        )
        back_btn.bind(on_press=lambda x: self.go_back())
        title_lbl = Label(
            text=title, font_size=22, bold=True,
            halign='left', valign='middle', color=CLR_TITLE
        )
        # Bind width only for text_size so halign/valign work correctly
        title_lbl.bind(
            width=lambda *a: setattr(title_lbl, 'text_size',
                                     (title_lbl.width, None))
        )
        top_bar.add_widget(back_btn)
        top_bar.add_widget(title_lbl)

        # Content area
        self.scroll = ScrollView(size_hint_y=0.82)
        self.content = BoxLayout(
            orientation='vertical', size_hint_y=None, spacing=12
        )
        self.content.bind(
            minimum_height=self.content.setter('height')
        )
        self.scroll.add_widget(self.content)

        # Action bar
        self.action_bar = BoxLayout(size_hint_y=0.1, spacing=10)

        self.root_layout.add_widget(top_bar)
        self.root_layout.add_widget(self.scroll)
        self.root_layout.add_widget(self.action_bar)
        self.add_widget(self.root_layout)

    def go_back(self):
        # Handle None name, menu screens → home, unknown → home
        name = self.name or ''
        if not self.manager:
            return
        if name.endswith('_menu'):
            self.manager.current = 'home'
        elif name.startswith('cbt'):
            self.manager.current = 'cbt_menu'
        elif name.startswith('dbt'):
            self.manager.current = 'dbt_menu'
        elif name.startswith('soothe'):
            self.manager.current = 'soothe_menu'
        elif name.startswith('tools'):
            self.manager.current = 'tools_menu'
        else:
            self.manager.current = 'home'

    def add_label(self, text, color=None):
        lbl = Label(
            text=text, halign='left', valign='middle',
            size_hint_y=None, height=30,
            font_size='16sp', color=color or CLR_HEADING
        )
        # Bind width only so text_size height is unconstrained;
        # halign then works correctly
        lbl.bind(
            width=lambda *a: setattr(lbl, 'text_size', (lbl.width, None))
        )
        self.content.add_widget(lbl)
        return lbl

    def add_text_input(self, multiline=False, height=60, hint=''):
        ti = TextInput(
            multiline=multiline, size_hint_y=None, height=height,
            hint_text=hint,
            foreground_color=CLR_HEADING,
            hint_text_color=CLR_LIGHT_TEXT,
            background_color=(0.92, 0.91, 0.89, 1)
        )
        self.content.add_widget(ti)
        return ti

    def add_spinner(self, values):
        sp = Spinner(
            text='Select', values=values,
            size_hint_y=None, height=44,
            color=CLR_HEADING,
            background_color=(0.92, 0.91, 0.89, 1)
        )
        self.content.add_widget(sp)
        return sp

    def add_action_button(self, text, color, callback):
        btn = Button(
            text=text, background_color=color, color=CLR_WHITE,
            background_normal='', background_down='',
            font_size='16sp', bold=True
        )
        btn.bind(on_press=lambda x: callback())
        self.action_bar.add_widget(btn)
        return btn  # Return the button so callers can reference it