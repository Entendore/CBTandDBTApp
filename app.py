from kivy.app import App
from kivy.core.window import Window

from base_widgets import RootWidget
from constants import CLR_APP_BG

# Import screens to register with Kivy's Factory
from home_screen import HomeScreen
from cbt_screens import (
    CBTMenuScreen, CBTThoughtScreen, CBTActivityScreen,
    CBTCopingScreen, CBTValuesScreen
)
from dbt_screens import (
    DBTMenuScreen, DBTDiaryScreen, DBTDEARMANScreen,
    DBTOppositeScreen, DBTSTOPScreen, DBTTIPPScreen
)
from soothe_screens import (
    SootheMenuScreen, SootheGroundScreen, SootheSensesScreen,
    SootheBreatheScreen, SootheMindfulScreen
)
from tools_screens import (
    ToolsMenuScreen, ToolsMoodScreen, ToolsGratitudeScreen,
    ToolsHabitsScreen, ToolsSafetyScreen, ToolsCrisisScreen
)


class TherapyApp(App):
    def build(self):
        Window.clearcolor = CLR_APP_BG

        root = RootWidget()
        sm = root.sm

        # Register all screens with the ScreenManager
        screens = [
            HomeScreen(name='home'),
            CBTMenuScreen(name='cbt_menu'),
            CBTThoughtScreen(name='cbt_thought'),
            CBTActivityScreen(name='cbt_activity'),
            CBTCopingScreen(name='cbt_coping'),
            CBTValuesScreen(name='cbt_values'),
            DBTMenuScreen(name='dbt_menu'),
            DBTDiaryScreen(name='dbt_diary'),
            DBTDEARMANScreen(name='dbt_dearman'),
            DBTOppositeScreen(name='dbt_opposite'),
            DBTSTOPScreen(name='dbt_stop'),
            DBTTIPPScreen(name='dbt_tipp'),
            SootheMenuScreen(name='soothe_menu'),
            SootheGroundScreen(name='soothe_ground'),
            SootheSensesScreen(name='soothe_senses'),
            SootheBreatheScreen(name='soothe_breathe'),
            SootheMindfulScreen(name='soothe_mindful'),
            ToolsMenuScreen(name='tools_menu'),
            ToolsMoodScreen(name='tools_mood'),
            ToolsGratitudeScreen(name='tools_gratitude'),
            ToolsHabitsScreen(name='tools_habits'),
            ToolsSafetyScreen(name='tools_safety'),
            ToolsCrisisScreen(name='tools_crisis'),
        ]
        for screen in screens:
            sm.add_widget(screen)

        sm.current = 'home'
        return root


if __name__ == '__main__':
    TherapyApp().run()